import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateChangeFee(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]
        
        if reservation_id not in reservations:
            return "Error: reservation not found"
          
        res = reservations[reservation_id]
        
        policy: Dict[str, Any] = {
            "basic_economy": {"fee": None, "refundable": False},
            "economy":       {"fee": 100, "refundable": True},
            "business":      {"fee": 50,  "refundable": True},
        }
        
        cabin = res.get("cabin")
        entry = policy.get(cabin, {})
        fee = entry.get("fee")
        
        if fee is None:
            return json.dumps({"reservation_id": reservation_id, "change_allowed": False})
          
        return json.dumps({"reservation_id": reservation_id, "change_fee": fee})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_change_fee",
                "description": "Calculate the fee to change a reservation based on fare class.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"}
                    },
                    "required": ["reservation_id"]
                }
            }
        }