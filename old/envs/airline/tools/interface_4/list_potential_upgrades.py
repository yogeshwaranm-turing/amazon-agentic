import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListPotentialUpgrades(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        reservation_id: str,
    ) -> str:
        reservations = data["reservations"]
        
        if reservation_id not in reservations:
            return "Error: reservation not found"
          
        cabin = reservations[reservation_id].get("cabin")
        
        upgrade_map = {
            "basic_economy": ["economy", "business"],
            "economy": ["business", "first"],
            "business": ["first"],
            "first": []
        }
        
        potentials = upgrade_map.get(cabin, [])
        
        return json.dumps({
            "reservation_id": reservation_id,
            "current_cabin": cabin,
            "available_upgrades": potentials
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_potential_upgrades",
                "description": "List cabin classes available for upgrade on a reservation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reservation_id": {"type": "string"}
                    },
                    "required": ["reservation_id"]
                }
            }
        }