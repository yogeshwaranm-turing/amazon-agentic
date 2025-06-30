import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class CreateWorker(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        worker_id: str,
        user_id: str,
        organization_id: str,
        worker_type: str,
        title: str
    ) -> str:
        users = data.get("users", {})
        organizations = data.get("organizations", {})
        workers = data.setdefault("workers", {})

        if worker_id in workers:
            raise ValueError(f"Worker ID '{worker_id}' already exists.")

        if user_id not in users:
            raise ValueError(f"User ID '{user_id}' not found.")

        if organization_id not in organizations:
            raise ValueError(f"Organization ID '{organization_id}' not found.")

        if worker_type not in ["employee", "contractor"]:
            raise ValueError("worker_type must be 'employee' or 'contractor'.")

        worker = {
            "worker_id": worker_id,
            "user_id": user_id,
            "organization_id": organization_id,
            "worker_type": worker_type,
            "title": title,
            "status": "active",
            "created_at": "2025-06-30T09:25:07.658835Z",
            "updated_at": "2025-06-30T09:25:07.658835Z"
        }
        workers[worker_id] = worker
        return json.dumps(worker)

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
                        "worker_id": {"type": "string", "description": "Unique ID for the worker."},
                        "user_id": {"type": "string", "description": "ID of an existing user."},
                        "organization_id": {"type": "string", "description": "ID of a valid organization."},
                        "worker_type": {
                            "type": "string",
                            "enum": ["employee", "contractor"],
                            "description": "Type of worker being created."
                        },
                        "title": {"type": "string", "description": "Job title or role description."}
                    },
                    "required": ["worker_id", "user_id", "organization_id", "worker_type", "title"]
                }
            }
        }
