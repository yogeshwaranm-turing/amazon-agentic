from tau_bench.envs.tool import Tool
from typing import Any, Dict, List

class DetectAnomalies(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entries: List[str]) -> List[str]:
        anomalies = []
        for entry_id in entries:
            entry = data["time_entries"].get(entry_id)
            if not entry:
                continue
            duration = entry.get("duration_hours", 0)
            if duration > 12 or duration == 0:
                anomalies.append(entry_id)
        return anomalies

    @staticmethod
    def get_info():
        return {
            "name": "detect_anomalies",
            "description": "Detects anomalies in time entries based on duration (e.g., >12 hours or 0).",
            "parameters": {
                "entries": "List[str]"
            },
            "returns": "List[str]"
        }