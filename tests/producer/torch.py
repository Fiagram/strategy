import json
import threading
import time
from queue import Queue
from unittest.mock import MagicMock, patch, call

import pytest

from producer.kafka import TorchProducer


@pytest.fixture
def signal_queue():
    return Queue()


@pytest.fixture
def producer(signal_queue):
    return TorchProducer(signal_queue, bootstrap_servers="localhost:9092", topic="test-topic")


class TestTorchProducerInit:
    def test_default_values(self, signal_queue):
        p = TorchProducer(signal_queue)
        assert p._topic == "torch"
        assert p._bootstrap_servers == "localhost:9092"
        assert p._producer is None
        assert p._thread is None

    def test_custom_values(self, signal_queue):
        p = TorchProducer(signal_queue, bootstrap_servers="broker:9093", topic="custom")
        assert p._topic == "custom"
        assert p._bootstrap_servers == "broker:9093"


class TestStart:
    @patch("src.producer.torch.Producer")
    def test_start_creates_producer_and_thread(self, mock_producer_cls, producer):
        producer.start()
        try:
            mock_producer_cls.assert_called_once_with({
                "bootstrap.servers": "localhost:9092",
                "acks": "all",
                "retries": 3,
            })
            assert producer._thread is not None
            assert producer._thread.is_alive()
            assert not producer._stop_event.is_set()
        finally:
            producer.stop()


class TestStop:
    @patch("src.producer.torch.Producer")
    def test_stop_sets_event_and_flushes(self, mock_producer_cls, producer):
        mock_prod = MagicMock()
        mock_producer_cls.return_value = mock_prod

        producer.start()
        producer.stop()

        assert producer._stop_event.is_set()
        mock_prod.flush.assert_called()

    @patch("src.producer.torch.Producer")
    def test_stop_without_start(self, mock_producer_cls, producer):
        # Should not raise
        producer.stop()


class TestOnDelivery:
    def test_successful_delivery(self, producer, caplog):
        msg = MagicMock()
        msg.topic.return_value = "test-topic"
        msg.partition.return_value = 0
        msg.offset.return_value = 42

        with caplog.at_level("INFO"):
            producer._on_delivery(None, msg)

        assert "Published signal" in caplog.text
        assert "partition=0" in caplog.text
        assert "offset=42" in caplog.text

    def test_failed_delivery(self, producer, caplog):
        msg = MagicMock()
        msg.key.return_value = b"VNM"

        with caplog.at_level("ERROR"):
            producer._on_delivery("Broker unavailable", msg)

        assert "Delivery failed" in caplog.text


class TestRun:
    @patch("src.producer.torch.Producer")
    def test_publishes_signal_from_queue(self, mock_producer_cls, signal_queue):
        mock_prod = MagicMock()
        mock_producer_cls.return_value = mock_prod

        producer = TorchProducer(signal_queue, topic="test-topic")
        producer.start()

        signal = {"symbol": "VNM", "signal": "BUY", "price": 85.5}
        signal_queue.put(signal)
        signal_queue.join()  # wait until task_done() is called

        producer.stop()

        mock_prod.produce.assert_called_once_with(
            "test-topic",
            key=b"VNM",
            value=json.dumps(signal).encode("utf-8"),
            callback=producer._on_delivery,
        )

    @patch("src.producer.torch.Producer")
    def test_publishes_signal_with_missing_symbol(self, mock_producer_cls, signal_queue):
        mock_prod = MagicMock()
        mock_producer_cls.return_value = mock_prod

        producer = TorchProducer(signal_queue, topic="test-topic")
        producer.start()

        signal = {"signal": "SELL", "price": 100.0}
        signal_queue.put(signal)
        signal_queue.join()

        producer.stop()

        mock_prod.produce.assert_called_once_with(
            "test-topic",
            key=b"unknown",
            value=json.dumps(signal).encode("utf-8"),
            callback=producer._on_delivery,
        )

    @patch("src.producer.torch.Producer")
    def test_handles_buffer_error_with_retry(self, mock_producer_cls, signal_queue):
        mock_prod = MagicMock()
        mock_producer_cls.return_value = mock_prod
        # First produce() raises BufferError, second succeeds
        mock_prod.produce.side_effect = [BufferError("queue full"), None]

        producer = TorchProducer(signal_queue, topic="test-topic")
        producer.start()

        signal = {"symbol": "FPT", "signal": "BUY", "price": 90.0}
        signal_queue.put(signal)
        signal_queue.join()

        producer.stop()

        assert mock_prod.produce.call_count == 2
        mock_prod.flush.assert_any_call(timeout=5)

    @patch("src.producer.torch.Producer")
    def test_handles_generic_exception(self, mock_producer_cls, signal_queue):
        mock_prod = MagicMock()
        mock_producer_cls.return_value = mock_prod
        mock_prod.produce.side_effect = RuntimeError("unexpected")

        producer = TorchProducer(signal_queue, topic="test-topic")
        producer.start()

        signal = {"symbol": "HPG", "signal": "BUY", "price": 25.0}
        signal_queue.put(signal)
        signal_queue.join()

        producer.stop()
        # Should not crash — exception is logged

    @patch("src.producer.torch.Producer")
    def test_polls_for_delivery_callbacks(self, mock_producer_cls, signal_queue):
        mock_prod = MagicMock()
        mock_producer_cls.return_value = mock_prod

        producer = TorchProducer(signal_queue, topic="test-topic")
        producer.start()

        signal = {"symbol": "VIC", "signal": "SELL", "price": 50.0}
        signal_queue.put(signal)
        signal_queue.join()

        producer.stop()

        mock_prod.poll.assert_called_with(0)