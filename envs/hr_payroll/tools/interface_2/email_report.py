from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class EmailReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], document_id: str) -> str:
        email_id = f"email_{uuid.uuid4().hex[:8]}"
        if "emails" not in data:
            data["emails"] = {}
        data["emails"][email_id] = {
            "email_id": email_id,
            "document_id": document_id,
            "sent_at": datetime.utcnow().isoformat()
        }
        return email_id

    @staticmethod
    def get_info():
        return {
            "name": "email_report",
            "description": "Emails a risk heatmap report document.",
            "parameters": {
                "document_id": "str"
            },
            "returns": "str"
        }