import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOrganizations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        workers = data.get("workers", {})
        organizations = data.get("organizations", {})

        org_ids = {
            w["organization_id"]
            for w in workers.values()
            if w.get("user_id") == user_id
        }

        matched_orgs = [
            org for oid, org in organizations.items()
            if oid in org_ids
        ]
        return json.dumps(matched_orgs)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_organizations",
                "description": "Returns organizations associated with a specific user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose associated organizations are to be listed"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
