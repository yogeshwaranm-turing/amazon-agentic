import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EnrollLoyaltyMember(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
    ) -> str:
        users = data["users"]
        
        if user_id not in users:
            return "Error: user not found"
          
        user = users[user_id]
        
        if "loyalty_points" in user:
            return "Error: already enrolled"
          
        user["loyalty_points"] = 0
        user["tier"] = "basic"
        
        return json.dumps({
            "user_id": user_id,
            "tier": user["tier"],
            "points": user["loyalty_points"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "enroll_loyalty_member",
                "description": "Enroll a user into the loyalty program.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }