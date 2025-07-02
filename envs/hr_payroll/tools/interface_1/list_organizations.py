
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOrganizations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        return json.dumps(list(data.get("organizations", {}).values()))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_organizations",
                "description": "Returns all registered organizations with details",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
