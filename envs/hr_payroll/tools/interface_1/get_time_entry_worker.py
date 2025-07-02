
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetTimeEntryWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        time_entries = data.get("time_entries", {})
        result = [entry for entry in time_entries.values() if entry.get("worker_id") == worker_id]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_time_entry_worker",
                "description": "Fetches total hours logged by a worker",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {"type": "string"}
                    },
                    "required": ["worker_id"]
                }
            }
        }
