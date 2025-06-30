from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class SendTerminationNotice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        notice_id = f"notice_{uuid.uuid4().hex[:8]}"
        if "termination_notices" not in data:
            data["termination_notices"] = {}
        data["termination_notices"][notice_id] = {
            "notice_id": notice_id,
            "worker_id": worker_id,
            "sent_at": datetime.utcnow().isoformat()
        }
        return notice_id

    @staticmethod
    def get_info():
        return {
            "name": "send_termination_notice",
            "description": "Sends a termination notice to a worker whose contract is ending.",
            "parameters": {
                "worker_id": "str"
            },
            "returns": "str"
        }