import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPendingReimbursements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], organization_id: str) -> str:
        reimbursements = data.get("reimbursements", {})
        pending = [
            r for r in reimbursements.values()
            if r.get("status") == "submitted" and r.get("organization_id") == organization_id
        ]
        return json.dumps(pending)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pending_reimbursements",
                "description": "Returns all reimbursements pending approval for a specific organization",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "The ID of the organization for which pending reimbursements are requested"
                        }
                    },
                    "required": ["organization_id"]
                }
            }
        }
