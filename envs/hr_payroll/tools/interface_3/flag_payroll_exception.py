from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class FlagPayrollException(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, reason: str) -> str:
        exception_id = f"exception_{uuid.uuid4().hex[:8]}"
        if "payroll_exceptions" not in data:
            data["payroll_exceptions"] = {}
        data["payroll_exceptions"][exception_id] = {
            "exception_id": exception_id,
            "worker_id": worker_id,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        return exception_id

    @staticmethod
    def get_info():
        return {
            "name": "flag_payroll_exception",
            "description": "Flags a payroll exception for a worker with a reason.",
            "parameters": {
                "worker_id": "str",
                "reason": "str"
            },
            "returns": "str"
        }