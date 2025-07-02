import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool
from datetime import timezone

class FreezeAccount(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      account_id: str
    ) -> str:
        acct = data["accounts"][account_id] if account_id in data["accounts"] else None
        
        if not acct:
            raise KeyError(f"Account {account_id} not found")
          
        acct["status"] = "frozen"
        acct["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(acct)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "freeze_account",
            "description": "Freeze an account.",
            "parameters": {
              "type": "object",
              "properties": { "account_id": { "type": "string" } },
              "required": ["account_id"]
            }
          }
        }