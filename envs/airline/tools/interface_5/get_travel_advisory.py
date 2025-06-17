import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetTravelAdvisory(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
    ) -> str:
        advisories: List[Dict[str, Any]] = [
            {"id": "TA1", "region": "Europe", "message": "Schengen visa requirements updated."},
            {"id": "TA2", "region": "North America", "message": "TSA security wait times may exceed 60 minutes."},
            {"id": "TA3", "region": "Asia", "message": "Typhoon warnings in Tokyo region."},
        ]
        return json.dumps(advisories)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_travel_advisory",
                "description": "Retrieve current global travel advisories.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }