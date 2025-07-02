import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemovePurchaseOrderItem(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str, product_id: str) -> str:
        purchase_order_items = data.get("purchase_order_items", {})
        removed_item = None

        if isinstance(purchase_order_items, dict):
            key_to_remove = None
            for key, item in purchase_order_items.items():
                if item.get("purchase_order_id") == purchase_order_id and item.get("product_id") == product_id:
                    removed_item = item
                    key_to_remove = key
                    break
            if key_to_remove:
                del purchase_order_items[key_to_remove]
            else:
                return "Error: purchase order item not found"
        else:
            # Assume list
            for idx, item in enumerate(purchase_order_items):
                if item.get("purchase_order_id") == purchase_order_id and item.get("product_id") == product_id:
                    removed_item = purchase_order_items.pop(idx)
                    break
            if removed_item is None:
                return "Error: purchase order item not found"

        data["purchase_order_items"] = purchase_order_items
        return json.dumps(removed_item)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_purchase_order_item",
                "description": "Remove a purchase order item by purchase_order_id and product_id from purchase_order_items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The ID of the purchase order."
                        },
                        "product_id": {
                            "type": "string",
                            "description": "The ID of the product."
                        }
                    },
                    "required": ["purchase_order_id", "product_id"]
                }
            }
        }

# ...existing code...

