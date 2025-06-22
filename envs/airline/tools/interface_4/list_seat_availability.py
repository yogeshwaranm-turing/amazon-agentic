import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListSeatAvailability(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        flight_number: str,
        date: str,
    ) -> str:
        flights = data["flights"]
        
        if flight_number not in flights:
            return "Error: flight not found"
        
        f = flights[flight_number]
        d = f["dates"].get(date)
        
        if not d:
            return "Error: no data for date"
        
        return json.dumps(d["available_seats"])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_seat_availability",
                "description": "List remaining seats by cabin for a given flight and date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {
                            "type": "string",
                            "description": "The flight number."
                        },
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format."
                        }
                    },
                    "required": ["flight_number", "date"]
                }
            }
        }