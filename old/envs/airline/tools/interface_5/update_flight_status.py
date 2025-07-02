import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateFlightStatus(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        flight_number: str,
        date: str,
        status: str,
    ) -> str:
        flights = data["flights"]
        
        if flight_number not in flights:
            return f"Error: flight {flight_number} not found"
        
        if date not in flights[flight_number]["dates"]:
            return f"Error: flight {flight_number} not scheduled on date {date}"
        
        flights[flight_number]["dates"][date]["status"] = status
        
        return json.dumps(flights[flight_number]["dates"][date])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_flight_status",
                "description": "Update the status for a specific flight on a given date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {
                            "type": "string",
                            "description": "Flight code, e.g., 'HAT001'.",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date of the flight (YYYY-MM-DD).",
                        },
                        "status": {
                            "type": "string",
                            "description": "New status (e.g., 'available', 'cancelled', 'landed', 'delayed').",
                        },
                    },
                    "required": ["flight_number", "date", "status"],
                },
            },
        }
