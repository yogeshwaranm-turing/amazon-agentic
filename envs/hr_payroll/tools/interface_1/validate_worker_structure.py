from typing import Dict, Any
from tau_bench.envs.tool import Tool

class ValidateWorkerStructure(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        workers = data["workers"]
        if worker_id not in workers:
            raise ValueError("Worker not found")
        worker = workers[worker_id]
        required_fields = ["position_title", "department", "organization_id", "user_id"]
        missing = [f for f in required_fields if not worker.get(f)]
        if missing:
            return f"Incomplete: missing {', '.join(missing)}"
        return "Valid"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "validate_worker_structure",
            "description": "Checks whether a worker has all necessary fields to be considered valid in the system.",
            "parameters": {
                "worker_id": {"type": "string", "description": "ID of the worker to validate"}
            },
            "returns": {"type": "string", "description": "Validation status"}
        }