import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewSalesOrderItem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        order_id: str,
        product_id: str,
        quantity: int
    ) -> str:
        # Validate quantity
        if quantity <= 0:
            return "Error: quantity must be greater than 0"
        
        # Retrieve sales_order_items list, initialize if missing
        sales_order_items = data.get("sales_order_items")
        if sales_order_items is None:
            # Prefer dict format for consistency
            sales_order_items = {}
            data["sales_order_items"] = sales_order_items

        # Fix: Determine new so_item_id using keys if dict or iterating items if list, following place_order.py
        if isinstance(sales_order_items, dict):
            if sales_order_items:
                max_soi = max(int(key[3:]) for key in sales_order_items.keys())
            else:
                max_soi = 0
            new_so_item_id = f"SOI{str(max_soi + 1).zfill(5)}"
        else:  # assume list
            if sales_order_items:
                max_soi = max(int(item.get("so_item_id", "SOI00000")[3:]) for item in sales_order_items)
            else:
                max_soi = 0
            new_so_item_id = f"SOI{str(max_soi + 1).zfill(5)}"
        
        # Create the new sales order item
        new_item = {
            "so_item_id": new_so_item_id,
            "sales_order_id": order_id,
            "product_id": product_id,
            "quantity": quantity
        }
        
        # Append to sales_order_items (supporting both list and dict)
        if isinstance(sales_order_items, list):
            sales_order_items.append(new_item)
        else:
            sales_order_items[new_so_item_id] = new_item

        return json.dumps(new_item)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_sales_order_item",
                "description": "Add a new sales order item with auto-incremented so_item_id given order_id, product_id, and quantity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The sales order id."
                        },
                        "product_id": {
                            "type": "string",
                            "description": "The product id."
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity for the sales order item. Must be > 0."
                        }
                    },
                    "required": ["order_id", "product_id", "quantity"]
                }
            }
        }
