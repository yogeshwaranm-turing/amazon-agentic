from typing import Dict, Any
from tau_bench.envs.tool import Tool

class CalculateGrossPayroll(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return {"result": "ok", "tool": "calculate_gross_payroll", "input": kwargs}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_gross_payroll",
                "description": "Placeholder for calculate gross payroll.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "example_field": {"type": "string"}
                    },
                    "required": ["example_field"]
                }
            }
        }
