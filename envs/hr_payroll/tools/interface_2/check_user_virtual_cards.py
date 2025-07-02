
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CheckUserVirtualCards(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        cards = data.get("virtual_cards", {})
        result = [card for card in cards.values() if card.get("user_id") == user_id]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_user_virtual_cards",
                "description": "Returns the virtual cards owned by the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose virtual cards are being queried"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
