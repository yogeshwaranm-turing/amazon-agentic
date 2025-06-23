import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteLoan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        loan_id: str,
        reason: str
    ) -> str:
        loans = data.get("loans", {})
        
        if loan_id not in loans:
            raise ValueError(f"Loan {loan_id} not found.")
        
        loan = loans[loan_id]
        
        # Only allow deletion of loans that haven't been disbursed or are cancelled
        allowed_statuses = ["pending", "cancelled"]
        current_status = loan.get("status")
        
        if current_status not in allowed_statuses:
            raise ValueError(f"Cannot delete loan with status '{current_status}'. Only loans with status 'pending' or 'cancelled' can be deleted.")
        
        # Verify no payments have been made
        if loan.get("total_paid", 0) > 0:
            raise ValueError("Cannot delete loan that has received payments.")
        
        # Store deleted loan info for audit
        deleted_loan = {
            "deleted_loan": loan.copy(),
            "deleted_at": "2025-06-22T00:00:00Z",
            "deletion_reason": reason
        }
        
        # Remove loan from active loans
        del loans[loan_id]
        
        return json.dumps(deleted_loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_loan",
                "description": "Delete a loan record for cancelled or voided loans before disbursement.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "loan_id": {"type": "string"},
                        "reason": {"type": "string"}
                    },
                    "required": ["loan_id", "reason"]
                }
            }
        }
