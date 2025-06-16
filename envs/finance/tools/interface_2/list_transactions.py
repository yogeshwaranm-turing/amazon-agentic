import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class ListTransactions(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        account_id: str, 
        limit: int = 20, 
        start_date: str = None, 
        end_date: str = None
    ) -> str:
        txs = data.get("transactions", {}).values()
        
        if not isinstance(txs, list):
            raise ValueError("Transactions data is not in the expected format.")
        
        if not account_id:
            raise ValueError("Account ID cannot be empty.")
        
        if limit <= 0:
            raise ValueError("Limit must be a positive integer.")
        
        filtered = [t for t in txs if t.get("account_id") == account_id]
        
        if start_date:
            sd = datetime.fromisoformat(start_date)
            filtered = [t for t in filtered if datetime.fromisoformat(t["timestamp"][:-1]) >= sd]
            
        if end_date:
            ed = datetime.fromisoformat(end_date)
            filtered = [t for t in filtered if datetime.fromisoformat(t["timestamp"][:-1]) <= ed]
            
        filtered.sort(key=lambda x: x["timestamp"], reverse=True)

        return json.dumps(filtered[:limit])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_transactions",
                "description": "Fetch recent transactions on an account.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {
                            "type": "string"
                        },
                        "limit": {
                            "type": "integer"
                        },
                        "start_date": {
                            "type": "string", 
                            "format": "date-time"
                        },
                        "end_date": {
                            "type": "string", 
                            "format": "date-time"
                        }
                    },
                    "required": ["account_id"]
                }
            }
        }