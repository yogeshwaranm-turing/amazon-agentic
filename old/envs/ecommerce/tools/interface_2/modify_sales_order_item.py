import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifySalesOrderItem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: str,
        product_id: str,
        new_quantity: int
    ) -> str:
        # Validate new_quantity
        if new_quantity <= 0:
            return "Error: new quantity must be greater than 0"
        sales_order_items = data["sales_order_items"]
        # Handle sales_order_items as dict or list
        if isinstance(sales_order_items, dict):
            items_iter = sales_order_items.values()
        else:
            items_iter = sales_order_items

        for item in items_iter:
            if item['sales_order_id'] == sales_order_id and item['product_id'] == product_id:
                old_quantity = int(item['quantity'])  # force type conversion
                if old_quantity == new_quantity:
                    return "Error: new quantity is the same as the old quantity"
                item['quantity'] = new_quantity
                return json.dumps(item)
        return "Error: sales order item not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_sales_order_item",
                "description": "Modify the quantity of a sales order item based on sales_order_id and product_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The ID of the sales order."
                        },
                        "product_id": {
                            "type": "string",
                            "description": "The ID of the product."
                        },
                        "new_quantity": {
                            "type": "integer",
                            "description": "The new quantity for the item. Must be > 0 and different from the current quantity."
                        }
                    },
                    "required": ["sales_order_id", "product_id", "new_quantity"]
                }
            }
        }
