import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class UpdateWorkerStatus(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        worker_id: str,
        new_status: str
    ) -> str:
        workers = data.get("workers", {})

        if worker_id not in workers:
            raise ValueError(f"Worker ID '{worker_id}' not found.")

        allowed_statuses = ["active", "terminated", "on_leave", "suspended"]
        if new_status not in allowed_statuses:
            raise ValueError(f"Invalid status '{new_status}'. Must be one of {allowed_statuses}.")

        worker = workers[worker_id]
        worker["status"] = new_status
        worker["updated_at"] = "2025-06-30T09:25:07.732625Z"
        return json.dumps(worker)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_worker_status",
                "description": "Update the employment status of a worker (e.g., active, suspended).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {"type": "string", "description": "The ID of the worker to update."},
                        "new_status": {
                            "type": "string",
                            "enum": ["active", "terminated", "on_leave", "suspended"],
                            "description": "New status to apply to the worker."
                        }
                    },
                    "required": ["worker_id", "new_status"]
                }
            }
        }
