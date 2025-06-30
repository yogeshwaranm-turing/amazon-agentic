from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class AssignToHR(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        task_id = f"hrtask_{uuid.uuid4().hex[:8]}"
        if "hr_tasks" not in data:
            data["hr_tasks"] = {}
        data["hr_tasks"][task_id] = {
            "task_id": task_id,
            "worker_id": worker_id,
            "type": "compliance_followup",
            "status": "assigned",
            "assigned_at": datetime.utcnow().isoformat()
        }
        return task_id

    @staticmethod
    def get_info():
        return {
            "name": "assign_to_hr",
            "description": "Assigns a compliance follow-up task to the HR team.",
            "parameters": {
                "worker_id": "str"
            },
            "returns": "str"
        }