import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreateUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        first_name: str,
        last_name: str,
        email: str,
        role: str,
        timezone: str,
        locale: str
    ) -> str:
        users = data.setdefault("users", {})

        # Check for unique email
        for user in users.values():
            if user["email"].lower() == email.lower():
                raise ValueError(f"Email '{email}' is already in use.")

        # Validate role
        valid_roles = ["admin", "hr_manager", "payroll", "compliance", "employee", "contractor", "manager"]
        if role not in valid_roles:
            raise ValueError(f"Invalid role '{role}'. Must be one of {valid_roles}")

        # Generate user ID
        def generate_user_id(first_name, last_name):
            base = f"{first_name.lower()}_{last_name.lower()}"
            suffix = 1000
            while f"{base}_{suffix}" in users:
                suffix += 1
            return f"{base}_{suffix}"

        user_id = generate_user_id(first_name, last_name)
        now = datetime.now(timezone.utc).isoformat()

        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "role": role,
            "timezone": timezone,
            "locale": locale,
            "status": "pending",
            "password_hash": "",  # Leave empty for now
            "created_at": now,
            "updated_at": now
        }

        users[user_id] = new_user
        return json.dumps({**new_user, "user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user",
                "description": "Create a new user with auto-generated ID and default fields.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "role": {"type": "string"},
                        "timezone": {"type": "string"},
                        "locale": {"type": "string"}
                    },
                    "required": ["first_name", "last_name", "email", "role", "timezone", "locale"]
                }
            }
        }
