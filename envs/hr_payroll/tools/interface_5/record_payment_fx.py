from typing import Dict, Any
from tau_bench.envs.tool import Tool

class RecordPaymentFx(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return {"result": "ok", "tool": "record_payment_fx", "input": kwargs}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "record_payment_fx",
                "description": "Placeholder for record payment fx.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "example_field": {"type": "string"}
                    },
                    "required": ["example_field"]
                }
            }
        }
