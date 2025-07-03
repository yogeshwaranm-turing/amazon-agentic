import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CloseAccount(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      account_id: str
    ) -> str:
        acct = data["accounts"].pop(account_id, None)
        
        if not acct:
            raise KeyError(f"Account {account_id} not found")
          
        acct["status"] = "closed"
        acct["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return json.dumps(acct)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "close_account",
            "description": "Closes an account.",
            "parameters": {
              "type": "object",
              "properties": { "account_id": { "type": "string" } },
              "required": ["account_id"]
            }
          }
        }
