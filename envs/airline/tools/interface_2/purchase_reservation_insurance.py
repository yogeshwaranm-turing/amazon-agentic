import json
import time
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PurchaseReservationInsurance(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        payment_method_id: str,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        user_id = res.get("user_id")
        if user_id not in users:
            return "Error: user not found"
        user = users[user_id]

        pm = user.get("payment_methods", {})
        if payment_method_id not in pm:
            return "Error: payment method not found"

        if res.get("insurance") == "yes":
            return "Error: insurance already purchased"

        insurance_fee = 30.0  # flat insurance rate
        res["insurance"] = "yes"
        entry = {
            "payment_id": payment_method_id,
            "amount": insurance_fee,
            "timestamp": int(time.time())
        }
        res.setdefault("payment_history", []).append(entry)

        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "purchase_reservation_insurance",
                "description": (
                    "Purchase insurance for a reservation by charging a flat fee "
                    "to a user’s saved payment method and updating the reservation."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "ID of the reservation to insure."
                        },
                        "payment_method_id": {
                            "type": "string",
                            "description": "One of the user’s payment_methods IDs."
                        }
                    },
                    "required": ["reservation_id", "payment_method_id"]
                }
            }
        }

