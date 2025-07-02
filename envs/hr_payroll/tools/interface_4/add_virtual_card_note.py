
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddVirtualCardNote(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], card_id: str, note: str) -> str:
        cards = data.get("virtual_cards", {})
        if card_id not in cards:
            raise ValueError("Card not found")
        if cards[card_id]["status"] in ["revoked", "expired"]:
            raise ValueError("Cannot modify notes on inactive cards")

        cards[card_id]["note"] = note
        return json.dumps({"card_id": card_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_virtual_card_note",
                "description": "Adds a note for financial tracking",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "card_id": {
                            "type": "string",
                            "description": "Virtual card ID to annotate"
                        },
                        "note": {
                            "type": "string",
                            "description": "The note content to attach"
                        }
                    },
                    "required": ["card_id", "note"]
                }
            }
        }
