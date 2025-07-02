
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ViewVirtualCardUsage(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], virtual_card_id: str) -> str:
        cards = data.get("virtual_cards", {})
        card = cards.get(virtual_card_id)
        if not card:
            raise ValueError("Virtual card not found")

        # Simulated usage for demo purposes
        usage = float(card.get("limit", 0)) * 0.6
        return json.dumps({
            "card_id": virtual_card_id,
            "limit": card.get("limit"),
            "currency": card.get("currency"),
            "status": card.get("status"),
            "used": round(usage, 2),
            "available": round(float(card.get("limit", 0)) - usage, 2)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "view_virtual_card_usage",
                "description": "Shows limit, usage, and status of a virtual card",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "virtual_card_id": {"type": "string"}
                    },
                    "required": ["virtual_card_id"]
                }
            }
        }
