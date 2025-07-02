
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOpenReimbursements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        reimbursements = data.get("reimbursements", {})
        open_items = [r for r in reimbursements.values() if r.get("status") == "submitted"]
        return json.dumps(open_items)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_open_reimbursements",
                "description": "Lists all reimbursements pending approval",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
