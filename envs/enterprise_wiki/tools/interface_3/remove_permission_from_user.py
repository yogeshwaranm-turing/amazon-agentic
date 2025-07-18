import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class RemovePermissionFromUser(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int, user_id: int, permission_id: int) -> str:
        space_permissions = data.get("space_permissions", [])
        before = len(space_permissions)
        space_permissions[:] = [
            p for p in space_permissions if not (
                str(p["space_id"]) == str(space_id) and
                p["subject_type"] == "user" and
                str(p["subject_id"]) == str(user_id) and
                str(p["permission_id"]) == str(permission_id)
            )
        ]
        after = len(space_permissions)
        return json.dumps({
            "status": "removed" if before != after else "not_found",
            "space_id": space_id,
            "user_id": user_id,
            "permission_id": permission_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_permission_from_user",
                "description": "Remove a permission from a user in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "permission_id": {"type": "integer"}
                    },
                    "required": ["space_id", "user_id", "permission_id"]
                }
            }
        }
