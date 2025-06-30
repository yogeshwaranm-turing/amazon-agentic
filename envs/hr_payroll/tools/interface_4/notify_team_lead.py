from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class NotifyTeamLead(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], team_id: str) -> str:
        notification_id = f"teamlead_notify_{uuid.uuid4().hex[:8]}"
        if "notifications" not in data:
            data["notifications"] = {}
        data["notifications"][notification_id] = {
            "notification_id": notification_id,
            "team_id": team_id,
            "type": "low_engagement_alert",
            "timestamp": datetime.utcnow().isoformat()
        }
        return notification_id

    @staticmethod
    def get_info():
        return {
            "name": "notify_team_lead",
            "description": "Sends a notification to the team lead for low survey participation.",
            "parameters": {
                "team_id": "str"
            },
            "returns": "str"
        }