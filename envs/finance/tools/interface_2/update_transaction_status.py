import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class UpdateTransactionStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], transaction_id: str, status: str) -> str:
        txns = data["transactions"]
        txn = txns[transaction_id] if transaction_id in txns else None
        
        if not txn:
            raise KeyError(f"Transaction {transaction_id} not found")
          
        txn["status"] = status
        txn["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(txn)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "update_transaction_status",
            "description": "Update a transaction's status.",
            "parameters": {
              "type": "object",
              "properties": {
                "transaction_id": { "type": "string" },
                "status": { "type": "string" }
              },
              "required": ["transaction_id", "status"]
            }
          }
        }
