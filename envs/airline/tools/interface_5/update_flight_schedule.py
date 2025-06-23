import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateFlightSchedule(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        flight_number: str,
        scheduled_departure_time_est: str = None,
        scheduled_arrival_time_est: str = None,
    ) -> str:
        flights = data["flights"]
        
        if flight_number not in flights:
            return "Error: flight not found"
        f = flights[flight_number]

        if scheduled_departure_time_est is not None:
            f["scheduled_departure_time_est"] = scheduled_departure_time_est  # :contentReference[oaicite:3]{index=3}
        if scheduled_arrival_time_est is not None:
            f["scheduled_arrival_time_est"] = scheduled_arrival_time_est

        return json.dumps({
            "flight_number": flight_number,
            "scheduled_departure_time_est": f["scheduled_departure_time_est"],
            "scheduled_arrival_time_est": f["scheduled_arrival_time_est"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_flight_schedule",
                "description": "Modify the scheduled departure or arrival times for a flight.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flight_number": {"type": "string"},
                        "scheduled_departure_time_est": {
                            "type": "string",
                            "description": "New departure time (HH:MM:SS)."
                        },
                        "scheduled_arrival_time_est": {
                            "type": "string",
                            "description": "New arrival time (HH:MM:SS or HH:MM:SS±offset)."
                        }
                    },
                    "required": ["flight_number"]
                }
            }
        }
