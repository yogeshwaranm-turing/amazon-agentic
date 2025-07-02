import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifyUserAddress(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, new_address: str) -> str:
        users = data.get("users")
        if not users:
            return "Error: users data not found"
        updated_user = None
        if isinstance(users, dict):
            user = users.get(user_id)
            if not user:
                return f"Error: user {user_id} not found"
            user["address"] = new_address
            updated_user = user
        elif isinstance(users, list):
            for user in users:
                if user.get("user_id") == user_id:
                    user["address"] = new_address
                    updated_user = user
                    break
            if updated_user is None:
                return f"Error: user {user_id} not found"
        return json.dumps(updated_user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_user_address",
                "description": "Modifies the address of a given user identified by user_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The user id."
                        },
                        "new_address": {
                            "type": "string",
                            "description": "The new address to be set."
                        }
                    },
                    "required": ["user_id", "new_address"]
                }
            }
        }

