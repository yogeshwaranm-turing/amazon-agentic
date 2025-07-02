import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAircraftDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        flight_number: str,
    ) -> str:
        flights = data["flights"]
        if flight_number not in flights:
            return "Error: flight not found"

        f = flights[flight_number]
        # Return route and schedule details since no aircraft field exists
        return json.dumps({
            "flight_number": flight_number,
            "origin": f.get("origin"),
            "destination": f.get("destination"),
            "scheduled_dates": list(f.get("dates", {}).keys())
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_aircraft_details",
                "description": (
                    "Fetch route (origin/destination) and scheduled dates for a flight "
                    "from the flights database."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {"type": "string", "description": "The flight number."}
                    },
                    "required": ["flight_number"]
                }
            }
        }
