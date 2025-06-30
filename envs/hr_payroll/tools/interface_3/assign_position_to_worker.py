import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class AssignPositionToWorker(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, position_id: str) -> str:
        workers = data.get("workers", {})
        hr_positions = data.get("hr_positions", {})

        if worker_id not in workers:
            raise ValueError(f"Worker '{worker_id}' not found.")

        if position_id not in hr_positions:
            raise ValueError(f"Position '{position_id}' not found.")

        workers[worker_id]["position_id"] = position_id
        workers[worker_id]["updated_at"] = "2025-06-30T09:25:07.697803Z"

        return json.dumps(workers[worker_id])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_position_to_worker",
                "description": "Assign a job position to an existing worker.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "ID of the worker to assign the position to."
                        },
                        "position_id": {
                            "type": "string",
                            "description": "ID of the position to assign."
                        }
                    },
                    "required": ["worker_id", "position_id"]
                }
            }
        }
