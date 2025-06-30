from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class CreateComplianceAction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, document_type: str) -> str:
        action_id = f"comp_action_{uuid.uuid4().hex[:8]}"
        if "compliance_actions" not in data:
            data["compliance_actions"] = {}
        data["compliance_actions"][action_id] = {
            "compliance_action_id": action_id,
            "worker_id": worker_id,
            "document_type": document_type,
            "status": "open",
            "created_at": datetime.utcnow().isoformat()
        }
        return action_id

    @staticmethod
    def get_info():
        return {
            "name": "create_compliance_action",
            "description": "Creates a compliance action for missing or expired documents.",
            "parameters": {
                "worker_id": "str",
                "document_type": "str"
            },
            "returns": "str"
        }