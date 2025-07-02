import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateLoanTerms(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        loan_id: str, 
        updates: Dict[str, Any]
    ) -> str:
        loans = data["loans"]
        loan = loans.get(loan_id)
        
        if not loan:
            raise KeyError(f"Loan {loan_id} not found")
        
        loan.update(updates)
        
        return json.dumps(loan)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"update_loan_terms",
                "description":"Tweak term_months or interest_rate on a loan.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "loan_id":{"type":"string"},
                        "updates": { 
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "string",
                                    "enum": ["active", "defaulted", "paid_off"],
                                    "description": "The status of the loan to update to"
                                },
                                "interest_rate": {
                                    "type": "number",
                                    "description": "The interest rate to be changed to"
                                },
                                "term_months": {
                                    "type": "number",
                                    "description": "The term month to be changed to"
                                },
                                "maturity_date": {
                                    "type": "string",
                                    "format": "date",
                                    "description": "The maturity date to be updated to"
                                }
                            }
                        }
                    },
                    "required":["loan_id","updates"]
                }
            }
        }