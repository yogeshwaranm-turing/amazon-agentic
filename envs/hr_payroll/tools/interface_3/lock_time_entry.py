from tau_bench.envs.tool import Tool
from typing import Any, Dict

class LockTimeEntry(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], time_entry_id: str) -> str:
        entry = data["time_entries"].get(time_entry_id)
        if not entry:
            raise ValueError("Time entry not found.")
        entry["status"] = "locked"
        return time_entry_id

    @staticmethod
    def get_info():
        return {
            "name": "lock_time_entry",
            "description": "Locks a time entry to prevent payroll processing.",
            "parameters": {
                "time_entry_id": "str"
            },
            "returns": "str"
        }