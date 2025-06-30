import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ListOrganizations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        organizations = data.get("organizations", {})
        return json.dumps(list(organizations.values()))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_organizations",
                "description": "List all registered organizations.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
