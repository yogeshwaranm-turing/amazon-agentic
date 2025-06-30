from tau_bench.envs.tool import Tool
from typing import Any, Dict
from datetime import datetime

class ProcessReimbursement(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str) -> str:
        reimbursement = data["reimbursements"].get(reimbursement_id)
        if not reimbursement:
            raise ValueError("Reimbursement not found.")
        reimbursement["status"] = "processed"
        reimbursement["processed_at"] = datetime.utcnow().isoformat()
        return reimbursement_id

    @staticmethod
    def get_info():
        return {
            "name": "process_reimbursement",
            "description": "Processes a valid reimbursement using the supported method.",
            "parameters": {
                "reimbursement_id": "str"
            },
            "returns": "str"
        }