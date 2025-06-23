import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class ProcessLoanPayment(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        loan_id: str,
        payment_amount: float,
        payment_date: str = None
    ) -> str:
        loans = data.get("loans", {})
        
        if loan_id not in loans:
            raise ValueError(f"Loan {loan_id} not found.")
        
        loan = loans[loan_id]
        
        # Validate loan status
        if loan.get("status") != "active":
            raise ValueError(f"Cannot process payment for loan with status: {loan.get('status')}")
        
        # Use current date if not provided
        if not payment_date:
            payment_date = "2025-01-01T00:00:00Z"
        
        # Calculate interest and principal portions
        outstanding_balance = loan.get("outstanding_balance", 0)
        interest_rate = loan.get("interest_rate", 0) / 100 / 12  # Monthly rate
        interest_portion = outstanding_balance * interest_rate
        principal_portion = max(0, payment_amount - interest_portion)
        
        # Update loan record
        new_outstanding_balance = max(0, outstanding_balance - principal_portion)
        total_paid = loan.get("total_paid", 0) + payment_amount
        
        loan["outstanding_balance"] = new_outstanding_balance
        loan["total_paid"] = total_paid
        loan["last_payment_at"] = payment_date
        loan["last_payment_amount"] = payment_amount
        loan["last_payment_interest"] = interest_portion
        loan["last_payment_principal"] = principal_portion
        
        # Calculate next payment due date
        payment_frequency = loan.get("payment_frequency", "monthly")
        if payment_frequency == "monthly":
            next_due = datetime.fromisoformat(payment_date.replace("Z", "")) + timedelta(days=30)
        elif payment_frequency == "quarterly":
            next_due = datetime.fromisoformat(payment_date.replace("Z", "")) + timedelta(days=90)
        else:  # annually
            next_due = datetime.fromisoformat(payment_date.replace("Z", "")) + timedelta(days=365)
        
        # Check if loan is paid off
        if new_outstanding_balance <= 0.01:  # Account for floating point precision
            loan["status"] = "paid_off"
            loan["next_payment_due"] = None
            loan["paid_off_at"] = payment_date
        else:
            loan["next_payment_due"] = next_due.isoformat() + "Z"
        
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_loan_payment",
                "description": "Process a loan payment, update outstanding balance and calculate next payment due date.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "loan_id": {"type": "string"},
                        "payment_amount": {"type": "number"},
                        "payment_date": {"type": "string"}
                    },
                    "required": ["loan_id", "payment_amount"]
                }
            }
        }
