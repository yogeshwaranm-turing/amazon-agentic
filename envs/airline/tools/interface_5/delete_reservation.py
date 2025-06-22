import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteReservation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations, users = data["reservations"], data["users"]
        
        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        # remove from the user’s list
        user_id = reservations[reservation_id]["user_id"]
        if user_id in users and "reservations" in users[user_id]:
            try:
                users[user_id]["reservations"].remove(reservation_id)
            except ValueError:
                pass
        
        # delete it
        del reservations[reservation_id]
        
        return json.dumps({"reservation_id": reservation_id, "deleted": True})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_reservation",
                "description": "Delete an existing reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation ID to delete.",
                        },
                    },
                    "required": ["reservation_id"],
                },
            },
        }
