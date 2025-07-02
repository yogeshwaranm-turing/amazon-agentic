import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetLoanDetails(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      loan_id: str
    ) -> str:
        loan = data.get("loans", {}).get(loan_id)
        
        if not loan:
            raise KeyError(f"Loan {loan_id} not found")
          
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"get_loan_details",
                "description":"Retrieve full loan record by loan_id.",
                "parameters":{
                    "type":"object",
                    "properties":{"loan_id":{"type":"string"}},
                    "required":["loan_id"]
                }
            }
        }