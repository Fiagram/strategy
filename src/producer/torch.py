import json
import logging
import threading
from queue import Queue, Empty

from confluent_kafka import Producer

logger = logging.getLogger(__name__)


class TorchProducer:
    def __init__(
        self,
        signal_queue: Queue,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "torch",
    ):
        self._queue = signal_queue
        self._topic = topic
        self._bootstrap_servers = bootstrap_servers
        self._producer: Producer | None = None
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self):
        """Start the producer thread."""
        self._stop_event.clear()
        self._producer = Producer({
            "bootstrap.servers": self._bootstrap_servers,
            "acks": "all",
            "retries": 3,
        })
        self._thread = threading.Thread(target=self._run, name="kafka-signal-producer", daemon=True)
        self._thread.start()
        logger.info("Kafka producer started (servers=%s, topic=%s)", self._bootstrap_servers, self._topic)

    def stop(self):
        """Signal the producer thread to stop and wait for it to finish."""
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=10)
        if self._producer:
            self._producer.flush(timeout=5)
        logger.info("Kafka producer stopped")

    def _on_delivery(self, err, msg):
        """Delivery callback invoked by confluent-kafka."""
        if err is not None:
            logger.error("Delivery failed for %s: %s", msg.key(), err)
        else:
            logger.info(
                "Published signal -> %s [partition=%s offset=%s]",
                msg.topic(),
                msg.partition(),
                msg.offset(),
            )

    def _run(self):
        """Main loop: drain the queue and publish to Kafka."""
        while not self._stop_event.is_set():
            # Service delivery callbacks from previous produce() calls
            self._producer.poll(0)

            try:
                signal = self._queue.get(timeout=1)
            except Empty:
                continue

            try:
                symbol = signal.get("symbol", "unknown")
                self._producer.produce(
                    self._topic,
                    key=symbol.encode("utf-8") if symbol else None,
                    value=json.dumps(signal).encode("utf-8"),
                    callback=self._on_delivery,
                )
            except BufferError:
                logger.warning("Producer queue full, flushing...")
                self._producer.flush(timeout=5)
                # Retry after flush
                self._producer.produce(
                    self._topic,
                    key=symbol.encode("utf-8") if symbol else None,
                    value=json.dumps(signal).encode("utf-8"),
                    callback=self._on_delivery,
                )
            except Exception:
                logger.exception("Failed to publish signal: %s", signal)
            finally:
                self._queue.task_done()
