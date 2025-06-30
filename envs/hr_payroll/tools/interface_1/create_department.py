import json
from typing import Any, Dict
from datetime import datetime, timezone
import re
from tau_bench.envs.tool import Tool

class CreateDepartment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        name: str,
        organization_id: str,
        manager_user_id: str = None
    ) -> str:
        organizations = data.get("organizations", {})
        users = data.get("users", {})
        departments = data.setdefault("org_departments", {})

        if organization_id not in organizations:
            raise ValueError(f"Organization ID '{organization_id}' does not exist.")

        if manager_user_id and manager_user_id not in users:
            raise ValueError(f"Manager user ID '{manager_user_id}' not found.")

        # Slug from name + org for ID
        org_slug = re.sub(r'[^a-z0-9]+', '-', organization_id.lower()).strip('-')
        base = f"dept_{org_slug}"
        suffix = 0
        while f"{base}_{suffix}" in departments:
            suffix += 1
        dept_id = f"{base}_{suffix}"

        now = datetime.now(timezone.utc).isoformat()
        new_dept = {
            "name": name,
            "organization_id": organization_id,
            "created_at": now,
            "updated_at": now
        }

        if manager_user_id:
            new_dept["manager_user_id"] = manager_user_id

        departments[dept_id] = new_dept
        return json.dumps({**new_dept, "department_id": dept_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_department",
                "description": "Create a department within an organization with optional manager.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Department name."
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "ID of the parent organization."
                        },
                        "manager_user_id": {
                            "type": "string",
                            "description": "Optional manager user ID for department."
                        }
                    },
                    "required": ["name", "organization_id"]
                }
            }
        }
