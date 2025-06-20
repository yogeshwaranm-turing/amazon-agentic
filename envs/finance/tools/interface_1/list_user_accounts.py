import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListUserAccounts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        user_id: str
    ) -> str:
        accounts = data["accounts"]
        
        # Validate user_id
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        
        # Filter accounts by user_id
        result = [a for a in accounts.values() if a.get("user_id") == user_id]
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_user_accounts",
                "description": "List all accounts for a given customer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string", 
                            "description": "Customer ID."
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }