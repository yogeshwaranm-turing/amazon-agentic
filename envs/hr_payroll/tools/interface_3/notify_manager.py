from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class NotifyManager(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, issue: str) -> str:
        notification_id = f"mgr_alert_{uuid.uuid4().hex[:8]}"
        if "notifications" not in data:
            data["notifications"] = {}
        data["notifications"][notification_id] = {
            "notification_id": notification_id,
            "worker_id": worker_id,
            "type": "time_entry_alert",
            "issue": issue,
            "timestamp": datetime.utcnow().isoformat()
        }
        return notification_id

    @staticmethod
    def get_info():
        return {
            "name": "notify_manager",
            "description": "Sends an anomaly alert to the manager for a time entry issue.",
            "parameters": {
                "worker_id": "str",
                "issue": "str"
            },
            "returns": "str"
        }