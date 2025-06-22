import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetUserPaymentSummary(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]

        if user_id not in users:
            return "Error: user not found"

        total_paid = 0.0
        history = []
        for res_id in users[user_id].get("reservations", []):
            res = reservations.get(res_id)
            
            if not res:
                continue
              
            for p in res.get("payment_history", []):
                history.append({"reservation_id": res_id, **p})
                total_paid += p.get("amount", 0)

        return json.dumps({
            "user_id": user_id,
            "total_paid": total_paid,
            "payment_records": history
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_payment_summary",
                "description": (
                    "Compute the total amount paid and list all payment_history entries "
                    "across a user’s reservations."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }
