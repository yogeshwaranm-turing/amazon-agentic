import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateSeatSelection(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        flight_number: str,
        passenger_index: int,
        new_seat: str,
    ) -> str:
        reservations = data["reservations"]
        
        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        res = reservations[reservation_id]
        fa = res.get("seat_assignments", {}).get(flight_number)
        
        if not fa or str(passenger_index) not in fa:
            return "Error: no existing seat to update"
        
        fa[str(passenger_index)] = new_seat
        
        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_seat_selection",
                "description": "Change a passenger’s seat assignment on a flight.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"},
                        "flight_number": {"type": "string"},
                        "passenger_index": {"type": "integer"},
                        "new_seat": {"type": "string"}
                    },
                    "required": ["reservation_id", "flight_number", "passenger_index", "new_seat"]
                }
            }
        }