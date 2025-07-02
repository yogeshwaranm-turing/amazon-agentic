import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateAccount(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        account_type: str,
        initial_deposit: float,
        currency: str = "USD"
    ) -> str:
        users = data.get("users", {})
        accounts = data.setdefault("accounts", {})
        
        # Validate user exists
        if user_id not in users:
            raise ValueError(f"User {user_id} not found.")
        
        # Validate account type
        valid_types = ["checking", "savings"]
        if account_type not in valid_types:
            raise ValueError(f"Invalid account type. Must be one of: {valid_types}")
        
        # Validate minimum deposit
        min_deposits = {"checking": 25.0, "savings": 100.0}
        if initial_deposit < min_deposits[account_type]:
            raise ValueError(f"Minimum deposit for {account_type} account is ${min_deposits[account_type]}")
        
        # Generate account ID
        # Generate account ID with a deterministic format
        account_id = f"ACC{user_id[-6:]}{account_type[:3].upper()}"
        
        # Set interest rate based on account type
        interest_rate = 0.01 if account_type == "checking" else 1.5
        
        # Create account record
        account = {
            "account_id": account_id,
            "user_id": user_id,
            "account_type": account_type,
            "status": "open",
            "opened_at": "2025-01-01T00:00:00Z",
            "closed_at": None,
            "currency": currency,
            "balances": {
                "opening": initial_deposit,
                "book": initial_deposit,
                "available": initial_deposit,
                "closing": None
            },
            "interest_rate": interest_rate,
            "interest_accrued": 0.0,
            "last_interest_posted": None,
            "overdraft_limit": 500.0 if account_type == "checking" else None
        }
        
        accounts[account_id] = account
        return json.dumps(account)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_account",
                "description": "Create new checking or savings account for existing users with initial deposit requirements.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "account_type": {"type": "string", "enum": ["checking", "savings"]},
                        "initial_deposit": {"type": "number"},
                        "currency": {"type": "string"}
                    },
                    "required": ["user_id", "account_type", "initial_deposit"]
                }
            }
        }
