import os
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetShipmentInformationByOrderId(Tool):
    @staticmethod
    def invoke(data: dict, order_id: str) -> str:
        # Use shipping data from the provided data dictionary instead of loading it here
        shipments = data.get("shipping", {})
        shipment = None
        for key, record in shipments.items():
            if record.get("sales_order_id") == order_id:
                shipment = record
                break
        if shipment is None:
            return "Error: shipment for the given order_id not found"
        return json.dumps(shipment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_shipment_information_by_order_id",
                "description": "Retrieve the shipment information from shipping.json based on the provided order_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The order id for which the shipment is requested."
                        }
                    },
                    "required": ["order_id"]
                }
            }
        }

