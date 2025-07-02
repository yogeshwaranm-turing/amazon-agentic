import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddPassenger(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
        first_name: str,
        last_name: str,
        dob: str,
    ) -> str:
        reservations = data["reservations"]

        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        res = reservations[reservation_id]

        new_passenger = {
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob
        }
        
        res.setdefault("passengers", []).append(new_passenger)

        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_passenger",
                "description": "Add a new passenger to an existing reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {
                            "type": "string",
                            "description": "The reservation to modify."
                        },
                        "first_name": {
                            "type": "string",
                            "description": "Passenger’s first name."
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Passenger’s last name."
                        },
                        "dob": {
                            "type": "string",
                            "format": "date",
                            "description": "Passenger’s date of birth (YYYY-MM-DD)."
                        }
                    },
                    "required": ["reservation_id", "first_name", "last_name", "dob"]
                }
            }
        }

