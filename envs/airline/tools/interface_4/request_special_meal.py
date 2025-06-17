import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RequestSpecialMeal(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        passenger_index: int,
        meal_type: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
          
        res = reservations[reservation_id]

        passengers = res.get("passengers", [])
        if passenger_index < 0 or passenger_index >= len(passengers):
            return "Error: invalid passenger index"

        return json.dumps({
            "reservation_id": reservation_id,
            "passenger_index": passenger_index,
            "passenger_name": f"{passengers[passenger_index]['first_name']} {passengers[passenger_index]['last_name']}",
            "meal_type": meal_type,
            "status": "requested"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "request_special_meal",
                "description": "Validate a special meal request for a given passenger; returns a confirmation but doesn’t mutate the reservations database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID."
                        },
                        "passenger_index": {
                            "type": "integer",
                            "description": "Zero-based index of the passenger in the reservation’s passenger list."
                        },
                        "meal_type": {
                            "type": "string",
                            "description": "Type of special meal requested (e.g., vegetarian, kosher)."
                        }
                    },
                    "required": ["reservation_id", "passenger_index", "meal_type"]
                }
            }
        }
