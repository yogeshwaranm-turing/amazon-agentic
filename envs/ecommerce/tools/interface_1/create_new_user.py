import json
import re
from tau_bench.envs.tool import Tool

class CreateNewUser(Tool):
    @staticmethod
    def invoke(
        data: dict,
        first_name: str,
        last_name: str,
        email: str,
        address: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
    ) -> str:
        # Validate email format using a regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Error: invalid email format"
        # Check if email already exists among users
        for user in data.get("users", {}).values():
            if user.get("email") == email:
                return "Error: email already exists"
        # Auto-generate new user_id in format USRxxx
        users = data.setdefault("users", {})
        if users:
            max_id = max(int(uid[3:]) for uid in users.keys() if uid.startswith("USR"))
            new_id_num = max_id + 1
        else:
            new_id_num = 1
        new_user_id = f"USR{str(new_id_num).zfill(3)}"
        # Create new user record
        new_user = {
            "user_id": new_user_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "country": country,
            "orders": []
        }
        users[new_user_id] = new_user
        return json.dumps(new_user)

    @staticmethod
    def get_info() -> dict:
        return {
            "type": "function",
            "function": {
                "name": "create_new_user",
                "description": "Create a new user with auto-incremented user_id and verified email format.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string", "description": "Must be a valid email."},
                        "address": {"type": "string"},
                        "city": {"type": "string"},
                        "state": {"type": "string"},
                        "zip_code": {"type": "string"},
                        "country": {"type": "string"}
                    },
                    "required": ["first_name", "last_name", "email", "address", "city", "state", "zip_code", "country"]
                }
            }
        }
