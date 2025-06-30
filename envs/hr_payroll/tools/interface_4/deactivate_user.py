import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeactivateUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str, reason: str) -> str:
        users = data.get("users", {})
        if user_id not in users:
            raise ValueError(f"User '{user_id}' not found.")

        user = users[user_id]
        if user.get("status") == "inactive":
            raise ValueError(f"User '{user_id}' is already inactive.")

        user["status"] = "inactive"
        user["updated_at"] = "2025-06-30T09:25:07.710335Z"
        return json.dumps({
            "user_id": user_id,
            "status": "inactive",
            "reason": reason,
            "updated_at": user["updated_at"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "deactivate_user",
                "description": "Mark a user as inactive for compliance or access reasons.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID to deactivate."},
                        "reason": {"type": "string", "description": "Reason for deactivation."}
                    },
                    "required": ["user_id", "reason"]
                }
            }
        }
