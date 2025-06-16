import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetAccountDetails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        account_id: str,
        account_type: str
    ) -> str:
        account = data.get("accounts", {}).get(account_id)
        
        if not account:
            # If the account is not found, we raise an exception
            # This is to ensure that the tool behaves correctly when the account does not exist
            raise Exception("NotFound")
        
        # If the account is found, we check if it matches the expected type
        if account.get("account_type") != account_type:
            raise ValueError(f"Account type mismatch: expected {account_type}, got {account.get('account_type')}")
        
        # Ensure the account belongs to the user
        if account.get("user_id") != user_id:
            raise ValueError(f"Account {account_id} does not belong to user {user_id}.")
        
        if not isinstance(account, dict):
            raise ValueError("Account data is not in the expected format.")
        
        return json.dumps(account)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_account_details",
                "description": "Retrieve details for a single account.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string", 
                            "description": "User ID to which the account belongs."
                        },
                        "account_id": {
                            "type": "string", 
                            "description": "Account ID."
                        },
                        "account_type": {
                            "type": "string", 
                            "description": "Type of the account (e.g., checking, savings)."
                        }
                    },
                    "required": ["user_id", "account_id", "account_type"],
                }
            }
        }