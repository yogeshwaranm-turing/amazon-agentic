import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetMembershipTier(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]

        if user_id not in users:
            return "Error: user not found"

        # Compute “loyalty points” as one point per flight leg
        points = 0
        for res in reservations.values():
            if res.get("user_id") == user_id:
                points += len(res.get("flights", []))   # each leg counts as one point :contentReference[oaicite:0]{index=0}

        # Determine tier based on points
        if points < 5:
            tier = "bronze"
        elif points < 15:
            tier = "silver"
        else:
            tier = "gold"

        # 4. Return tier and points
        return json.dumps({
            "user_id": user_id,
            "tier": tier,
            "loyalty_points": points
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_membership_tier",
                "description": "Compute a user’s membership tier based on loyalty points (one point per flight leg).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user to look up."
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
