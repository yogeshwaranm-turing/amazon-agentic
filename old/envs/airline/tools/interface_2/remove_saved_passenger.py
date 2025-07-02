import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveSavedPassenger(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        passenger_index: int,
    ) -> str:
        users = data["users"]
        if user_id not in users:
            return "Error: user not found"
        saved = users[user_id].get("saved_passengers", [])

        if passenger_index < 0 or passenger_index >= len(saved):
            return "Error: invalid passenger index"

        removed = saved.pop(passenger_index)
        
        return json.dumps({
            "user_id": user_id,
            "removed_passenger": removed,
            "saved_passengers": saved
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_saved_passenger",
                "description": "Delete a passenger from a user’s saved_passengers by index.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "passenger_index": {"type": "integer"}
                    },
                    "required": ["user_id", "passenger_index"]
                }
            }
        }
