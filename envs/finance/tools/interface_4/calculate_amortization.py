import json
from typing import Any, Dict
from datetime import datetime, timedelta, timezone
from tau_bench.envs.tool import Tool

class CalculateAmortization(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      principal: float, 
      interest_rate: float, 
      term_years: int, 
      payments_per_year: int = 12
    ) -> str:
        rate = interest_rate / 100 / payments_per_year
        total_payments = term_years * payments_per_year
        payment = (rate * principal) / (1 - (1 + rate) ** -total_payments)
        schedule = []
        balance = principal
        start = datetime.now(timezone.utc)
        interval = timedelta(days=int(365 / payments_per_year))
        
        for n in range(1, total_payments + 1):
            interest_component = round(balance * rate, 2)
            principal_component = round(payment - interest_component, 2)
            balance = round(balance - principal_component, 2)
            payment_date = (start + interval * n).isoformat() + "Z"
            
            schedule.append({
                "payment_number": n,
                "payment_date": payment_date,
                "principal_component": principal_component,
                "interest_component": interest_component,
                "balance": balance
            })
            
        return json.dumps({"schedule": schedule})

    @staticmethod
    def get_info() -> Dict[str, Any]: 
        return {
            "type": "function",
            "function": {
                "name": "calculate_amortization",
                "description": "Generate an amortization schedule for a loan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "principal": {
                            "type": "number"
                        },
                        "interest_rate": {
                            "type": "number"
                        },
                        "term_years": {
                            "type": "integer"
                        },
                        "payments_per_year": {
                            "type": "integer"
                        }
                    },
                    "required": ["principal", "interest_rate", "term_years"]
                }
            }
        }