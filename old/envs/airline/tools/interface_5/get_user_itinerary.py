import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetUserItinerary(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
    ) -> str:
        users = data["users"]
        reservations_db = data["reservations"]
        flights_db = data["flights"]

        if user_id not in users:
            return "Error: user not found"

        # Gather reservation IDs from the user profile
        user_res_ids = users[user_id].get("reservations", [])

        itinerary: List[Dict[str, Any]] = []
        for res_id in user_res_ids:
            # Skip any unknown reservation IDs
            if res_id not in reservations_db:
                continue
            res = reservations_db[res_id]

            # Build base reservation info
            res_info: Dict[str, Any] = {
                "reservation_id": res_id,
                "origin": res.get("origin"),
                "destination": res.get("destination"),
                "flight_type": res.get("flight_type"),
                "cabin": res.get("cabin"),
                "flights": []
            }

            # Enrich each flight leg
            for leg in res.get("flights", []):
                fn = leg.get("flight_number")
                date = leg.get("date")
                leg_info: Dict[str, Any] = {
                    "flight_number": fn,
                    "date": date,
                    "origin": leg.get("origin"),
                    "destination": leg.get("destination"),
                    "price": leg.get("price"),
                }

                # Pull schedule & status from flights DB if available
                if fn in flights_db:
                    f = flights_db[fn]
                    leg_info["scheduled_departure_time_est"] = f.get("scheduled_departure_time_est")
                    leg_info["scheduled_arrival_time_est"]   = f.get("scheduled_arrival_time_est")
                    date_info = f.get("dates", {}).get(date, {})
                    leg_info["status"] = date_info.get("status")
                    # include any actual times or availability/prices if present
                    if "actual_departure_time_est" in date_info:
                        leg_info["actual_departure_time_est"] = date_info["actual_departure_time_est"]
                    if "actual_arrival_time_est" in date_info:
                        leg_info["actual_arrival_time_est"]   = date_info["actual_arrival_time_est"]
                    if "available_seats" in date_info:
                        leg_info["available_seats"] = date_info["available_seats"]
                    if "prices" in date_info:
                        leg_info["prices"] = date_info["prices"]

                res_info["flights"].append(leg_info)

            itinerary.append(res_info)

        return json.dumps({
            "user_id": user_id,
            "itinerary": itinerary
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_itinerary",
                "description": (
                    "Fetch a user’s full itinerary by linking their profile, reservations, and flight schedules."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose itinerary to retrieve."
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }

