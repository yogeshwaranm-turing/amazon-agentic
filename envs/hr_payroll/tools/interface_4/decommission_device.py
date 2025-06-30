from typing import Dict, Any
from tau_bench.envs.tool import Tool

class DecommissionDevice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return {"result": "ok", "tool": "decommission_device", "input": kwargs}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "decommission_device",
                "description": "Placeholder for decommission device.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "example_field": {"type": "string"}
                    },
                    "required": ["example_field"]
                }
            }
        }
