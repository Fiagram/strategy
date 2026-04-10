import argparse
import logging
import sys
from concurrent import futures

import grpc
import yaml

from generated.grpc import strategy_pb2_grpc
from repository.alert_repository import AlertRepository
from server.strategy_servicer import StrategyServicer

DEFAULT_CONFIG_PATH = "configs/local.yaml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fiagram Strategy gRPC Server")
    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help=f"Path to YAML config file (default: {DEFAULT_CONFIG_PATH})",
    )
    return parser.parse_args()


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def serve(config_path: str):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stdout,
    )
    logger = logging.getLogger(__name__)

    cfg = load_config(config_path)
    logger.info("Loaded config from %s", config_path)

    repo = AlertRepository(
        mongo_uri=cfg["mongo_client"]["uri"],
        db_name=cfg["mongo_client"]["database"],
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    strategy_pb2_grpc.add_StrategyServicer_to_server(StrategyServicer(repo), server)

    listen_addr = f"[::]:{cfg['grpc']['port']}"
    server.add_insecure_port(listen_addr)
    server.start()
    logger.info("gRPC server started on %s", listen_addr)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server...")
        server.stop(grace=5)


def main():
    args = parse_args()
    serve(args.config)


if __name__ == "__main__":
    main()