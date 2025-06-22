import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateAccountStatus(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        account_id: str,
        new_status: str,
        reason: str = None
    ) -> str:
        accounts = data.get("accounts", {})
        
        if account_id not in accounts:
            raise ValueError(f"Account {account_id} not found.")
        
        account = accounts[account_id]
        old_status = account.get("status")
        
        # Validate status transitions
        valid_transitions = {
            "open": ["frozen", "closed"],
            "frozen": ["open", "closed"],
            "closed": []  # Cannot change from closed
        }
        
        if old_status not in valid_transitions:
            raise ValueError(f"Invalid current status: {old_status}")
        
        if new_status not in valid_transitions[old_status]:
            raise ValueError(f"Cannot transition from {old_status} to {new_status}")
        
        # Update account status
        account["status"] = new_status
        account["status_updated_at"] = datetime.now().isoformat() + "Z"
        
        if reason:
            account["status_reason"] = reason
        
        # Handle specific status changes
        if new_status == "frozen":
            account["frozen_at"] = datetime.now().isoformat() + "Z"
            # When frozen, available balance becomes 0 but book balance remains
            account["balances"]["available"] = 0.0
        elif new_status == "open" and old_status == "frozen":
            account["unfrozen_at"] = datetime.now().isoformat() + "Z"
            # Restore available balance from book balance
            account["balances"]["available"] = account["balances"]["book"]
        elif new_status == "closed":
            account["closed_at"] = datetime.now().isoformat() + "Z"
            # Zero out all balances
            remaining_balance = account["balances"]["available"]
            account["balances"]["closing"] = remaining_balance
            account["balances"]["available"] = 0.0
            account["balances"]["book"] = 0.0
        
        return json.dumps(account)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_account_status",
                "description": "Change account status (open → frozen → closed) with proper validation and audit trails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string"},
                        "new_status": {"type": "string", "enum": ["open", "frozen", "closed"]},
                        "reason": {"type": "string"}
                    },
                    "required": ["account_id", "new_status"]
                }
            }
        }
