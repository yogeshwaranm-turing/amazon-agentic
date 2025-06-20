import os
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ConfirmPayment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], sales_order_id: str) -> str:
        sales_orders = data.get("sales_orders", {})
        if sales_order_id not in sales_orders:
            return "Error: sales_order_id not found in sales_orders"
        order = sales_orders[sales_order_id]
        if order.get("status") != "Pending":
            return f"Error: order status is not 'Pending', current status: {order.get('status')}"
        order["status"] = "Confirmed"
        sales_orders[sales_order_id] = order
        data["sales_orders"] = sales_orders
        return json.dumps(order)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "confirm_payment",
                "description": "Confirm payment for a sales order by updating the status from 'Pending' to 'Confirmed'. Throws error if the status is not 'Pending'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sales_order_id": {
                            "type": "string",
                            "description": "The sales order id to confirm payment for."
                        }
                    },
                    "required": ["sales_order_id"]
                }
            }
        }
