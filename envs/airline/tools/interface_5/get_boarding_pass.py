import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetBoardingPass(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]
        
        if reservation_id not in reservations:
            return "Error: reservation not found"
        
        res = reservations[reservation_id]
        
        if res.get("status") != "checked_in":
            return "Error: reservation not checked in"

        passes: List[Dict[str, Any]] = []
        
        for pax in enumerate(res["passengers"]):
            full_name = f"{pax['first_name']} {pax['last_name']}"
            for f in res["flights"]:
                fn = f["flight_number"]
                date = f["date"]
                
                
                passes.append({
                    "reservation_id": reservation_id,
                    "passenger": full_name,
                    "flight_number": fn,
                    "date": date,
                    "origin": f["origin"],
                    "destination": f["destination"],
                })
                
        return json.dumps(passes)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_boarding_pass",
                "description": "Retrieve boarding pass details for all checked-in passengers on a reservation.",
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