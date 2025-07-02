
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RegisterNewOrganization(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, timezone: str, region: str) -> str:
        orgs = data.setdefault("organizations", {})
        if any(o.get("name") == name and o.get("country") == region for o in orgs.values()):
            raise ValueError("Organization with same name and region already exists")

        org_id = str(uuid.uuid4())
        orgs[org_id] = {
            "name": name,
            "country": region,
            "timezone": timezone,
            "address": {}
        }

        return json.dumps({"organization_id": org_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "register_new_organization",
                "description": "Adds a new organization to the system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Organization name"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Organization's timezone"
                        },
                        "region": {
                            "type": "string",
                            "description": "Region or country of operation"
                        }
                    },
                    "required": ["name", "timezone", "region"]
                }
            }
        }
