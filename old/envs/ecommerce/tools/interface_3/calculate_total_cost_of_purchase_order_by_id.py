import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateTotalCostOfPurchaseOrderById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str) -> str:
        purchase_order_items = data.get("purchase_order_items", {})
        total_cost = 0.0

        if isinstance(purchase_order_items, dict):
            for item in purchase_order_items.values():
                if item.get("purchase_order_id") == purchase_order_id:
                    total_cost += item.get("quantity", 0) * item.get("unit_cost", 0)
        else:  # assume list
            for item in purchase_order_items:
                if item.get("purchase_order_id") == purchase_order_id:
                    total_cost += item.get("quantity", 0) * item.get("unit_cost", 0)

        return json.dumps({"purchase_order_id": purchase_order_id, "total_cost": total_cost})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_total_cost_of_purchase_order_by_id",
                "description": "Calculate the sum of quantity*unit_cost for each purchase order item with the given purchase_order_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The id of the purchase order for which the total cost is calculated."
                        }
                    },
                    "required": ["purchase_order_id"]
                }
            }
        }
