import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifyQuantityOfPurchaseOrderItem(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str, product_id: str, new_quantity: int) -> str:
        # Validate new_quantity
        if new_quantity <= 0:
            return "Error: new quantity must be greater than 0"
        purchase_order_items = data.get("purchase_order_items", {})
        item_found = None
        if isinstance(purchase_order_items, dict):
            for item in purchase_order_items.values():
                if item.get("purchase_order_id") == purchase_order_id and item.get("product_id") == product_id:
                    item_found = item
                    break
        else:
            for item in purchase_order_items:
                if item.get("purchase_order_id") == purchase_order_id and item.get("product_id") == product_id:
                    item_found = item
                    break
        if item_found is None:
            return "Error: purchase order item not found"
        if int(item_found.get("quantity", 0)) == new_quantity:
            return "Error: new quantity is the same as the current quantity"
        item_found["quantity"] = new_quantity
        return json.dumps(item_found)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_quantity_of_purchase_order_item",
                "description": "Modify the quantity of a purchase order item given purchase_order_id and product_id. Validates that the new quantity is > 0 and different from the current value.",
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
                        },
                        "new_quantity": {
                            "type": "integer",
                            "description": "The new quantity for the purchase order item. Must be > 0 and different from the current quantity."
                        }
                    },
                    "required": ["purchase_order_id", "product_id", "new_quantity"]
                }
            }
        }
