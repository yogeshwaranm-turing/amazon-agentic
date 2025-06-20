import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateShippingAddress(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], identifier: str, new_address: str) -> str:
        shipments = data.get("shipping", {})
        shipment_key = None
        shipment_record = None
        # Find shipment by matching tracking_number or sales_order_id
        for key, shipment in shipments.items():
            if shipment.get("tracking_number") == identifier or shipment.get("sales_order_id") == identifier:
                shipment_key = key
                shipment_record = shipment
                break
        if shipment_record is None:
            return "Error: identifier not found in shipping"
        # Update shipping address
        shipment_record["address"] = new_address
        shipments[shipment_key] = shipment_record
        data["shipping"] = shipments
        return json.dumps(shipment_record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_shipping_address",
                "description": "Update the shipping address for a shipment using tracking_number or sales_order_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "identifier": {
                            "type": "string",
                            "description": "The tracking number or sales order id associated with the shipment."
                        },
                        "new_address": {
                            "type": "string",
                            "description": "The new shipping address."
                        }
                    },
                    "required": ["identifier", "new_address"]
                }
            }
        }
