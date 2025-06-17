import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetLoyaltyBalance(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]

        if user_id not in users:
            return "Error: user not found"

        # Sum up flight legs across this user's reservations
        points = 0
        for res in reservations.values():
            if res.get("user_id") == user_id:
                # each entry in res["flights"] is one flight leg :contentReference[oaicite:0]{index=0}
                points += len(res.get("flights", []))

        return json.dumps({
            "user_id": user_id,
            "loyalty_points": points
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_loyalty_balance",
                "description": "Compute a user's loyalty points as one point per flight leg across all their reservations.",
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
