import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTransactionDetails(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      transaction_id: str
    ) -> str:
        tx = data.get("transactions", {}).get(transaction_id)
        
        if not isinstance(tx, dict):
            raise ValueError("Transaction data is not in the expected format.")
          
        if not transaction_id:
            raise ValueError("Transaction ID cannot be empty.")
          
        if not tx:
            raise Exception("NotFound")
          
        return json.dumps(tx)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_transaction_details",
                "description": "Retrieve details for a specific transaction.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "transaction_id": {
                            "type": "string"
                        }
                    },
                    "required": ["transaction_id"]
                }
            }
        }