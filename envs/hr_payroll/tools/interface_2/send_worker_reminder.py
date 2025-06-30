from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class SendWorkerReminder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, document_type: str) -> str:
        reminder_id = f"reminder_{uuid.uuid4().hex[:8]}"
        if "reminders" not in data:
            data["reminders"] = {}
        data["reminders"][reminder_id] = {
            "reminder_id": reminder_id,
            "worker_id": worker_id,
            "document_type": document_type,
            "sent_at": datetime.utcnow().isoformat()
        }
        return reminder_id

    @staticmethod
    def get_info():
        return {
            "name": "send_worker_reminder",
            "description": "Sends a document reminder to the worker.",
            "parameters": {
                "worker_id": "str",
                "document_type": "str"
            },
            "returns": "str"
        }