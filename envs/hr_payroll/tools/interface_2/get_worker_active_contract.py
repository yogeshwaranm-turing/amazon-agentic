from typing import Dict, Any
from tau_bench.envs.tool import Tool

class GetWorkerActiveContract(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return {"result": "ok", "tool": "get_worker_active_contract", "input": kwargs}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_worker_active_contract",
                "description": "Placeholder for get worker active contract.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "example_field": {"type": "string"}
                    },
                    "required": ["example_field"]
                }
            }
        }
