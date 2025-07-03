
import json
from typing import Any, Dict
from collections import defaultdict
from tau_bench.envs.tool import Tool

class GetReimbursementTotalsByWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        reimbursements = data.get("reimbursements", {})
        result = defaultdict(float)

        for r in reimbursements.values():
            if r.get("worker_id") == worker_id:
                status = r.get("status", "submitted")
                result[status] += r.get("amount", 0)

        return json.dumps({
            "worker_id": worker_id,
            "totals": dict(result)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reimbursement_totals_by_worker",
                "description": "Summarizes reimbursements for a worker across different statuses",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID to fetch reimbursement totals for"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
