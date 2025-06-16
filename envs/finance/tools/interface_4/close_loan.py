import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CloseLoan(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        loan_id: str
    ) -> str:
        loans = data["loans"]
        loan = loans.get(loan_id)
        
        if not loan:
            raise KeyError(f"Loan {loan_id} not found")
        
        loan["status"] = "paid_off"
        loan["maturity_date"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"close_loan",
                "description":"Mark a loan as paid-off/closed.",
                "parameters":{
                    "type":"object",
                    "properties":{"loan_id":{"type":"string"}},
                    "required":["loan_id"]
                }
            }
        }