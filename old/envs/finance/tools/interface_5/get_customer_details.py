import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetCustomerDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        user_id: str = None, 
        email: str = None
    ) -> str:
        users = data["users"]
        
        if user_id:
            user = users[user_id]
            if not user:
                raise Exception("NotFound")
            return json.dumps(user)
        
        if email:
            for u in users.values():
                if u.get("email") == email:
                    return json.dumps(u)
            raise Exception("NotFound")
        
        raise Exception("Either user_id or email must be provided")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_customer_details",
                "description": "Fetch a customer profile by user_id or email.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Customer ID, e.g., CUST123456."
                        },
                        "email": {
                            "type": "string",
                            "description": "Customer email address."
                        }
                    },
                    "required": []
                }
            }
        }