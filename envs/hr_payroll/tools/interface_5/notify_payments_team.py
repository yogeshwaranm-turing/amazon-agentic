from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class NotifyPaymentsTeam(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], reimbursement_id: str) -> str:
        notification_id = f"pay_notify_{uuid.uuid4().hex[:8]}"
        if "notifications" not in data:
            data["notifications"] = {}
        data["notifications"][notification_id] = {
            "notification_id": notification_id,
            "type": "reimbursement_issue",
            "reimbursement_id": reimbursement_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        return notification_id

    @staticmethod
    def get_info():
        return {
            "name": "notify_payments_team",
            "description": "Sends a notification to the payments team about a reimbursement issue.",
            "parameters": {
                "reimbursement_id": "str"
            },
            "returns": "str"
        }