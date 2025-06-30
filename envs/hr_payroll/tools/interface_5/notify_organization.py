from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class NotifyOrganization(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], organization_id: str) -> str:
        notification_id = f"org_notify_{uuid.uuid4().hex[:8]}"
        if "notifications" not in data:
            data["notifications"] = {}
        data["notifications"][notification_id] = {
            "notification_id": notification_id,
            "organization_id": organization_id,
            "type": "invoice_overdue",
            "timestamp": datetime.utcnow().isoformat()
        }
        return notification_id

    @staticmethod
    def get_info():
        return {
            "name": "notify_organization",
            "description": "Sends an overdue invoice notification to an organization.",
            "parameters": {
                "organization_id": "str"
            },
            "returns": "str"
        }