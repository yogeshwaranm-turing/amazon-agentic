import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateUserProfile(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        role: str = None,
        timezone: str = None,
        locale: str = None
    ) -> str:
        users = data.get("users", {})

        if user_id not in users:
            raise ValueError(f"User '{user_id}' not found.")

        user = users[user_id]

        if email and email != user["email"]:
            # Ensure new email is unique
            for uid, u in users.items():
                if u["email"].lower() == email.lower() and uid != user_id:
                    raise ValueError(f"Email '{email}' is already in use.")

        allowed_roles = ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"]
        if role and role not in allowed_roles:
            raise ValueError(f"Invalid role: '{role}'. Allowed values: {allowed_roles}")

        if first_name: user["first_name"] = first_name
        if last_name: user["last_name"] = last_name
        if email: user["email"] = email
        if role: user["role"] = role
        if timezone: user["timezone"] = timezone
        if locale: user["locale"] = locale

        user["updated_at"] = "2025-06-30T09:25:07.650972Z"
        return json.dumps(user)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_user_profile",
                "description": "Update basic details of an existing user including role, email, or timezone.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user to update."
                        },
                        "first_name": {
                            "type": "string",
                            "description": "Updated first name (optional)."
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Updated last name (optional)."
                        },
                        "email": {
                            "type": "string",
                            "description": "New unique email address (optional)."
                        },
                        "role": {
                            "type": "string",
                            "enum": ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"],
                            "description": "Role to assign (optional)."
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Updated timezone (optional)."
                        },
                        "locale": {
                            "type": "string",
                            "description": "Updated locale (optional)."
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
