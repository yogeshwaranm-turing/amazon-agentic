import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreateAccount(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        user_id: str, 
        account_type: str
    ) -> str:
        accounts = data["accounts"]
        if account_type not in ["checking", "savings"]:
            raise ValueError("Invalid account type. Must be 'checking' or 'savings'.")
        
        # Check if the user exists
        if user_id not in data["users"]:
            raise ValueError(f"User ID {user_id} does not exist.")
        
        # Check if the user already has an account of the same type
        for account in accounts.values():
            if account["user_id"] == user_id and account["account_type"] == account_type and account["status"] == "open":
                raise ValueError(f"User {user_id} already has an open {account_type} account.")
            
        # Generate a new account ID
        if not accounts:
            existing = []
        else:
            existing = [int(a.replace("ACC", "")) for a in accounts.keys() if a.startswith("ACC")]
        
        new_num = max(existing, default=1000000000) + 1
        account_id = f"ACC{new_num}"
        
        record = {
            "account_id": account_id,
            "user_id": user_id,
            "account_type": account_type,
            "status": "open",
            "opened_at": datetime.now(timezone.utc).isoformat(),
            "closed_at": None,
            "currency": "USD",
            "balances": {
                "opening": 0.0,
                "book": 0.0,
                "available": 0.0,
                "closing": None
            },
            "interest_rate": 0.0,
            "interest_accrued": 0.0,
            "last_interest_posted": None,
            "overdraft_limit": 0.0
        }
        
        accounts[account_id] = record
        
        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_account",
                "description": "Create a new checking or savings account for a customer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Customer ID."
                        },
                        "account_type": {
                            "type": "string",
                            "enum": ["checking", "savings"],
                            "description": "Type of account to open."
                        }
                    },
                    "required": ["user_id", "account_type"]
                }
            }
        }