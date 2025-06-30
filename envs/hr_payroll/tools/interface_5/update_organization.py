import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateOrganization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        organization_id: str,
        name: str = None,
        country: str = None,
        timezone: str = None,
        address: Dict[str, Any] = None
    ) -> str:
        organizations = data.get("organizations", {})
        if organization_id not in organizations:
            raise ValueError(f"Organization '{organization_id}' not found.")

        org = organizations[organization_id]
        if name: org["name"] = name
        if country: org["country"] = country
        if timezone: org["timezone"] = timezone
        if address: org["address"] = address

        org["updated_at"] = "2025-06-30T09:25:07.734513Z"
        return json.dumps(org)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_organization",
                "description": "Update details of an existing organization.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {"type": "string", "description": "ID of the organization to update."},
                        "name": {"type": "string", "description": "New name, if updating."},
                        "country": {"type": "string", "description": "New country, if updating."},
                        "timezone": {"type": "string", "description": "New timezone, if updating."},
                        "address": {
                            "type": "object",
                            "description": "New address details in JSON format (optional)."
                        }
                    },
                    "required": ["organization_id"]
                }
            }
        }
