from tau_bench.envs.tool import Tool
from typing import Any, Dict

class ApproveTimeEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], time_entry_id: str) -> str:
        entry = data["time_entries"].get(time_entry_id)
        if not entry:
            raise ValueError("Time entry not found.")
        entry["status"] = "approved"
        return time_entry_id

    @staticmethod
    def get_info():
        return {
            "name": "approve_time_entry",
            "description": "Approves a normal time entry for payroll processing.",
            "parameters": {
                "time_entry_id": "str"
            },
            "returns": "str"
        }