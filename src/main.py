import sys
import logging
import signal
import threading

from queue import Queue

from utils.config_reader import load_yaml_config, parse_args

from handlers.producer.models import ProducerSignalAbstract
from handlers.producer.kafka import KafkaProducer
from handlers.grpc.server import GrpcServer

def serve(config_path: str):
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stdout,
    )
    logger = logging.getLogger(__name__)
    cfg = load_yaml_config(config_path)
    logger.info("Loaded config from %s", config_path)

    # Signals queue and Kafka producer setup and starting
    producerQueue: Queue[ProducerSignalAbstract] = Queue()
    kafkaProducer = KafkaProducer(
        signal_queue=producerQueue,
        bootstrap_servers=cfg["kafka_producer"]["bootstrap_servers"],
    )
    kafkaProducer.start()

    # gRPC server setup and starting
    grpcServer = GrpcServer(
        mongo_uri=cfg["mongo_client"]["uri"],
        mongo_db=cfg["mongo_client"]["database"],
        grpc_address=f"[::]:{cfg['grpc']['port']}",
    )  
    grpcServer.start()

    # Block main thread until interrupted
    shutdown_event = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: shutdown_event.set())
    signal.signal(signal.SIGINT, lambda *_: shutdown_event.set())
    shutdown_event.wait()
    # Stop servers gracefully
    logger.info("Received shutdown signal, stopping servers...")
    grpcServer.stop()
    kafkaProducer.stop()

def main():
    args = parse_args()
    serve(args.config)


if __name__ == "__main__":
    main()