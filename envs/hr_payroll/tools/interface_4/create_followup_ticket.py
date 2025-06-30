from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class CreateFollowupTicket(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        ticket_id = f"ticket_{uuid.uuid4().hex[:8]}"
        if "followup_tickets" not in data:
            data["followup_tickets"] = {}
        data["followup_tickets"][ticket_id] = {
            "ticket_id": ticket_id,
            "worker_id": worker_id,
            "type": "device_return",
            "status": "open",
            "created_at": datetime.utcnow().isoformat()
        }
        return ticket_id

    @staticmethod
    def get_info():
        return {
            "name": "create_followup_ticket",
            "description": "Creates a follow-up ticket for a device not returned by the worker.",
            "parameters": {
                "worker_id": "str"
            },
            "returns": "str"
        }