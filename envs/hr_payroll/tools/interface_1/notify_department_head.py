from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class NotifyDepartmentHead(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        notification_id = f"dephead_notify_{uuid.uuid4().hex[:8]}"
        if "notifications" not in data:
            data["notifications"] = {}
        data["notifications"][notification_id] = {
            "notification_id": notification_id,
            "worker_id": worker_id,
            "type": "position_misalignment",
            "timestamp": datetime.utcnow().isoformat()
        }
        return notification_id

    @staticmethod
    def get_info():
        return {
            "name": "notify_department_head",
            "description": "Notifies the department head of a persistent position misalignment.",
            "parameters": {
                "worker_id": "str"
            },
            "returns": "str"
        }