import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PayBaggageFee(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        payment_method: str,
    ) -> str:
        reservations = data["reservations"]
        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        res = reservations[reservation_id]
        count = res.get("total_baggages", 0)

        # fetch policy
        policy: Dict[str, Any] = {
            "basic_economy": {"free": 1, "weight_limit_kg": 20},
            "economy":       {"free": 2, "weight_limit_kg": 23},
            "business":      {"free": 3, "weight_limit_kg": 32},
        }
        cabin = res.get("cabin")
        free_allowance = policy.get(cabin, {}).get("free", 0)

        extra = max(0, count - free_allowance)
        fee_per_extra = 50  # flat fee per extra bag
        total_fee = extra * fee_per_extra
        
        # simulate payment...
        res = reservations[reservation_id]
        res["baggage_fee_paid"] = True
        res["baggage_fee_amount"] = total_fee
        res["baggage_fee_payment_method"] = payment_method

        return json.dumps({
            "status": "paid",
            "reservation_id": reservation_id,
            "amount": total_fee,
            "method": payment_method
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "pay_baggage_fee",
                "description": "Pay any calculated baggage fees on a reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"},
                        "payment_method": {"type": "string", "description": "e.g., credit_card, paypal"}
                    },
                    "required": ["reservation_id", "payment_method"]
                }
            }
        }