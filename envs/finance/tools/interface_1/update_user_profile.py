import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class UpdateUserProfile(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      user_id: str, 
      updates: Dict[str, Any]
    ) -> str:
        users = data["users"]
        user = users.get(user_id)
        
        if not user:
            raise KeyError(f"User {user_id} not found")
          
        user.update(updates)
        
        user["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "update_user_profile",
            "description": "Update user details.",
            "parameters": {
              "type": "object",
              "properties": {
                "user_id": { "type": "string" },
                "updates": { "type": "object", "additionalProperties": "true" }
              },
              "required": ["user_id", "updates"]
            }
          }
        }