
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetPendingReimbursements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        reimbursements = data.get("reimbursements", {})
        pending = [r for r in reimbursements.values() if r.get("status") == "submitted"]
        return json.dumps(pending)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_pending_reimbursements",
                "description": "Returns all reimbursements that are pending approval",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
