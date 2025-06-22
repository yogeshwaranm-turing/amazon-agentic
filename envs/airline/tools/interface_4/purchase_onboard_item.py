import json
import time
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PurchaseOnboardItem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        item: str,
        price: float,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        payment_id = f"onboard_{item}_{int(time.time())}"
        new_payment = {"payment_id": payment_id, "amount": price}
        res.setdefault("payment_history", []).append(new_payment)

        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "purchase_onboard_item",
                "description": (
                    "Record an onboard item purchase by adding a payment entry "
                    "to the reservation’s existing payment_history."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "ID of the reservation to charge."
                        },
                        "item": {
                            "type": "string",
                            "description": "Name of the onboard item or service."
                        },
                        "price": {
                            "type": "number",
                            "description": "Amount to charge for the item."
                        }
                    },
                    "required": ["reservation_id", "item", "price"]
                }
            }
        }
