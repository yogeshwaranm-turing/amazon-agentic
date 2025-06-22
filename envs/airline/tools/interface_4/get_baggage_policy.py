import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetBaggagePolicy(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
    ) -> str:
        policy: Dict[str, Any] = {
            "basic_economy": {"free": 1, "weight_limit_kg": 20},
            "economy":       {"free": 2, "weight_limit_kg": 23},
            "business":      {"free": 3, "weight_limit_kg": 32},
        }
        return json.dumps(policy)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_baggage_policy",
                "description": "Retrieve the baggage allowance policy for each cabin class.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }