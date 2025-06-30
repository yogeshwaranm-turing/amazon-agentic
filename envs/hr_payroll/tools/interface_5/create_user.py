import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        role: str,
        timezone: str,
        locale: str
    ) -> str:
        users = data.setdefault("users", {})

        if user_id in users:
            raise ValueError(f"User ID '{user_id}' already exists.")

        # Check for unique email
        for u in users.values():
            if u["email"].lower() == email.lower():
                raise ValueError(f"Email '{email}' is already in use.")

        # Validate role enum
        allowed_roles = ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"]
        if role not in allowed_roles:
            raise ValueError(f"Role '{role}' is not valid. Must be one of: {allowed_roles}")

        user_record = {
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "timezone": timezone,
            "locale": locale,
            "status": "active",
            "created_at": "2025-06-30T09:25:07.725617Z",
            "updated_at": "2025-06-30T09:25:07.725617Z"
        }

        users[user_id] = user_record
        return json.dumps(user_record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new platform user with validations for email uniqueness and role enforcement.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "A unique identifier for the user, globally scoped."
                        },
                        "first_name": {
                            "type": "string",
                            "description": "The user's first name."
                        },
                        "last_name": {
                            "type": "string",
                            "description": "The user's last name."
                        },
                        "email": {
                            "type": "string",
                            "description": "The user's primary email address, must be unique across the platform."
                        },
                        "role": {
                            "type": "string",
                            "enum": ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"],
                            "description": "The user's role in the system, which governs access and capabilities."
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone ID (e.g. 'Asia/Kolkata', 'UTC') used for localizing actions and deadlines."
                        },
                        "locale": {
                            "type": "string",
                            "description": "User's preferred language/region setting (e.g. 'en-US', 'fr-FR')."
                        }
                    },
                    "required": ["user_id", "first_name", "last_name", "email", "role", "timezone", "locale"]
                }
            }
        }
