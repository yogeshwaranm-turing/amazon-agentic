
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FetchTimeSummaryByTeam(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], team_id: str) -> str:
        team_members = data.get("team_members", {})
        time_entries = data.get("time_entries", {})

        worker_ids = [m["worker_id"] for m in team_members.values() if m["team_id"] == team_id]
        summary = {}
        for entry in time_entries.values():
            if entry["worker_id"] in worker_ids:
                date = entry["date"]
                summary[date] = summary.get(date, 0) + entry.get("duration_hours", 0)

        return json.dumps({"team_id": team_id, "summary_by_date": summary})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_time_summary_by_team",
                "description": "Fetches time entries grouped by team",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "team_id": {
                            "type": "string",
                            "description": "The ID of the team whose time entries should be summarized"
                        }
                    },
                    "required": ["team_id"]
                }
            }
        }
