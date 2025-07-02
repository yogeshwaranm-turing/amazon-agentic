import os
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetShipmentInformationByTrackingNumber(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], tracking_number: str) -> str:
        shipments = data.get("shipping", {})
        for key, record in shipments.items():
            if record.get("tracking_number") == tracking_number:
                return json.dumps(record)
        return "Error: shipment for the given tracking number not found"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_shipment_information_by_tracking_number",
                "description": "Retrieve the shipment information from shipping.json based on the provided tracking number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tracking_number": {
                            "type": "string",
                            "description": "The tracking number for which shipment information is requested."
                        }
                    },
                    "required": ["tracking_number"]
                }
            }
        }

