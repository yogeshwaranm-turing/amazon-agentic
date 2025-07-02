import os
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ConfirmShipmentForOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str) -> str:
        sales_orders = data.get("sales_orders", {})
        if order_id not in sales_orders:
            return "Error: order_id not found in sales_orders"
        order = sales_orders[order_id]
        if order.get("status") != "Confirmed":
            return f"Error: order status is not 'Confirmed', current status: {order.get('status')}"
        order["status"] = "Shipped"
        sales_orders[order_id] = order
        data["sales_orders"] = sales_orders
        return json.dumps(order)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "confirm_shipment_for_order",
                "description": "Confirm shipment for an order by updating the status from 'Confirmed' to 'Shipped'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order id for which the shipment is being confirmed."
                        }
                    },
                    "required": ["order_id"]
                }
            }
        }
