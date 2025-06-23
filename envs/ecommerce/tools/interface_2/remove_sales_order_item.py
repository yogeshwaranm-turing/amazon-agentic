import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveSalesOrderItem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        sales_order_id: str,
        product_id: str
    ) -> str:
        sales_order_items = data.get("sales_order_items", [])
        removed_item = None

        # Remove the item from sales_order_items
        if isinstance(sales_order_items, dict):
            # Use list of keys to avoid runtime error during deletion
            keys_to_remove = []
            for key, item in sales_order_items.items():
                if item.get("sales_order_id") == sales_order_id and item.get("product_id") == product_id:
                    removed_item = item
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del sales_order_items[key]
        else:
            # Assume list
            for idx, item in enumerate(sales_order_items):
                if item.get("sales_order_id") == sales_order_id and item.get("product_id") == product_id:
                    removed_item = item
                    del sales_order_items[idx]
                    break

        if removed_item is None:
            return "Error: sales order item not found"

        # Check remaining items in the same sales order
        remaining = 0
        if isinstance(sales_order_items, dict):
            for item in sales_order_items.values():
                if item.get("sales_order_id") == sales_order_id:
                    remaining += 1
        else:
            for item in sales_order_items:
                if item.get("sales_order_id") == sales_order_id:
                    remaining += 1

        order_cancelled = False
        if remaining == 0:
            # Update corresponding sales order to status "Cancelled"
            sales_orders = data.get("sales_orders", [])
            if isinstance(sales_orders, dict):
                for order in sales_orders.values():
                    if order.get("sales_order_id") == sales_order_id:
                        order["status"] = "Cancelled"
                        order["cancellation_reason"] = "Cancelled by the user"
                        order_cancelled = True
                        break
            else:
                for order in sales_orders:
                    if order.get("sales_order_id") == sales_order_id:
                        order["status"] = "Cancelled"
                        order["cancellation_reason"] = "Cancelled by the user"
                        order_cancelled = True
                        break

        result = {
            "removed_item": removed_item,
            "order_cancelled": order_cancelled
        }
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_sales_order_item",
                "description": "Remove a sales order item by sales_order_id and product_id. If this is the last item, cancel the sales order with reason 'Cancelled by the user'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order id."
                        },
                        "product_id": {
                            "type": "string",
                            "description": "The product id."
                        }
                    },
                    "required": ["sales_order_id", "product_id"]
                }
            }
        }
