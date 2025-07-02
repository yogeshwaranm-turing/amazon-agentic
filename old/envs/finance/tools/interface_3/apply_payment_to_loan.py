import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ApplyPaymentToLoan(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], loan_id: str, amount: float) -> str:
        lns = data.get("loans", {})
        loan = lns.get(loan_id)
        
        if not loan:
            raise KeyError(f"Loan {loan_id} not found")
          
        payments = data.setdefault("loan_payments", {})
        pay_id = f"LP-{len(payments)+1:06d}"
        now = "2025-01-01T00:00:00Z"
        payment = {
          "payment_id": pay_id, 
          "loan_id": loan_id, 
          "amount": amount, 
          "currency": loan.get("currency","USD"), 
          "paid_at": now
        }
        payments[pay_id] = payment
        
        # reduce principal
        loan["principal_amount"] = loan.get("principal_amount",0.0) - amount
        if loan["principal_amount"] <= 0:
            loan["status"] = "paid_off"
            loan["paid_off_at"] = now
            
        return json.dumps({"payment": payment, "loan": loan})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"apply_payment_to_loan",
            "description":"Record a payment towards a loan and update principal.",
            "parameters":{"type":"object","properties":{"loan_id":{"type":"string"},"amount":{"type":"number"}},"required":["loan_id","amount"]}
        }}