from typing import Dict, Any
from tau_bench.envs.tool import Tool

class CalculateAmortization(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], principal: float, interest_rate: float, term_years: int) -> Dict[str, Any]:
        monthly_rate = interest_rate / 12 / 100
        n = term_years * 12
        monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -n)
        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_payment": round(monthly_payment * n, 2),
            "schedule": [{"month": i + 1, "payment": round(monthly_payment, 2)} for i in range(n)]
        }

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_amortization",
                "description": "Calculate the monthly loan payment and generate amortization schedule.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "principal": {"type": "number"},
                        "interest_rate": {"type": "number"},
                        "term_years": {"type": "integer"}
                    },
                    "required": ["principal", "interest_rate", "term_years"]
                }
            }
        }