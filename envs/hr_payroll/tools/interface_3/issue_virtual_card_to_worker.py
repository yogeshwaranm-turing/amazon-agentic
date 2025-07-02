
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class IssueVirtualCardToWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, limit: float) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers or workers[worker_id]["status"] != "active":
            raise ValueError("Worker is not active or not found")

        user_id = workers[worker_id]["user_id"]
        provider_id = next(iter(data.get("financial_providers", {})), None)
        if not provider_id:
            raise ValueError("No financial provider available")

        cards = data.setdefault("virtual_cards", {})
        existing = [c for c in cards.values() if c.get("user_id") == user_id and c.get("status") == "active"]
        if existing:
            raise ValueError("Active card already exists for this user")

        card_id = str(uuid.uuid4())
        cards[card_id] = {
            "user_id": user_id,
            "provider_id": provider_id,
            "currency": "USD",
            "limit": round(limit, 2),
            "status": "active"
        }

        return json.dumps({"card_id": card_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "issue_virtual_card_to_worker",
                "description": "Creates a virtual card for a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "The ID of the worker receiving the virtual card"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Spending limit for the new card"
                        }
                    },
                    "required": ["worker_id", "limit"]
                }
            }
        }
