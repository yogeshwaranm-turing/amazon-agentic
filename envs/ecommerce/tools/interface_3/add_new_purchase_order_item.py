import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AddNewPurchaseOrderItem(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        purchase_order_id: str,
        product_id: str,
        quantity: int,
        unit_cost: float
    ) -> str:
        # Validate quantity and unit_cost
        if quantity <= 0:
            return "Error: quantity must be greater than 0"
        if unit_cost <= 0:
            return "Error: unit_cost must be greater than 0"
        
        # Retrieve purchase_orders, products, and purchase_order_items from data variable instead of files
        purchase_orders = data.get("purchase_orders", {})
        if purchase_order_id not in purchase_orders:
            return "Error: purchase_order_id not found in purchase_orders"
        
        products = data.get("products", {})
        if product_id not in products:
            return "Error: product_id not found in products"
        
        purchase_order_items = data.get("purchase_order_items", {})
        
        # Determine new po_item_id with prefix "POI"
        if isinstance(purchase_order_items, dict):
            if purchase_order_items:
                max_poi = max(int(key[3:]) for key in purchase_order_items.keys())
            else:
                max_poi = 0
            new_po_item_id = f"POI{str(max_poi + 1).zfill(5)}"
        else:  # assume list
            if purchase_order_items:
                max_poi = max(int(item.get("po_item_id", "POI00000")[3:]) for item in purchase_order_items)
            else:
                max_poi = 0
            new_po_item_id = f"POI{str(max_poi + 1).zfill(5)}"
        
        # Create the new purchase order item
        new_item = {
            "po_item_id": new_po_item_id,
            "purchase_order_id": purchase_order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_cost": unit_cost
        }
        
        # Append to purchase_order_items supporting both list and dict
        if isinstance(purchase_order_items, list):
            purchase_order_items.append(new_item)
        else:
            purchase_order_items[new_po_item_id] = new_item
        
        # Update the data variable instead of writing to a file
        data["purchase_order_items"] = purchase_order_items
        
        return json.dumps(new_item)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_new_purchase_order_item",
                "description": "Add a new purchase order item with an auto-incremented po_item_id based on the purchase_order_items data. Validates purchase_order_id against purchase_orders and product_id against products.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The purchase order id. Must exist in purchase_orders."
                        },
                        "product_id": {
                            "type": "string",
                            "description": "The product id. Must exist in products."
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity for the purchase order item. Must be > 0."
                        },
                        "unit_cost": {
                            "type": "number",
                            "description": "Unit cost for the purchase order item. Must be > 0."
                        }
                    },
                    "required": ["purchase_order_id", "product_id", "quantity", "unit_cost"]
                }
            }
        }
