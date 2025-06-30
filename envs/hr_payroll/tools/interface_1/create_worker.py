import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CreateWorker(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        organization_id: str,
        worker_type: str
    ) -> str:
        users = data.get("users", {})
        organizations = data.get("organizations", {})
        workers = data.setdefault("workers", {})

        if user_id not in users:
            raise ValueError(f"User ID '{user_id}' not found.")

        if organization_id not in organizations:
            raise ValueError(f"Organization ID '{organization_id}' not found.")

        if worker_type not in ["employee", "contractor"]:
            raise ValueError("worker_type must be 'employee' or 'contractor'.")

        # Generate unique worker_id
        def generate_worker_id():
            base = "wrk_10000_"
            suffix = 0
            while f"{base}{suffix}" in workers:
                suffix += 1
            return f"{base}{suffix}"

        worker_id = generate_worker_id()
        now = datetime.now(timezone.utc).isoformat()

        new_worker = {
            "user_id": user_id,
            "organization_id": organization_id,
            "worker_type": worker_type,
            "status": "active",
            "created_at": now,
            "updated_at": now
        }

        workers[worker_id] = new_worker
        return json.dumps({**new_worker, "worker_id": worker_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_worker",
                "description": "Create a worker record for a user tied to an organization.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID of an existing user."
                        },
                        "organization_id": {
                            "type": "string",
                            "description": "ID of a valid organization."
                        },
                        "worker_type": {
                            "type": "string",
                            "enum": ["employee", "contractor"],
                            "description": "Type of worker being created."
                        }
                    },
                    "required": ["user_id", "organization_id", "worker_type"]
                }
            }
        }
