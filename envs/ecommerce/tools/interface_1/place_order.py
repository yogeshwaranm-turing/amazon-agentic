import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class PlaceOrder(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        order_date: str,
        items: List[Dict[str, Any]],
    ) -> str:
        # Verify user exists
        if user_id not in data["users"]:
            return "Error: user not found"
        # Verify each product exists
        for item in items:
            product_id = item.get("product_id")
            if product_id not in data["products"]:
                return f"Error: product {product_id} not found"
        
        # Generate unique order_id with format SOXXXX; start at 0010 if none exists
        if data.get("sales_orders"):
            max_so = max(int(so_id[2:]) for so_id in data["sales_orders"].keys())
            new_order_num = max_so + 1
        else:
            new_order_num = 10
        order_id = f"SO{str(new_order_num).zfill(4)}"
        
        # Create order record with status Pending
        order = {
            "order_id": order_id,
            "user_id": user_id,
            "order_date": order_date,
            "status": "Pending"
        }
        data.setdefault("sales_orders", {})[order_id] = order
        
        order_items = []
        # Setup counter for sales_order_item ids with format SOI00000
        if data.get("sales_order_items"):
            max_soi = max(int(soi_id[3:]) for soi_id in data["sales_order_items"].keys())
        else:
            max_soi = 0

        for item in items:
            # Validate quantity greater than 0
            if item.get("quantity", 0) <= 0:
                return f"Error: invalid quantity for product {item.get('product_id')}"
            max_soi += 1
            order_item_id = f"SOI{str(max_soi).zfill(5)}"
            order_item = {
                "so_item_id": order_item_id,
                "sales_order_id": order_id,
                "product_id": item["product_id"],
                "quantity": item["quantity"]
            }
            data.setdefault("sales_order_items", {})[order_item_id] = order_item
            order_items.append(order_item)
        return json.dumps({"order": order, "order_items": order_items})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "place_order",
                "description": "Place an order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user placing the order."
                        },
                        "order_date": {
                            "type": "string",
                            "description": "The date of the order in the format 'YYYY-MM-DD'."
                        },
                        "items": {
                            "type": "array",
                            "description": "An array of order items.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "product_id": {
                                        "type": "string",
                                        "description": "The product ID to order."
                                    },
                                    "quantity": {
                                        "type": "number",
                                        "description": "The quantity of the product."
                                    }
                                },
                                "required": ["product_id", "quantity"]
                            }
                        }
                    },
                    "required": ["user_id", "order_date", "items"]
                }
            }
        }
