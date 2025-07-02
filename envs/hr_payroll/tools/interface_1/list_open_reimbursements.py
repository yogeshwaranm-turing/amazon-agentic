import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ListOpenReimbursements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: str) -> str:
        reimbursements = data.get("reimbursements", {})
        open_items = [
            r for r in reimbursements.values()
            if r.get("status") == "submitted" and r.get("user_id") == user_id
        ]
        return json.dumps(open_items)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_open_reimbursements",
                "description": "Lists all reimbursements pending approval for a specific user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose open reimbursements are to be listed"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        }
