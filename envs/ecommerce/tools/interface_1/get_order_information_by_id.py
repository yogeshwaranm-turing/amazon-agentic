import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetOrderInformationById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str) -> str:
        if order_id not in data.get("sales_orders", {}):
            return json.dumps({"error": "Order id not found"})
        order = data["sales_orders"][order_id]
        order_items = [
            item for item in data.get("sales_order_items", {}).values()
            if item.get("sales_order_id") == order_id
        ]
        return json.dumps({"order": order, "order_items": order_items})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_order_information_by_id",
                "description": "Return order information and related sales order items given an order id",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "Sales order id"
                        }
                    },
                    "required": ["order_id"]
                }
            }
        }
