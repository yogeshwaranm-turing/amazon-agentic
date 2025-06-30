import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AssignDepartmentManager(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department: str, user_id: str) -> str:
        users = data.get("users", {})
        org_departments = data.setdefault("org_departments", {})

        if user_id not in users:
            raise ValueError(f"User '{user_id}' not found.")

        role = users[user_id].get("role")
        if role not in ["manager", "admin", "hr_manager"]:
            raise ValueError(f"User '{user_id}' is not eligible to manage a department. Role must be manager or above.")

        org_departments[department] = {
            "manager_user_id": user_id,
            "updated_at": "2025-06-30T09:25:07.684401Z"
        }
        return json.dumps({"department": department, "manager": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_department_manager",
                "description": "Assign a user as manager of a department (must be admin/hr_manager/manager).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "department": {"type": "string", "description": "Name of the department."},
                        "user_id": {"type": "string", "description": "User ID of the department manager."}
                    },
                    "required": ["department", "user_id"]
                }
            }
        }
