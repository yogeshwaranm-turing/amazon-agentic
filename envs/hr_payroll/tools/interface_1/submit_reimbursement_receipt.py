
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SubmitReimbursementReceipt(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str, document_id: str) -> str:
        reimbursements = data.get("reimbursements", {})
        documents = data.get("documents", {})

        if reimbursement_id not in reimbursements:
            raise ValueError("Reimbursement not found")
        if document_id not in documents:
            raise ValueError("Document not found")

        reimbursements[reimbursement_id]["document_id"] = document_id
        return json.dumps(reimbursements[reimbursement_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "submit_reimbursement_receipt",
                "description": "Uploads receipt to a reimbursement",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reimbursement_id": {"type": "string"},
                        "document_id": {"type": "string"}
                    },
                    "required": ["reimbursement_id", "document_id"]
                }
            }
        }
