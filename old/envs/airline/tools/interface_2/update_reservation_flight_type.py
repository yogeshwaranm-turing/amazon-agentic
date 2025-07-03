import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateReservationFlightType(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        new_flight_type: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        allowed = {"one_way", "round_trip"}
        if new_flight_type not in allowed:
            return f"Error: invalid flight_type '{new_flight_type}'"
        
        res["flight_type"] = new_flight_type
        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_reservation_flight_type",
                "description": "Change a reservation’s flight_type (one_way or round_trip).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "ID of the reservation to update."
                        },
                        "new_flight_type": {
                            "type": "string",
                            "description": "Either 'one_way' or 'round_trip'."
                        }
                    },
                    "required": ["reservation_id", "new_flight_type"]
                }
            }
        }
