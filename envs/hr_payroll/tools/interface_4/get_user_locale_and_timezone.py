
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserLocaleAndTimezone(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        users = data.get("users", {})
        user = users.get(user_id)
        if not user:
            raise ValueError("User not found")

        return json.dumps({
            "user_id": user_id,
            "locale": user.get("locale"),
            "timezone": user.get("timezone")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_locale_and_timezone",
                "description": "Retrieves user locale and timezone info",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose locale and timezone are requested"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
