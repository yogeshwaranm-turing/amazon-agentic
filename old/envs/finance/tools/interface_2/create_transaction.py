import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateTransaction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], account_id: str, type: str, amount: float, currency: str, description: str) -> str:
        txns = data["transactions"]
        
        new_id = f"TXN-{len(txns)+1:06d}"
        now_iso = "2025-01-01T00:00:00Z"
        
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
              "lat": 40.7128,
              "lng": -74.0060,
              "city": "New York",
              "country": "United States"
            },
            "reference_id": f"REF-{new_id}",
            "tags": [],
            "notes": None,
            "merchant": {
              "name": "Generic Store",
              "mcc": "5411",
              "category": "retail"
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
