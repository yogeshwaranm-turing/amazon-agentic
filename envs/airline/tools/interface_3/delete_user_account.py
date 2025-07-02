import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteUserAccount(Tool):
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
        user = users.pop(user_id)

        # Remove each reservation and restore seats
        for res_id in user.get("reservations", []):
            if res_id not in reservations_db:
                continue
            res = reservations_db.pop(res_id)
            cabin = res.get("cabin")
            # For each flight leg, bump available_seats for that cabin
            for leg in res.get("flights", []):
                fn = leg.get("flight_number")
                date = leg.get("date")
                if fn in flights_db:
                    date_info = flights_db[fn].get("dates", {}).get(date)
                    if date_info and cabin in date_info.get("available_seats", {}):
                        date_info["available_seats"][cabin] += 1

        # Return confirmation
        return json.dumps({
            "status": "deleted",
            "user_id": user_id,
            "deleted_reservations": user.get("reservations", [])
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_user_account",
                "description": (
                    "Remove a user and all their reservations, "
                    "restoring seat availability on each flight leg."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user to delete."
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
