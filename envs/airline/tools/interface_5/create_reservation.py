import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateReservation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        reservation_details: Dict[str, Any],
    ) -> str:
        reservations, users = data["reservations"], data["users"]
        
        if user_id not in users:
            return "Error: user not found"
        
        # generate a simple unique ID
        reservation_id = f"RES{len(reservations) + 1:05d}"
        if reservation_id in reservations:
            reservation_id = f"{reservation_id}A"
            
        # assemble reservation
        reservation = {
            "reservation_id": reservation_id,
            "user_id": user_id,
            **reservation_details,
            "created_at": "2025-06-19T00:00:00",
        }
        
        # store it
        reservations[reservation_id] = reservation
        users[user_id].setdefault("reservations", []).append(reservation_id)
        
        return json.dumps(reservation)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_reservation",
                "description": "Create a new reservation for a user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user making the reservation.",
                        },
                        "reservation_details": {
                            "type": "object",
                            "description": "All reservation fields (origin, destination, flight_type, cabin, flights, passengers, payment_history, total_baggages, nonfree_baggages, insurance).",
                        },
                    },
                    "required": ["user_id", "reservation_details"],
                },
            },
        }
