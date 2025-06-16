import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class UpdateDepositStatus(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      deposit_id: str, 
      status: str
    ) -> str:
        deps = data["deposits"]
        dep = deps.get(deposit_id)
        
        if not dep:
            raise KeyError(f"Deposit {deposit_id} not found")
          
        dep["status"] = status
        dep["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        if status == "completed":
            dep["cleared_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            
        return json.dumps(dep)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "update_deposit_status",
            "description": "Update a deposit's status.",
            "parameters": {
              "type": "object",
              "properties": {
                "deposit_id": { "type": "string" },
                "status": { "type": "string" }
              },
              "required": ["deposit_id", "status"]
            }
          }
        }
