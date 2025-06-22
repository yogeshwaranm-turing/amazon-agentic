import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class ConsolidateUserAccounts(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        primary_account_id: str,
        accounts_to_consolidate: list
    ) -> str:
        accounts = data.get("accounts", {})
        users = data.get("users", {})
        
        # Validate user exists
        if user_id not in users:
            raise ValueError(f"User {user_id} not found.")
        
        # Validate primary account
        if primary_account_id not in accounts:
            raise ValueError(f"Primary account {primary_account_id} not found.")
        
        primary_account = accounts[primary_account_id]
        if primary_account.get("user_id") != user_id:
            raise ValueError(f"Primary account {primary_account_id} does not belong to user {user_id}")
        
        if primary_account.get("status") != "open":
            raise ValueError(f"Primary account {primary_account_id} is not open")
        
        # Validate accounts to consolidate
        total_balance_transferred = 0.0
        consolidated_accounts = []
        
        for acc_id in accounts_to_consolidate:
            if acc_id not in accounts:
                raise ValueError(f"Account {acc_id} not found.")
            
            account = accounts[acc_id]
            
            # Validate ownership
            if account.get("user_id") != user_id:
                raise ValueError(f"Account {acc_id} does not belong to user {user_id}")
            
            # Skip if already closed or the primary account
            if account.get("status") == "closed" or acc_id == primary_account_id:
                continue
            
            # Get available balance
            available_balance = account.get("balances", {}).get("available", 0)
            
            if available_balance > 0:
                # Transfer balance to primary account
                primary_account["balances"]["available"] += available_balance
                primary_account["balances"]["book"] += available_balance
                total_balance_transferred += available_balance
                
                # Record consolidation details
                account["consolidated_to"] = primary_account_id
                account["consolidated_at"] = datetime.now().isoformat() + "Z"
                account["consolidated_balance"] = available_balance
            
            # Close the account
            account["status"] = "closed"
            account["closed_at"] = datetime.now().isoformat() + "Z"
            account["closure_reason"] = "Account consolidation"
            account["balances"]["available"] = 0.0
            account["balances"]["book"] = 0.0
            account["balances"]["closing"] = available_balance
            
            consolidated_accounts.append({
                "account_id": acc_id,
                "account_type": account.get("account_type"),
                "balance_transferred": available_balance,
                "closed_at": account["closed_at"]
            })
        
        # Update primary account with consolidation info
        primary_account["consolidation_history"] = primary_account.get("consolidation_history", [])
        primary_account["consolidation_history"].append({
            "consolidated_at": datetime.now().isoformat() + "Z",
            "accounts_consolidated": len(consolidated_accounts),
            "total_balance_received": total_balance_transferred,
            "consolidated_account_ids": accounts_to_consolidate
        })
        
        result = {
            "user_id": user_id,
            "primary_account_id": primary_account_id,
            "consolidated_accounts": consolidated_accounts,
            "total_balance_transferred": total_balance_transferred,
            "new_primary_balance": primary_account["balances"]["available"],
            "consolidation_date": datetime.now().isoformat() + "Z"
        }
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "consolidate_user_accounts",
                "description": "Merge multiple accounts for a single user, combining balances and closing duplicate accounts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "primary_account_id": {"type": "string"},
                        "accounts_to_consolidate": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["user_id", "primary_account_id", "accounts_to_consolidate"]
                }
            }
        }
