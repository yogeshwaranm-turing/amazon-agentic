import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ModifyShipmentMethod(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], identifier: str, new_shipment_method: str) -> str:
        # Validate allowed shipment methods
        allowed_methods = ["Standard", "Express"]
        if new_shipment_method not in allowed_methods:
            return f"Error: shipment_method must be one of {allowed_methods}"
        # Retrieve shipment data from shipping.json via data variable
        shipments = data.get("shipping", {})
        shipment_key = None
        shipment_record = None
        # Find shipment record by matching tracking_number or sales_order_id
        for key, shipment in shipments.items():
            if shipment.get("tracking_number") == identifier or shipment.get("sales_order_id") == identifier:
                shipment_key = key
                shipment_record = shipment
                break
        if shipment_record is None:
            return "Error: identifier not found in shipping"
        # Check if the new shipment method is different from the current one
        current_method = shipment_record.get("method")
        if current_method == new_shipment_method:
            return "Error: new shipment method must be different from the current one"
        # Update shipment method
        shipment_record["method"] = new_shipment_method
        shipments[shipment_key] = shipment_record
        data["shipping"] = shipments
        return json.dumps(shipment_record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "modify_shipment_method",
                "description": ("Modify the shipment method of a shipment by tracking number or sales order id. "
                                "Allowed shipment methods: 'Standard' and 'Express'. "
                                "The new shipment method must be different from the current one."),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "identifier": {
                            "type": "string",
                            "description": "The tracking number or sales order id associated with the shipment."
                        },
                        "new_shipment_method": {
                            "type": "string",
                            "description": "The new shipment method; allowed values: 'Standard' and 'Express'."
                        }
                    },
                    "required": ["identifier", "new_shipment_method"]
                }
            }
        }
