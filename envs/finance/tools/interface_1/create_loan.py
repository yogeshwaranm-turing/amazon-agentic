import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class CreateLoan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        principal: float,
        interest_rate: float,
        term_months: int,
        payment_frequency: str,
        loan_purpose: str,
        collateral: str = None
    ) -> str:
        users = data.get("users", {})
        loans = data.setdefault("loans", {})
        accounts = data.get("accounts", {})
        
        # Validate user exists
        if user_id not in users:
            raise ValueError(f"User {user_id} not found.")
        
        # Check if user has at least one active account
        user_accounts = [acc for acc in accounts.values() if acc.get("user_id") == user_id and acc.get("status") == "open"]
        if not user_accounts:
            raise ValueError(f"User {user_id} has no active accounts.")
        
        # Generate loan ID
        loan_id = f"LN-{datetime.now().strftime('%y%m%d')}-{datetime.now().strftime('%H%M%S')}"
        
        # Calculate dates
        issued_at = datetime.now().isoformat() + "Z"
        maturity_date = (datetime.now() + timedelta(days=term_months * 30)).isoformat() + "Z"
        
        # Calculate fees
        origination_fee = principal * 0.01  # 1% origination fee
        
        # Create loan record
        loan = {
            "loan_id": loan_id,
            "user_id": user_id,
            "principal": principal,
            "interest_rate": interest_rate,
            "issued_at": issued_at,
            "maturity_date": maturity_date,
            "status": "active",
            "currency": "USD",
            "term_months": term_months,
            "payment_frequency": payment_frequency,
            "origination_fee": origination_fee,
            "loan_purpose": loan_purpose,
            "collateral": collateral,
            "credit_score_at_issue": 650,  # Default credit score
            "outstanding_balance": principal,
            "total_paid": 0.0,
            "last_payment_at": None,
            "next_payment_due": (datetime.now() + timedelta(days=30)).isoformat() + "Z"
        }
        
        loans[loan_id] = loan
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_loan",
                "description": "Create a new loan for a user with validation against user and account status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string"},
                        "principal": {"type": "number"},
                        "interest_rate": {"type": "number"},
                        "term_months": {"type": "integer"},
                        "payment_frequency": {"type": "string", "enum": ["monthly", "quarterly", "annually"]},
                        "loan_purpose": {"type": "string"},
                        "collateral": {"type": "string"}
                    },
                    "required": ["user_id", "principal", "interest_rate", "term_months", "payment_frequency", "loan_purpose"]
                }
            }
        }
