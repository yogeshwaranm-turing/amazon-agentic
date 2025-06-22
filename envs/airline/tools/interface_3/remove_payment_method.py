import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemovePaymentMethod(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        method_id: str,
    ) -> str:
        users = data["users"]

        if user_id not in users:
            return "Error: user not found"
          
        user = users[user_id]

        pm = user.get("payment_methods", {})
        if method_id not in pm:
            return "Error: payment_method not found"

        pm.pop(method_id)

        return json.dumps({
            "user_id": user_id,
            "payment_methods": pm
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_payment_method",
                "description": "Remove an existing payment method from a user’s profile.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user to update."
                        },
                        "method_id": {
                            "type": "string",
                            "description": "ID of the payment method to remove."
                        }
                    },
                    "required": ["user_id", "method_id"]
                }
            }
        }

