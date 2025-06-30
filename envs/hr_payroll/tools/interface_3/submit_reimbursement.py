from typing import Dict, Any
from tau_bench.envs.tool import Tool

class SubmitReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return {"result": "ok", "tool": "submit_reimbursement", "input": kwargs}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_reimbursement",
                "description": "Placeholder for submit reimbursement.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "example_field": {"type": "string"}
                    },
                    "required": ["example_field"]
                }
            }
        }
