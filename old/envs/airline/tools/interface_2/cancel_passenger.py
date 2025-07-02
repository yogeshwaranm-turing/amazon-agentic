import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CancelPassenger(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        passenger_index: int,
    ) -> str:
        reservations = data["reservations"]
        flights = data["flights"]

        # 1. Verify reservation exists
        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        # 2. Verify passenger index
        passengers = res.get("passengers", [])
        if passenger_index < 0 or passenger_index >= len(passengers):
            return "Error: invalid passenger index"
        
        # 3. Remove the passenger
        passengers.pop(passenger_index)

        # 4. Restore one seat per flight
        cabin = res.get("cabin")
        for leg in res.get("flights", []):
            fn = leg["flight_number"]
            date = leg["date"]
            if fn in flights and date in flights[fn]["dates"]:
                flights[fn]["dates"][date]["available_seats"][cabin] += 1

        # 5. Return updated reservation
        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_passenger",
                "description": "Remove a passenger from a reservation and release one seat back to availability on each flight leg.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID to modify."
                        },
                        "passenger_index": {
                            "type": "integer",
                            "description": "Zero-based index of the passenger in the reservation’s passenger list."
                        }
                    },
                    "required": ["reservation_id", "passenger_index"]
                }
            }
        }
