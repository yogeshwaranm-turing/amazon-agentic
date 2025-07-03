
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateUserAccount(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, email: str, role: str) -> str:
        users = data.setdefault("users", {})
        if any(u.get("email") == email for u in users.values()):
            raise ValueError("Email already exists")

        user_id = str(uuid.uuid4())
        first, *rest = name.split(" ", 1)
        last = rest[0] if rest else ""
        users[user_id] = {
            "first_name": first,
            "last_name": last,
            "email": email,
            "role": role,
            "timezone": "UTC",
            "locale": "en-US",
            "password_hash": "dummyhash",
            "status": "active"
        }

        return json.dumps({"user_id": user_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_user_account",
                "description": "Creates a new user with basic access",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Full name of the user"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email address of the user"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role to assign to the user (e.g., admin, employee)"
                        }
                    },
                    "required": ["name", "email", "role"]
                }
            }
        }
