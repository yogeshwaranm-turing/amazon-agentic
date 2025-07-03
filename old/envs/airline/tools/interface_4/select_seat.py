import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SelectSeat(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        flight_number: str,
        passenger_index: int,
        seat: str,
    ) -> str:
        flights = data["flights"]
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        res = reservations[reservation_id]
        cabin = res["cabin"]

        # locate flight date
        for f in res["flights"]:
            if f["flight_number"] == flight_number:
                date = f["date"]
                break
        else:
            return "Error: flight not in reservation"

        # check availability
        avail = flights[flight_number]["dates"][date]["available_seats"].get(cabin, 0)
        
        if avail < 1:
            return "Error: no seats available in cabin"
        
        flights[flight_number]["dates"][date]["available_seats"][cabin] -= 1

        # record assignment
        res.setdefault("seat_assignments", {}).setdefault(flight_number, {})[str(passenger_index)] = seat
        
        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "select_seat",
                "description": "Assign a specific seat to a passenger on a flight.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"},
                        "flight_number": {"type": "string"},
                        "passenger_index": {"type": "integer"},
                        "seat": {"type": "string"}
                    },
                    "required": ["reservation_id", "flight_number", "passenger_index", "seat"]
                }
            }
        }