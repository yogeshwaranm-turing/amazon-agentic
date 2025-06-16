import json
from typing import Any, Dict

class GetUserInfo:
    @staticmethod
    def invoke(data: Dict[str, Any], search: str) -> str:
        users = data.get("users", {})
        # Check if search matches a user_id directly
        if search in users:
            return json.dumps(users[search])
        # Otherwise search by email (case-insensitive)
        for user in users.values():
            if user.get("email", "").lower() == search.lower():
                return json.dumps(user)
        return "Error: user not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_info",
                "description": "Search for a user by user_id or email address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search": {
                            "type": "string",
                            "description": "User id or email address to search for."
                        }
                    },
                    "required": ["search"]
                }
            }
        }
