from typing import Dict, Any
from tau_bench.envs.tool import Tool

class SetWorkerPositionInfo(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, title: str, department: str, start_date: str) -> str:
        workers = data["workers"]

        if worker_id not in workers:
            raise ValueError("Worker not found")

        workers[worker_id]["position_title"] = title
        workers[worker_id]["department"] = department
        workers[worker_id]["position_status"] = "active"
        workers[worker_id]["position_start_date"] = start_date
        workers[worker_id]["position_end_date"] = None

        return "Worker position info updated"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "set_worker_position_info",
            "description": "Assign or update position title and department for a worker.",
            "parameters": {
                "worker_id": {"type": "string", "description": "Worker ID"},
                "title": {"type": "string", "description": "Position title"},
                "department": {"type": "string", "description": "Department name"},
                "start_date": {"type": "string", "description": "Position start date (YYYY-MM-DD)"}
            },
            "returns": {"type": "string", "description": "Confirmation message"}
        }