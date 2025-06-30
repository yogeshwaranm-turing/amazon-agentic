import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class TerminateWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, reason: str) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError(f"Worker '{worker_id}' not found.")

        worker = workers[worker_id]
        if worker.get("status") == "terminated":
            raise ValueError(f"Worker '{worker_id}' is already terminated.")

        worker["status"] = "terminated"
        worker["termination_reason"] = reason
        worker["updated_at"] = "2025-06-30T09:25:07.713368Z"
        return json.dumps(worker)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "terminate_worker",
                "description": "Terminate a worker's contract and update their status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID to terminate."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for termination."
                        }
                    },
                    "required": ["worker_id", "reason"]
                }
            }
        }
