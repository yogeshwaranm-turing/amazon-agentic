import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CancelPurchaseOrderStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str) -> str:
        purchase_orders = data.get("purchase_orders", {})
        if purchase_order_id not in purchase_orders:
            return "Error: purchase_order_id not found in purchase_orders"
        
        # Update the status to "Cancelled"
        purchase_order = purchase_orders[purchase_order_id]
        purchase_order["status"] = "Cancelled"
        data["purchase_orders"][purchase_order_id] = purchase_order
        
        return json.dumps(purchase_order)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_purchase_order_status",
                "description": "Cancel the purchase order status by setting it to 'Cancelled' if the purchase_order_id exists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order id to cancel. Must exist in purchase_orders."
                        }
                    },
                    "required": ["purchase_order_id"]
                }
            }
        }
