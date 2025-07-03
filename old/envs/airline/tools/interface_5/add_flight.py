import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AddFlight(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        flight_number: str,
        origin: str,
        destination: str,
        scheduled_departure_time_est: str,
        scheduled_arrival_time_est: str,
    ) -> str:
        flights = data["flights"]
        
        if flight_number in flights:
            return f"Error: flight {flight_number} already exists"
        
        flights[flight_number] = {
            "flight_number": flight_number,
            "origin": origin,
            "destination": destination,
            "scheduled_departure_time_est": scheduled_departure_time_est,
            "scheduled_arrival_time_est": scheduled_arrival_time_est,
            "dates": {},
        }
        
        return json.dumps(flights[flight_number])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_flight",
                "description": "Add a new flight to the system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {
                            "type": "string",
                            "description": "Unique flight code, e.g., 'HAT100'.",
                        },
                        "origin": {
                            "type": "string",
                            "description": "IATA code for departure airport.",
                        },
                        "destination": {
                            "type": "string",
                            "description": "IATA code for arrival airport.",
                        },
                        "scheduled_departure_time_est": {
                            "type": "string",
                            "description": "Scheduled departure time (HH:MM:SS).",
                        },
                        "scheduled_arrival_time_est": {
                            "type": "string",
                            "description": "Scheduled arrival time (HH:MM:SS or with offset).",
                        },
                    },
                    "required": ["flight_number", "origin", "destination", "scheduled_departure_time_est", "scheduled_arrival_time_est"],
                },
            },
        }
