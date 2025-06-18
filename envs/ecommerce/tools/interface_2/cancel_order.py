import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CancelOrder(Tool):
    @staticmethod
    def invoke(
            data: Dict[str, Any],
            sales_order_id: str,
            reason: str
    ) -> str:
        """
        Cancel a pending sales order.
        - Checks that the order exists and is currently Pending.
        - Updates its status to Cancelled.
        - Returns the updated order record or an error message.
        """
        orders = data.get("sales_orders", {})
        if sales_order_id not in orders:
            return f"Error: order {sales_order_id} not found"
        order = orders[sales_order_id]
        if order.get("status") != "Pending":
            return f"Error: cannot cancel order {sales_order_id} because its status is '{order.get('status')}'"

        # Perform cancellation
        order["status"] = "Cancelled"
        order["cancel_reason"] = reason  # optional extra field

        return json.dumps(order)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_order",
                "description": "Cancel a pending sales order. Requires the order to be in 'Pending' status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The ID of the sales order to cancel."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for cancellation (e.g. 'no longer needed')."
                        }
                    },
                    "required": ["sales_order_id", "reason"]
                }
            }
        }