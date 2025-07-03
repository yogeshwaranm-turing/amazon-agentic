import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListOnboardServices(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
    ) -> str:
        services: List[Dict[str, Any]] = [
            {"service": "WiFi", "price": 10},
            {"service": "In-seat Power", "price": 0},
            {"service": "Extra Legroom", "price": 25},
            {"service": "Headphones Rental", "price": 5},
        ]
        return json.dumps(services)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_onboard_services",
                "description": "List purchasable onboard services and their prices.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }