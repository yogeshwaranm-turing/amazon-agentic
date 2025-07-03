import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateTotalCostOfOrderById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str) -> str:
        total_cost = 0.0
        # Retrieve sales_order_items
        sales_order_items = data.get("sales_order_items")
        # Retrieve products data; assume dict with product_id keys or list format
        products = data.get("products", {})
        matching_items = []
        if isinstance(sales_order_items, dict):
            matching_items = [item for item in sales_order_items.values() if item.get("sales_order_id") == order_id]
        elif isinstance(sales_order_items, list):
            matching_items = [item for item in sales_order_items if item.get("sales_order_id") == order_id]
        
        # Calculate total cost
        for item in matching_items:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 0)
            unit_price = 0.0
            if isinstance(products, dict):
                prod = products.get(product_id, {})
                unit_price = prod.get("unit_price", 0.0)
            elif isinstance(products, list):
                # Find the product in the list
                prod = next((p for p in products if p.get("product_id") == product_id), {})
                unit_price = prod.get("unit_price", 0.0)
            total_cost += quantity * unit_price
        
        return json.dumps({"order_id": order_id, "total_cost": total_cost})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_total_cost_of_order_by_id",
                "description": "Calculates the total cost of a sales order by summing the product of quantity and unit price for each sales order item.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The sales order id."
                        }
                    },
                    "required": ["order_id"]
                }
            }
        }

