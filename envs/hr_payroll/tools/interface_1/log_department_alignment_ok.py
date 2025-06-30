from tau_bench.envs.tool import Tool
from typing import Any, Dict
from datetime import datetime

class LogDepartmentAlignmentOK(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        log_id = f"align_ok_{worker_id}"
        if "alignment_logs" not in data:
            data["alignment_logs"] = {}
        data["alignment_logs"][log_id] = {
            "log_id": log_id,
            "worker_id": worker_id,
            "status": "aligned",
            "timestamp": datetime.utcnow().isoformat()
        }
        return log_id

    @staticmethod
    def get_info():
        return {
            "name": "log_department_alignment_ok",
            "description": "Logs that a worker's position and department are properly aligned.",
            "parameters": {
                "worker_id": "str"
            },
            "returns": "str"
        }