from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class NotifyHRTeam(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, contract_id: str) -> str:
        notification_id = f"notify_{uuid.uuid4().hex[:8]}"
        if "notifications" not in data:
            data["notifications"] = {}
        data["notifications"][notification_id] = {
            "notification_id": notification_id,
            "type": "hr_termination_notice",
            "worker_id": worker_id,
            "contract_id": contract_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        return notification_id

    @staticmethod
    def get_info():
        return {
            "name": "notify_hr_team",
            "description": "Notifies the HR team of an expiring contract and pending termination.",
            "parameters": {
                "worker_id": "str",
                "contract_id": "str"
            },
            "returns": "str"
        }