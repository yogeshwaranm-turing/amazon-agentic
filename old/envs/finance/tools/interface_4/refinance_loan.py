import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RefinanceLoan(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      loan_id: str, 
      new_rate: float, 
      new_term_months: int
    ) -> str:
        loans = data["loans"]
        loan = loans.get(loan_id)
        
        if not loan:
            raise KeyError(f"Loan {loan_id} not found")
          
        loan["interest_rate"] = new_rate
        loan["term_months"] = new_term_months
        loan["issued_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"refinance_loan",
                "description":"Re-structure an existing loan.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "loan_id":{"type":"string"},
                        "new_rate":{"type":"number"},
                        "new_term_months":{"type":"integer"}
                    },
                    "required":["loan_id","new_rate","new_term_months"]
                }
            }
        }