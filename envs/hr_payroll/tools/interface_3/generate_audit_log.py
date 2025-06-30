from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class GenerateAuditLog(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, reason: str) -> str:
        audit_id = f"audit_{uuid.uuid4().hex[:8]}"
        if "audit_logs" not in data:
            data["audit_logs"] = {}
        data["audit_logs"][audit_id] = {
            "audit_id": audit_id,
            "worker_id": worker_id,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        return audit_id

    @staticmethod
    def get_info():
        return {
            "name": "generate_audit_log",
            "description": "Generates an audit log entry for a skipped payroll item.",
            "parameters": {
                "worker_id": "str",
                "reason": "str"
            },
            "returns": "str"
        }