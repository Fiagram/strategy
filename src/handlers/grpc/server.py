import logging
import grpc
from concurrent import futures

from generated.grpc import strategy_pb2, strategy_pb2_grpc
from dataaccess.mongo.alert_repository import AlertRepository
from logic.grpc.strategy import StrategyServicer

logger = logging.getLogger(__name__)

class GrpcServer():
    def __init__(
            self,
            mongo_uri: str,
            mongo_db: str,
            grpc_address: str,
        ):
        self._mongo_uri = mongo_uri
        self._mongo_db = mongo_db
        self._grpc_address = grpc_address
        self._repo = AlertRepository(mongo_uri, mongo_db)
        self._servicer = StrategyServicer(self._repo)
        self._grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        strategy_pb2_grpc.add_StrategyServicer_to_server(self._servicer, self._grpcServer)
        self._grpcServer.add_insecure_port(self._grpc_address)

    def start(self) -> None:
        self._grpcServer.start()
        logger.info("gRPC server started at %s", self._grpc_address)

    def stop(self) -> None:
        self._grpcServer.stop(grace=5)
        logger.info("Shut down gRPC server done!")