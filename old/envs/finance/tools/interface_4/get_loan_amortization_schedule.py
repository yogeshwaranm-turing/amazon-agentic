import json
from typing import Any, Dict, List
from decimal import Decimal, getcontext
from tau_bench.envs.tool import Tool

getcontext().prec = 10

class GetLoanAmortizationSchedule(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      loan_id: str
    ) -> str:
        loans = data.get("loans", {})
        loan = loans.get(loan_id)
        
        if not loan:
            raise KeyError(f"Loan {loan_id} not found")
          
        principal = Decimal(str(loan["principal_amount"]))
        rate = Decimal(str(loan["interest_rate"]))/Decimal('100')/Decimal('12')
        n = loan.get("term_months", 0)
        if n<=0 or rate==0:
            raise ValueError("Invalid term or rate")
          
        # Monthly payment formula
        payment = principal * rate / (1 - (1+rate)**(-n))
        schedule: List[Dict[str,Any]] = []
        balance = principal
        for m in range(1, n+1):
            interest = balance * rate
            principal_paid = payment - interest
            balance -= principal_paid
            schedule.append({
                "month": m,
                "payment": float(round(payment,2)),
                "principal": float(round(principal_paid,2)),
                "interest": float(round(interest,2)),
                "balance": float(round(balance if balance>0 else Decimal('0.00'),2))
            })
            
        return json.dumps(schedule)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"get_loan_amortization_schedule",
            "description":"Generate amortization schedule for a loan.",
            "parameters":{
                "type":"object",
                "properties":{ "loan_id":{"type":"string"} },
                "required":["loan_id"]
            }
        }}