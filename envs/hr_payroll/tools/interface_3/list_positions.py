import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ListPositions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        hr_positions = data.get("hr_positions", {})
        return json.dumps(list(hr_positions.values()))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_positions",
                "description": "List all available hr_positions.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
