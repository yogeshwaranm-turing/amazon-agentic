from typing import Dict, Any
from uuid import uuid4
from tau_bench.envs.tool import Tool

class GenerateUserInviteToken(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> Dict[str, str]:
        users = data["users"]
        if user_id not in users:
            raise ValueError("User not found")

        token = str(uuid4())
        users[user_id]["invite_token"] = token
        return {"user_id": user_id, "invite_token": token}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "generate_user_invite_token",
            "description": "Generate a unique invite token for user onboarding.",
            "parameters": {
                "user_id": {"type": "string", "description": "User ID"}
            },
            "returns": {"type": "object", "description": "User ID and generated token"}
        }