import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class RemoveFlightDateInstance(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        flight_number: str,
        date: str,
    ) -> str:
        flights = data["flights"]
        
        if flight_number not in flights:
            return f"Error: flight {flight_number} not found"
        
        if date not in flights[flight_number]["dates"]:
            return f"Error: flight {flight_number} not scheduled on date {date}"
        
        del flights[flight_number]["dates"][date]
        
        return json.dumps({"flight_number": flight_number, "date": date, "removed": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_flight_date_instance",
                "description": "Remove a specific date entry from a flight’s schedule.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {
                            "type": "string",
                            "description": "Flight code, e.g., 'HAT001'.",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date to remove (YYYY-MM-DD).",
                        },
                    },
                    "required": ["flight_number", "date"],
                },
            },
        }
