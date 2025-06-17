import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from get_baggage_policy import GetBaggagePolicy

class CalculateBaggageFees(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]
        
        if reservation_id not in reservations:
            return "Error: reservation not found"
          
        res = reservations[reservation_id]
        count = res.get("total_baggages", 0)

        # fetch policy
        policy = json.loads(GetBaggagePolicy.invoke(data))
        cabin = res.get("cabin")
        free_allowance = policy.get(cabin, {}).get("free", 0)

        extra = max(0, count - free_allowance)
        fee_per_extra = 50  # flat fee per extra bag
        total_fee = extra * fee_per_extra

        return json.dumps({
            "reservation_id": reservation_id,
            "total_baggages": count,
            "free_allowance": free_allowance,
            "extra_bags": extra,
            "total_fee": total_fee
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_baggage_fees",
                "description": "Calculate any fees due for baggage over the free allowance.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID."
                        }
                    },
                    "required": ["reservation_id"]
                }
            }
        }