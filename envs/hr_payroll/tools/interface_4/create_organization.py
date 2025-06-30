import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateOrganization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        organization_id: str,
        name: str,
        country: str,
        timezone: str,
        address: Dict[str, Any]
    ) -> str:
        organizations = data.setdefault("organizations", {})

        if organization_id in organizations:
            raise ValueError(f"Organization ID '{organization_id}' already exists.")

        organization = {
            "organization_id": organization_id,
            "name": name,
            "country": country,
            "timezone": timezone,
            "address": address,
            "created_at": "2025-06-30T09:25:07.713867Z",
            "updated_at": "2025-06-30T09:25:07.713867Z"
        }

        organizations[organization_id] = organization
        return json.dumps(organization)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_organization",
                "description": "Create a new organization profile including location and timezone.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {"type": "string", "description": "Unique identifier for the organization."},
                        "name": {"type": "string", "description": "Name of the organization."},
                        "country": {"type": "string", "description": "Country of legal operation."},
                        "timezone": {"type": "string", "description": "Timezone of primary office."},
                        "address": {
                            "type": "object",
                            "description": "Structured address in JSON format (line1, city, zip, etc.)."
                        }
                    },
                    "required": ["organization_id", "name", "country", "timezone", "address"]
                }
            }
        }
