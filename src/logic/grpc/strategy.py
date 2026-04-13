import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from generated.grpc import strategy_pb2, strategy_pb2_grpc
from dataaccess.mongo.alert_repository import AlertRepository


class StrategyServicer(strategy_pb2_grpc.StrategyServicer):
    def __init__(self, repo: AlertRepository):
        self._repo = repo

    def CreateAlert(self, request, context):
        alert_data = {
            "of_account_id": request.of_account_id,
            "timeframe": request.timeframe,
            "symbol": request.symbol,
            "indicator": request.indicator,
            "operator": request.operator,
            "trigger": request.trigger,
            "exp": request.exp,
            "message": request.message if request.HasField("message") else "",
        }
        doc = self._repo.create(alert_data)
        return strategy_pb2.CreateAlertResponse(alert=_doc_to_alert(doc))

    def GetAlerts(self, request, context):
        limit = request.limit if request.limit > 0 else 50
        offset = request.offset
        docs = self._repo.get_list(request.of_account_id, limit, offset)
        alerts = [_doc_to_alert(doc) for doc in docs]
        return strategy_pb2.GetAlertsResponse(alerts=alerts)

    def GetAlert(self, request, context):
        doc = self._repo.get_by_id(request.of_account_id, request.alert_id)
        if doc is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Alert {request.alert_id} not found")
            return strategy_pb2.GetAlertResponse()
        return strategy_pb2.GetAlertResponse(alert=_doc_to_alert(doc))

    def UpdateAlert(self, request, context):
        update_data = {
            "timeframe": request.timeframe,
            "symbol": request.symbol,
            "indicator": request.indicator,
            "operator": request.operator,
            "trigger": request.trigger,
            "exp": request.exp,
        }
        if request.HasField("message"):
            update_data["message"] = request.message

        doc = self._repo.update(request.of_account_id, request.alert_id, update_data)
        if doc is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Alert {request.alert_id} not found")
            return strategy_pb2.UpdateAlertResponse()
        return strategy_pb2.UpdateAlertResponse(alert=_doc_to_alert(doc))

    def DeleteAlert(self, request, context):
        deleted = self._repo.delete(request.of_account_id, request.alert_id)
        if not deleted:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Alert {request.alert_id} not found")
            return strategy_pb2.DeleteAlertResponse()
        return strategy_pb2.DeleteAlertResponse(
            of_account_id=request.of_account_id,
            alert_id=request.alert_id,
        )


def _doc_to_alert(doc: dict) -> strategy_pb2.Alert:
    created_at = Timestamp()
    created_at.FromDatetime(doc["created_at"])
    updated_at = Timestamp()
    updated_at.FromDatetime(doc["updated_at"])

    return strategy_pb2.Alert(
        id=doc["id"],
        of_account_id=doc["of_account_id"],
        timeframe=doc["timeframe"],
        symbol=doc["symbol"],
        indicator=doc["indicator"],
        operator=doc["operator"],
        trigger=doc["trigger"],
        exp=doc["exp"],
        message=doc.get("message", ""),
        created_at=created_at,
        updated_at=updated_at,
    )
