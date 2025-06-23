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
                "updates": { 
                  "type": "object",
                  "properties": {
                    "first_name": {
                      "type": "string"
                    },
                    "last_name": {
                      "type": "string"
                    },
                    "email": {
                      "type": "string",
                      "format": "email"
                    },
                    "date_of_birth": {
                      "type": "string",
                      "format": "date"
                    },
                    "phone_number": {
                      "type": "string"
                    },
                    "address": {
                      "type": "object",
                      "properties": {
                        "street": {
                          "type": "string"
                        },
                        "city": {
                          "type": "string"
                        },
                        "state": {
                          "type": "string"
                        },
                        "postal_code": {
                          "type": "string"
                        },
                        "country": {
                          "type": "string"
                        }
                      }
                    },
                    "timezone": {
                      "type": "string",
                      "description": "User's timezone, e.g., 'America/New_York'."
                    },
                  }
                }
              },
              "required": ["user_id", "updates"]
            }
          }
        }