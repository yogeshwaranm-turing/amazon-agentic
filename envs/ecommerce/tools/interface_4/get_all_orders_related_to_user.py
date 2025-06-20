import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class GetAllOrdersRelatedToUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        sales_orders = data.get("sales_orders", {})
        sales_order_items = data.get("sales_order_items", {})

        result: List[Dict[str, Any]] = []
        for order in sales_orders.values():
            if order.get("user_id") == user_id:
                order_id = order.get("sales_order_id") or order.get("order_id")
                items = [
                    item for item in sales_order_items.values() 
                    if item.get("sales_order_id") == order_id
                ]
                result.append({
                    "order": order,
                    "order_items": items
                })

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_all_orders_related_to_user",
                "description": "Retrieve all orders and their items for a given user_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user to retrieve orders for."
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
