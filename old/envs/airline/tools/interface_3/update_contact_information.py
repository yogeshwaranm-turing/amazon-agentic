import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateContactInformation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        email: str = None,
        phone: str = None,
    ) -> str:
        users = data["users"]
        
        if user_id not in users:
            return "Error: user not found"
          
        user = users[user_id]
        
        if email:
            user["email"] = email
        if phone:
            user["phone"] = phone
            
        return json.dumps({
            "user_id": user_id,
            "email": user.get("email"),
            "phone": user.get("phone")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_contact_information",
                "description": "Update a user's contact information (email and/or phone).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "email":   {"type": "string"},
                        "phone":   {"type": "string"}
                    },
                    "required": ["user_id"]
                }
            }
        }