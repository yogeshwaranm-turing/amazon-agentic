import json
import random
import string
from typing import Any, Dict
from datetime import datetime, timedelta, timezone
from tau_bench.envs.tool import Tool

class ApplyLoan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        user_id: str, 
        principal: float, 
        interest_rate: float, 
        term_years: int
    ) -> str:
        loans = data["loans"]
        issued = datetime.now(timezone.utc)
        date_part = issued.strftime('%y%m%d')

        # Helper to generate a unique ID of form "LN-<YYMMDD>-<4 alphanumeric>"
        def gen_loan_id():
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            return f"LN-{date_part}-{suffix}"

        loan_id = gen_loan_id()
        while loan_id in loans:
            loan_id = gen_loan_id()

        maturity = issued + timedelta(days=365 * term_years)
        first_due = issued + timedelta(days=30)

        record = {
            "loan_id": loan_id,
            "user_id": user_id,
            "principal": principal,
            "interest_rate": interest_rate,
            "issued_at": issued.isoformat() + "Z",
            "maturity_date": maturity.isoformat() + "Z",
            "status": "active",
            "currency": "USD",
            "term_months": term_years * 12,
            "payment_frequency": "monthly",
            "origination_fee": round(principal * 0.01, 2),
            "loan_purpose": None,
            "collateral": None,
            "credit_score_at_issue": None,
            "outstanding_balance": principal,
            "total_paid": 0.0,
            "last_payment_at": None,
            "next_payment_due": first_due.isoformat() + "Z"
        }

        loans[loan_id] = record
        return json.dumps(record, indent=2)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "apply_loan",
                "description": "Create a new loan for a customer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string"
                        },
                        "principal": {
                            "type": "number"
                        },
                        "interest_rate": {
                            "type": "number"
                        },
                        "term_years": {
                            "type": "integer"
                        }
                    },
                    "required": ["user_id", "principal", "interest_rate", "term_years"]
                }
            }
        }