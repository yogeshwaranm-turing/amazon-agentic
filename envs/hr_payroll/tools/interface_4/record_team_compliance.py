from tau_bench.envs.tool import Tool
from typing import Any, Dict
from datetime import datetime

class RecordTeamCompliance(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], team_id: str) -> str:
        if "team_compliance_logs" not in data:
            data["team_compliance_logs"] = {}
        data["team_compliance_logs"][team_id] = {
            "team_id": team_id,
            "status": "compliant",
            "recorded_at": datetime.utcnow().isoformat()
        }
        return team_id

    @staticmethod
    def get_info():
        return {
            "name": "record_team_compliance",
            "description": "Marks a team as compliant for engagement survey.",
            "parameters": {
                "team_id": "str"
            },
            "returns": "str"
        }