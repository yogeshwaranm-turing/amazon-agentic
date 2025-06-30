import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> str:
        raise NotImplementedError("This tool is yet to be implemented with real logic.")

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_users",
                "description": "Placeholder for list_users.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "placeholder": {
                            "type": "string",
                            "description": "Replace with actual parameters."
                        }
                    },
                    "required": ["placeholder"]
                }
            }
        }
