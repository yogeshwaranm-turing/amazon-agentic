import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListPurchaseOrderBySupplier(Tool):
    @staticmethod
    def invoke(
            data: Dict[str, Any],
            supplier_id: str
    ) -> str:
        """
        List all purchase orders for a given supplier.
        - Filters purchase orders by supplier_id.
        - Returns the filtered list as a JSON string.
        """
        purchase_orders = data.get("purchase_orders", {})
        filtered_orders = [order for order in purchase_orders.values() if order.get("supplier_id") == supplier_id]
        return json.dumps(filtered_orders)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_purchase_order_by_supplier",
                "description": "List all purchase orders for a specified supplier.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {
                            "type": "string",
                            "description": "The ID of the supplier whose purchase orders need to be listed."
                        }
                    },
                    "required": ["supplier_id"]
                }
            }
        }
