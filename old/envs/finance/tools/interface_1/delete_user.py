import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class DeleteUser(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      user_id: str
    ) -> str:
        users = data["users"]
        user = users.get(user_id)
        
        if not user:
            raise KeyError(f"User {user_id} not found")
          
        user["status"] = "deleted"
        user["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "delete_user",
            "description": "Deactivate a user.",
            "parameters": {
              "type": "object",
              "properties": { "user_id": { "type": "string" } },
              "required": ["user_id"]
            }
          }
        }
