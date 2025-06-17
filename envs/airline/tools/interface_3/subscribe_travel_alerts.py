import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubscribeTravelAlerts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
    ) -> str:
        users = data["users"]
        
        if user_id not in users:
            return "Error: user not found"
          
        sub = users[user_id].setdefault("alerts_subscribed", False)
        
        if sub:
            return "Error: already subscribed"
          
        users[user_id]["alerts_subscribed"] = True
        
        return json.dumps({
            "user_id": user_id,
            "alerts_subscribed": True
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "subscribe_travel_alerts",
                "description": "Subscribe a user to receive travel alerts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }