import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifyUnitCostOfPurchaseOrderItem(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str, product_id: str, new_unit_cost: float) -> str:
        # Validate new_unit_cost
        if new_unit_cost <= 0:
            return "Error: new unit cost must be greater than 0"
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
        if float(item_found.get("unit_cost", 0)) == new_unit_cost:
            return "Error: new unit cost is the same as the current unit cost"
        item_found["unit_cost"] = new_unit_cost
        return json.dumps(item_found)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_unit_cost_of_purchase_order_item",
                "description": "Modify the unit cost of a purchase order item given purchase_order_id and product_id. Validates that the new cost is > 0 and different from the current cost.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The ID of the purchase order."
                        },
                        "product_id": {
                            "type": "string",
                            "description": "The product ID in the purchase order item to locate it."
                        },
                        "new_unit_cost": {
                            "type": "number",
                            "description": "The new unit cost for the item. Must be > 0 and different from the current cost."
                        }
                    },
                    "required": ["purchase_order_id", "product_id", "new_unit_cost"]
                }
            }
        }

