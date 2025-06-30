from tau_bench.envs.tool import Tool
from typing import Any, Dict

class RouteToManualReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str) -> str:
        reimbursement = data["reimbursements"].get(reimbursement_id)
        if not reimbursement:
            raise ValueError("Reimbursement not found.")
        reimbursement["status"] = "manual_review"
        return reimbursement_id

    @staticmethod
    def get_info():
        return {
            "name": "route_to_manual_review",
            "description": "Routes a reimbursement to manual review due to unsupported payment method.",
            "parameters": {
                "reimbursement_id": "str"
            },
            "returns": "str"
        }