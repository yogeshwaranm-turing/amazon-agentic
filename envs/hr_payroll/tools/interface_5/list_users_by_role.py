import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ListUsersByRole(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], role: str) -> str:
        users = data.get("users", {})
        allowed_roles = ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"]
        if role not in allowed_roles:
            raise ValueError(f"Role '{role}' is invalid. Must be one of: {allowed_roles}")

        filtered_users: List[Dict[str, Any]] = [
            u for u in users.values() if u.get("role") == role
        ]
        return json.dumps(filtered_users)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_users_by_role",
                "description": "Retrieve all users with a specific platform role.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "enum": ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"],
                            "description": "The user role to filter on."
                        }
                    },
                    "required": ["role"]
                }
            }
        }
