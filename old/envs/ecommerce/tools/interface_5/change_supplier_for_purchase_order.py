import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ChangeSupplierForPurchaseOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], purchase_order_id: str, new_supplier_id: str) -> str:
        # Ensure purchase_orders exists in data
        if "purchase_orders" not in data:
            return json.dumps({"error": "purchase_orders data not provided"})
        if purchase_order_id not in data["purchase_orders"]:
            return json.dumps({"error": f"Purchase order '{purchase_order_id}' not found"})

        # Validate new supplier exists
        if "suppliers" not in data:
            return json.dumps({"error": "suppliers data not provided"})
        if new_supplier_id not in data["suppliers"]:
            return json.dumps({"error": f"Supplier '{new_supplier_id}' not found"})

        # Update the supplier_id for the purchase order
        data["purchase_orders"][purchase_order_id]["supplier_id"] = new_supplier_id
        return json.dumps(data["purchase_orders"][purchase_order_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "change_supplier_for_purchase_order",
                "description": "Change the supplier for a purchase order. Validates that both the purchase order and new supplier exist.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "purchase_order_id": {
                            "type": "string",
                            "description": "The ID of the purchase order to be updated."
                        },
                        "new_supplier_id": {
                            "type": "string",
                            "description": "The ID of the new supplier to set."
                        }
                    },
                    "required": ["purchase_order_id", "new_supplier_id"]
                }
            }
        }
