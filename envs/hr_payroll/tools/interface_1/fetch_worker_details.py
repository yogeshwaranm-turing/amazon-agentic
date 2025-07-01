from typing import Dict, Any
from tau_bench.envs.tool import Tool

class FetchWorkerDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> Dict[str, Any]:
        workers = data["workers"]
        users = data["users"]
        orgs = data["organizations"]

        if worker_id not in workers:
            raise ValueError("Worker not found")
        worker = workers[worker_id]

        user = users.get(worker["user_id"], {})
        org = orgs.get(worker["organization_id"], {})

        return {
            "worker_id": worker_id,
            "status": worker["status"],
            "type": worker["type"],
            "position_title": worker.get("position_title"),
            "department": worker.get("department"),
            "user_email": user.get("email"),
            "organization": org.get("name")
        }

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "fetch_worker_details",
            "description": "Retrieve detailed profile information for a given worker including linked user and organization info.",
            "parameters": {
                "worker_id": {"type": "string", "description": "ID of the worker"}
            },
            "returns": {"type": "object", "description": "Detailed worker information"}
        }