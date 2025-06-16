import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateOrderStatus(Tool):
    VALID_STATUS = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]

    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str, new_status: str) -> str:
        # Validate status
        if new_status not in UpdateOrderStatus.VALID_STATUS:
            return "Error: invalid status"
        # Verify order_id exists
        if "sales_orders" not in data or order_id not in data["sales_orders"]:
            return "Error: order not found"
        # Update order status
        data["sales_orders"][order_id]["status"] = new_status
        return json.dumps({"updated_order": data["sales_orders"][order_id]})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_order_status",
                "description": "Update the status of a sales order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The ID of the sales order."
                        },
                        "new_status": {
                            "type": "string",
                            "description": "The new order status. Must be one of: Pending, Confirmed, Shipped, Delivered, Cancelled."
                        }
                    },
                    "required": ["order_id", "new_status"]
                }
            }
        }
