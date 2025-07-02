import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdatePurchaseOrderStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str, new_status: str) -> str:
        # Validate new_status
        allowed_statuses = ["Pending", "Confirmed", "Delivered", "Cancelled"]
        if new_status not in allowed_statuses:
            return f"Error: status must be one of {allowed_statuses}"
        
        purchase_orders = data.get("purchase_orders", {})
        if purchase_order_id not in purchase_orders:
            return "Error: purchase_order_id not found in purchase_orders"
        
        # Update the status in the purchase order
        purchase_order = purchase_orders[purchase_order_id]
        purchase_order["status"] = new_status
        
        # Update the data variable in case of mutable reference
        data["purchase_orders"] = purchase_orders
        
        return json.dumps(purchase_order)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_purchase_order_status",
                "description": "Update the status of a purchase order. The status must be one of ['Pending', 'Confirmed', 'Delivered', 'Cancelled'].",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The ID of the purchase order."
                        },
                        "new_status": {
                            "type": "string",
                            "description": "The new status for the purchase order. Must be one of ['Pending', 'Confirmed', 'Delivered', 'Cancelled']."
                        }
                    },
                    "required": ["purchase_order_id", "new_status"]
                }
            }
        }
