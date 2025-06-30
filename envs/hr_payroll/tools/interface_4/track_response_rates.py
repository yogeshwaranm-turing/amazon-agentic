from tau_bench.envs.tool import Tool
from typing import Any, Dict

class TrackResponseRates(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], survey_id: str) -> Dict[str, float]:
        responses = data["engagement_responses"]
        teams = data["team_members"]
        team_response_counts = {}
        team_member_counts = {}

        for member_id, member in teams.items():
            team_id = member["team_id"]
            team_member_counts[team_id] = team_member_counts.get(team_id, 0) + 1
            for resp in responses.values():
                if resp.get("survey_id") == survey_id and resp.get("worker_id") == member["worker_id"]:
                    team_response_counts[team_id] = team_response_counts.get(team_id, 0) + 1

        result = {}
        for team_id in team_member_counts:
            responses = team_response_counts.get(team_id, 0)
            members = team_member_counts[team_id]
            result[team_id] = round((responses / members) * 100, 2)

        return result

    @staticmethod
    def get_info():
        return {
            "name": "track_response_rates",
            "description": "Calculates team-wise engagement survey response rates as a percentage.",
            "parameters": {
                "survey_id": "str"
            },
            "returns": "Dict[str, float]"
        }