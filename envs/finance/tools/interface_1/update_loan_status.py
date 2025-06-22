import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class UpdateLoanStatus(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        loan_id: str,
        new_status: str,
        reason: str = None
    ) -> str:
        loans = data.get("loans", {})
        
        if loan_id not in loans:
            raise ValueError(f"Loan {loan_id} not found.")
        
        loan = loans[loan_id]
        old_status = loan.get("status")
        
        # Validate status transition
        valid_transitions = {
            "active": ["paid_off", "defaulted", "suspended"],
            "suspended": ["active", "defaulted"],
            "defaulted": ["active"],  # Recovery scenario
            "paid_off": []  # Cannot change from paid_off
        }
        
        if old_status not in valid_transitions:
            raise ValueError(f"Invalid current status: {old_status}")
        
        if new_status not in valid_transitions[old_status]:
            raise ValueError(f"Cannot transition from {old_status} to {new_status}")
        
        # Update loan status
        loan["status"] = new_status
        loan["status_updated_at"] = datetime.now().isoformat() + "Z"
        
        if reason:
            loan["status_reason"] = reason
        
        # Handle specific status changes
        if new_status == "paid_off":
            loan["outstanding_balance"] = 0.0
            loan["next_payment_due"] = None
            loan["paid_off_at"] = datetime.now().isoformat() + "Z"
        elif new_status == "defaulted":
            loan["defaulted_at"] = datetime.now().isoformat() + "Z"
        
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_loan_status",
                "description": "Update loan status with proper validation and status transitions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "loan_id": {"type": "string"},
                        "new_status": {"type": "string", "enum": ["active", "paid_off", "defaulted", "suspended"]},
                        "reason": {"type": "string"}
                    },
                    "required": ["loan_id", "new_status"]
                }
            }
        }
