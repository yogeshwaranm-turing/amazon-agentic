import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RedeemLoyaltyMiles(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        miles: int,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]

        if user_id not in users:
            return "Error: user not found"

        # Compute current balance as one point per flight leg
        balance = 0
        for res in reservations.values():
            if res.get("user_id") == user_id:
                balance += len(res.get("flights", []))

        # Check if enough miles
        if miles > balance:
            return "Error: insufficient miles"

        # Calculate remaining balance (no mutation since we have no storage field)
        remaining = balance - miles

        return json.dumps({
            "user_id": user_id,
            "redeemed": miles,
            "remaining_balance": remaining
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "redeem_loyalty_miles",
                "description": "Redeem loyalty miles by consuming points computed as one per flight leg; does not persist changes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "miles": {"type": "integer"}
                    },
                    "required": ["user_id", "miles"]
                }
            }
        }
