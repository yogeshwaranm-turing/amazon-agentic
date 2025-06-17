import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from calculate_baggage_fees import CalculateBaggageFees

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

        fees = json.loads(CalculateBaggageFees.invoke(data, reservation_id))
        amount = fees.get("total_fee", 0)
        
        # simulate payment...
        res = reservations[reservation_id]
        res["baggage_fee_paid"] = True
        res["baggage_fee_amount"] = amount
        res["baggage_fee_payment_method"] = payment_method

        return json.dumps({
            "status": "paid",
            "reservation_id": reservation_id,
            "amount": amount,
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