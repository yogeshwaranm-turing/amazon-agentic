import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ChangeShipmentStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], tracking_number: str, status: str) -> str:
        # Validate allowed status values
        allowed_statuses = ["Preparing", "In Transit", "Delivered"]
        if status not in allowed_statuses:
            return f"Error: status must be one of {allowed_statuses}"
        # Retrieve shipment data from shipping.json via data variable
        shipments = data.get("shipping", {})
        # Find shipment record by matching tracking_number instead of sales_order_id
        shipment_key = None
        for key, shipment in shipments.items():
            if shipment.get("tracking_number") == tracking_number:
                shipment_key = key
                break
        if shipment_key is None:
            return "Error: tracking_number not found in shipping"
        # Update shipment status
        shipment = shipments[shipment_key]
        shipment["status"] = status
        shipments[shipment_key] = shipment
        data["shipping"] = shipments
        return json.dumps(shipment)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "change_shipment_status",
                "description": "Change the shipment status of a shipment associated with a sales order based on shipping.json data. Allowed statuses: 'Preparing', 'In Transit', 'Delivered'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tracking_number": {
                            "type": "string",
                            "description": "The tracking number associated with the shipment."
                        },
                        "status": {
                            "type": "string",
                            "description": "New status; allowed values: 'Preparing', 'In Transit', 'Delivered'."
                        }
                    },
                    "required": ["tracking_number", "status"]
                }
            }
        }
