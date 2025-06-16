import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAccountBalance(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      account_id: str
    ) -> str:
        acct = data["accounts"][account_id] if account_id in data["accounts"] else None
        
        if not acct:
            raise KeyError(f"Account {account_id} not found")
      
        return json.dumps(acct.get("balances", {}))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "get_account_balance",
            "description": "Fetch an account's balances.",
            "parameters": {
              "type": "object",
              "properties": { "account_id": { "type": "string" } },
              "required": ["account_id"]
            }
          }
        }