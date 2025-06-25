import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPurchaseOrderInformationById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str) -> str:
        purchase_orders = data.get("purchase_orders", {})
        if purchase_order_id not in purchase_orders:
            return f"Error: purchase_order_id {purchase_order_id} not found"
        order_info = purchase_orders[purchase_order_id]
        # New: Retrieve purchase_order_items and filter by purchase_order_id.
        purchase_order_items = data.get("purchase_order_items", {})
        items = [item for item in purchase_order_items.values() if item.get("purchase_order_id") == purchase_order_id]
        order_info["purchase_order_items"] = items
        return json.dumps(order_info)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_purchase_order_information_by_id",
                "description": "Retrieve the information of a purchase order by its ID including its associated purchase order items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order ID."
                        }
                    },
                    "required": ["purchase_order_id"]
                }
            }
        }
