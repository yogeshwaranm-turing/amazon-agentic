import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool
import re

class CreateOrganization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        country: str,
        timezone: str,
        address: Dict[str, Any]
    ) -> str:
        organizations = data.setdefault("organizations", {})

        # Validate name uniqueness
        for org in organizations.values():
            if org["name"].lower() == name.lower():
                raise ValueError(f"Organization name '{name}' already exists.")

        # Validate address
        for field in ["line1", "city", "zip"]:
            if field not in address:
                raise ValueError(f"Address missing required field '{field}'.")

        # Generate organization ID from name
        slug_base = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-').replace(" ", "_")
        suffix = 1000
        while f"{slug_base}_{suffix}" in organizations:
            suffix += 1
        org_id = f"{slug_base}_{suffix}"

        now = datetime.now(timezone.utc).isoformat()

        organization = {
            "name": name,
            "country": country,
            "timezone": timezone,
            "address": address,
            "created_at": now,
            "updated_at": now
        }

        organizations[org_id] = organization
        return json.dumps({**organization, "organization_id": org_id})

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
                        "name": {
                            "type": "string",
                            "description": "Name of the organization."
                        },
                        "country": {
                            "type": "string",
                            "description": "Country of legal operation."
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone of primary office."
                        },
                        "address": {
                            "type": "object",
                            "properties": {
                                "line1": {"type": "string"},
                                "city": {"type": "string"},
                                "zip": {"type": "string"}
                            },
                            "required": ["line1", "city", "zip"]
                        }
                    },
                    "required": ["name", "country", "timezone", "address"]
                }
            }
        }
