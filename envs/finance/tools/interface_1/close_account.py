import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class CloseAccount(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        account_id: str,
        transfer_to_account_id: str = None,
        reason: str = None
    ) -> str:
        accounts = data.get("accounts", {})
        
        if account_id not in accounts:
            raise ValueError(f"Account {account_id} not found.")
        
        account = accounts[account_id]
        
        # Validate account can be closed
        if account.get("status") != "open":
            raise ValueError(f"Account {account_id} is not open. Current status: {account.get('status')}")
        
        remaining_balance = account.get("balances", {}).get("available", 0)
        
        # Handle remaining balance
        if remaining_balance > 0:
            if not transfer_to_account_id:
                raise ValueError(f"Account has remaining balance of ${remaining_balance}. Must specify transfer_to_account_id.")
            
            if transfer_to_account_id not in accounts:
                raise ValueError(f"Transfer destination account {transfer_to_account_id} not found.")
            
            destination_account = accounts[transfer_to_account_id]
            
            # Validate destination account
            if destination_account.get("status") != "open":
                raise ValueError(f"Destination account {transfer_to_account_id} is not open.")
            
            if destination_account.get("user_id") != account.get("user_id"):
                raise ValueError("Can only transfer to accounts owned by the same user.")
            
            # Transfer balance
            destination_account["balances"]["available"] += remaining_balance
            destination_account["balances"]["book"] += remaining_balance
            
            # Record transfer
            account["final_balance_transferred_to"] = transfer_to_account_id
            account["final_balance_amount"] = remaining_balance
        
        # Close the account
        account["status"] = "closed"
        account["closed_at"] = datetime.now().isoformat() + "Z"
        account["closure_reason"] = reason or "Customer request"
        
        # Zero out balances
        account["balances"]["available"] = 0.0
        account["balances"]["book"] = 0.0
        account["balances"]["closing"] = remaining_balance
        
        return json.dumps(account)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "close_account",
                "description": "Close an account, setting status to closed and transferring remaining balance if specified.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string"},
                        "transfer_to_account_id": {"type": "string"},
                        "reason": {"type": "string"}
                    },
                    "required": ["account_id"]
                }
            }
        }
