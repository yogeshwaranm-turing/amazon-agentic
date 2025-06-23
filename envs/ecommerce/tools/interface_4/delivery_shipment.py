import os
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeliveryShipment(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], tracking_number: str) -> str:
        shipments = data.get("shipping", {})
        shipment_key = None
        shipment_record = None
        for key, shipment in shipments.items():
            if shipment.get("tracking_number") == tracking_number:
                shipment_key = key
                shipment_record = shipment
                break
        if shipment_record is None:
            return "Error: tracking number not found in shipping"
        
        if shipment_record.get("status") != "In Transit":
            return f"Error: shipment status is not 'In Transit', current status: {shipment_record.get('status')}"
        
        order_id = shipment_record.get("sales_order_id")
        if not order_id:
            return "Error: shipment record does not contain an order_id"
        
        sales_orders = data.get("sales_orders", {})
        if order_id not in sales_orders:
            return "Error: order_id not found in sales_orders"
        
        order = sales_orders[order_id]
        if order.get("status") != "Shipped":
            return f"Error: order status is not 'Shipped', current status: {order.get('status')}"
        
        order["status"] = "Delivered"
        sales_orders[order_id] = order
        
        shipment_record["status"] = "Delivered"
        shipments[shipment_key] = shipment_record

        return json.dumps({
            "order": order,
            "shipment": shipment_record
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delivery_shipment",
                "description": "Deliver the shipment: finds the order based on tracking_number if shipment status is 'In Transit' and order is 'Shipped', then updates both to 'Delivered'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tracking_number": {
                            "type": "string",
                            "description": "The tracking number associated with the shipment."
                        }
                    },
                    "required": ["tracking_number"]
                }
            }
        }

