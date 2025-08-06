import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class get_user_information(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        email: Optional[str] = None
    ) -> str:
        """
        Retrieve user records, optionally filtering by user_id or email. 
        Returns a JSON list of matching users.
        """
        users = data.get("users", {})
        result = {}
        for uid, user in users.items():
            # Filter by user_id if provided
            if user_id and str(uid) != user_id:
                continue
            # Filter by email if provided
            if email and user.get("email") != email:
                continue
            return(json.dumps(user))


        raise ValueError("User not found")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_information",
                "description": "Retrieve user information with optional filters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Filter by user ID"},
                        "email": {"type": "string", "description": "Filter by user email"}
                    },
                    "required": []
                }
            }
        }
