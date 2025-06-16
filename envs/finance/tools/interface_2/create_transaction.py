import json
from typing import Any, Dict
from datetime import datetime, timezone
from faker import Faker
from tau_bench.envs.tool import Tool
import uuid

fake = Faker()

class CreateTransaction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str, type: str, amount: float, currency: str, description: str) -> str:
        txns = data["transactions"]
        
        new_id = f"TXN-{len(txns)+1:06d}"
        now_iso = datetime.now(timezone.utc).isoformat()
        
        txn = {
            "transaction_id": new_id,
            "account_id": account_id,
            "type": type,
            "amount": amount,
            "currency": currency,
            "timestamp": now_iso,
            "related_id": None,
            "description": description,
            "status": "pending",
            "fee": 0.0,
            "running_balance": None,
            "geo_location": {
              "lat": float(fake.latitude()),
              "lng": float(fake.longitude()),
              "city": fake.city(),
              "country": fake.country()
            },
            "reference_id": f"REF-{uuid.uuid4()}",
            "tags": [],
            "notes": None,
            "merchant": {
              "name": fake.company(),
              "mcc": fake.pystr(min_chars=4, max_chars=4),
              "category": fake.word()
            },
            "channel": "branch"
        }
        txns[new_id] = txn
        
        return json.dumps(txn)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "create_transaction",
            "description": "Insert a new transaction.",
            "parameters": {
              "type": "object",
              "properties": {
                "account_id": { "type": "string" },
                "type": { "type": "string" },
                "amount": { "type": "number" },
                "currency": { "type": "string" },
                "description": { "type": "string" }
              },
              "required": ["account_id", "type", "amount", "currency", "description"]
            }
          }
        }
