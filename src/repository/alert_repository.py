import time
from datetime import datetime, timezone

from pymongo import MongoClient
from pymongo.collection import Collection


class AlertRepository:
    def __init__(self, mongo_uri: str = "mongodb://localhost:27017", db_name: str = "fiagram"):
        self._client = MongoClient(mongo_uri)
        self._db = self._client[db_name]
        self._collection: Collection = self._db["alerts"]
        self._collection.create_index("of_account_id")
        self._counter = self._db["counters"]

    def _next_id(self) -> int:
        result = self._counter.find_one_and_update(
            {"_id": "alert_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True,
        )
        return result["seq"]

    def create(self, alert_data: dict) -> dict:
        alert_id = self._next_id()
        now = datetime.now(timezone.utc)
        doc = {
            "_id": alert_id,
            "of_account_id": alert_data["of_account_id"],
            "timeframe": alert_data["timeframe"],
            "symbol": alert_data["symbol"],
            "indicator": alert_data["indicator"],
            "operator": alert_data["operator"],
            "trigger": alert_data["trigger"],
            "exp": alert_data["exp"],
            "message": alert_data.get("message", ""),
            "created_at": now,
            "updated_at": now,
        }
        self._collection.insert_one(doc)
        return self._doc_to_dict(doc)

    def get_by_id(self, of_account_id: int, alert_id: int) -> dict | None:
        doc = self._collection.find_one({"_id": alert_id, "of_account_id": of_account_id})
        if doc is None:
            return None
        return self._doc_to_dict(doc)

    def get_list(self, of_account_id: int, limit: int = 50, offset: int = 0) -> list[dict]:
        cursor = (
            self._collection.find({"of_account_id": of_account_id})
            .skip(offset)
            .limit(limit)
        )
        return [self._doc_to_dict(doc) for doc in cursor]

    def update(self, of_account_id: int, alert_id: int, update_data: dict) -> dict | None:
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = self._collection.find_one_and_update(
            {"_id": alert_id, "of_account_id": of_account_id},
            {"$set": update_data},
            return_document=True,
        )
        if result is None:
            return None
        return self._doc_to_dict(result)

    def delete(self, of_account_id: int, alert_id: int) -> bool:
        result = self._collection.delete_one({"_id": alert_id, "of_account_id": of_account_id})
        return result.deleted_count > 0

    @staticmethod
    def _doc_to_dict(doc: dict) -> dict:
        return {
            "id": doc["_id"],
            "of_account_id": doc["of_account_id"],
            "timeframe": doc["timeframe"],
            "symbol": doc["symbol"],
            "indicator": doc["indicator"],
            "operator": doc["operator"],
            "trigger": doc["trigger"],
            "exp": doc["exp"],
            "message": doc.get("message", ""),
            "created_at": doc["created_at"],
            "updated_at": doc["updated_at"],
        }
