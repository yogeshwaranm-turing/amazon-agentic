import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddPaymentMethod(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        payment_method: Dict[str, Any],
    ) -> str:
        users = data["users"]

        if user_id not in users:
            return "Error: user not found"
        user = users[user_id]

        pm = user["payment_methods"]

        # Verify new method ID
        method_id = payment_method.get("id")
        if not method_id:
            return "Error: payment_method.id is required"
        if method_id in pm:
            return "Error: payment_method already exists"

        pm[method_id] = payment_method

        return json.dumps({
            "user_id": user_id,
            "payment_methods": pm
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_payment_method",
                "description": "Add a new payment method to a user’s profile.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user to update."
                        },
                        "payment_method": {
                            "type": "object",
                            "description": "Payment method object, must include ‘id’ and ‘source’ and other fields depending on source.",
                            "properties": {
                                "id": {"type": "string"},
                                "source": {"type": "string"},
                                "brand": {"type": "string"},
                                "last_four": {"type": "string"},
                                "amount": {"type": "number"}
                            },
                            "required": ["id", "source"]
                        }
                    },
                    "required": ["user_id", "payment_method"]
                }
            }
        }
