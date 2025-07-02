import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListTravelAlerts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
    ) -> str:
        flights = data["flights"]
        alerts: List[Dict[str, Any]] = []
        LOW_SEAT_THRESHOLD = 5

        for flight_number, flight_data in flights.items():
            for date_str, date_info in flight_data.get("dates", {}).items():
                status = date_info.get("status")
                if status != "available":
                    alerts.append({
                        "flight_number": flight_number,
                        "date": date_str,
                        "type": "status_alert",
                        "message": f"Flight {flight_number} on {date_str} is {status}."
                    })

                for cabin, seats_left in date_info.get("available_seats", {}).items():
                    if seats_left < LOW_SEAT_THRESHOLD:
                        alerts.append({
                            "flight_number": flight_number,
                            "date": date_str,
                            "type": "low_seat_alert",
                            "message": (
                                f"Low availability on flight {flight_number} ({cabin}): "
                                f"only {seats_left} seats left."
                            )
                        })

        return json.dumps(alerts)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_travel_alerts",
                "description": (
                    "Generate travel alerts based on flight status and seat availability "
                    "from the flights database."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
