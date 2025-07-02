import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class TransferReservationOwner(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        current_user_id: str,
        new_user_id: str,
    ) -> str:
        users = data["users"]
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        res = reservations[reservation_id]

        old_uid = res.get("user_id")
        if current_user_id != old_uid:
            return "Error: only the current owner can transfer this reservation"

        if new_user_id not in users:
            return "Error: new user not found"

        users[old_uid].setdefault("reservations", []).remove(reservation_id)

        res["user_id"] = new_user_id
        users[new_user_id].setdefault("reservations", []).append(reservation_id)

        return json.dumps({
            "reservation_id": reservation_id,
            "old_user_id": old_uid,
            "new_user_id": new_user_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_reservation_owner",
                "description": (
                    "Reassign a reservation from its current user to another user, "
                    "but only if the request is made by the current owner."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"},
                        "current_user_id": {"type": "string", "description": "The user ID of the caller; must match the reservation’s owner."},
                        "new_user_id": {"type": "string", "description": "The user ID to transfer the reservation to."}
                    },
                    "required": ["reservation_id", "current_user_id", "new_user_id"]
                }
            }
        }

