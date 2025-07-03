import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetWorkerProfileById(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        workers = data.get("workers", {})
        if worker_id not in workers:
            raise ValueError("Worker not found")
        worker = workers[worker_id]
        return json.dumps({
            "worker_id": worker_id,
            "user_id": worker.get("user_id"),
            "worker_type": worker.get("worker_type"),
            "status": worker.get("status"),
            "organization_id": worker.get("organization_id")
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_worker_profile_by_id",
                "description": "Retrieves the complete profile of a worker using their worker_id.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {"type": "string", "description": "Worker ID"}
                    },
                    "required": ["worker_id"]
                }
            }
        }
