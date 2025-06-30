import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class DeleteUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        user_id: str,
        reason: str
    ) -> str:
        users = data.get("users", {})
        workers = data.get("workers", {})

        if user_id not in users:
            raise ValueError(f"User '{user_id}' not found.")

        # Ensure user is not linked to a worker
        for worker in workers.values():
            if worker.get("user_id") == user_id:
                raise ValueError(f"Cannot delete user '{user_id}' — associated with worker '{worker.get('worker_id')}'.")

        deleted_user = users.pop(user_id)

        audit_entry = {
            "deleted_user": deleted_user,
            "deleted_at": "2025-06-30T09:25:07.726505Z",
            "reason": reason
        }

        return json.dumps(audit_entry)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_user",
                "description": "Delete a user if not associated with any worker profile. Otherwise, raise an error.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The unique ID of the user to delete."
                        },
                        "reason": {
                            "type": "string",
                            "description": "Reason for deletion for audit purposes."
                        }
                    },
                    "required": ["user_id", "reason"]
                }
            }
        }
