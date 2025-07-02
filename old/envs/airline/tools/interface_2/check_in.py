import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class CheckIn(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]
        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        passengers = res.get("passengers", [])
        legs = res.get("flights", [])
        if not passengers or not legs:
            return "Error: reservation has no passengers or no flight legs"

        # Build a check-in confirmation payload
        checked_in: List[Dict[str, Any]] = []
        for idx, pax in enumerate(passengers):
            full_name = f"{pax['first_name']} {pax['last_name']}"
            for leg in legs:
                checked_in.append({
                    "passenger_index": idx,
                    "passenger_name": full_name,
                    "flight_number": leg["flight_number"],
                    "date": leg["date"]
                })

        return json.dumps({
            "reservation_id": reservation_id,
            "checked_in": checked_in
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_in",
                "description": "Validate and return check-in confirmation for each passenger on every flight leg, without modifying the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID."
                        }
                    },
                    "required": ["reservation_id"]
                }
            }
        }
