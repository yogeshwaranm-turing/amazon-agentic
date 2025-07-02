import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class BookLoungeAccess(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        lounge: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        return json.dumps({
            "reservation_id": reservation_id,
            "lounge": lounge,
            "status": "booked"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "book_lounge_access",
                "description": "Reserve lounge access for a reservation (simulated confirmation).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"},
                        "lounge": {"type": "string"}
                    },
                    "required": ["reservation_id", "lounge"]
                }
            }
        }
