from tau_bench.envs.tool import Tool
from typing import Any, Dict

class FlagTeamForFollowup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], team_id: str) -> str:
        if "team_flags" not in data:
            data["team_flags"] = {}
        data["team_flags"][team_id] = {
            "team_id": team_id,
            "reason": "low_survey_participation",
            "status": "flagged"
        }
        return team_id

    @staticmethod
    def get_info():
        return {
            "name": "flag_team_for_followup",
            "description": "Flags a team for HR follow-up due to low engagement.",
            "parameters": {
                "team_id": "str"
            },
            "returns": "str"
        }