import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool



class RemovePermissionFromGroup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], space_id: int, group_id: int, permission_id: int) -> str:
        space_permissions = data.get("space_permissions", [])
        before = len(space_permissions)
        space_permissions[:] = [
            p for p in space_permissions if not (
                p["space_id"] == space_id and
                p["subject_type"] == "group" and
                p["subject_id"] == group_id and
                p["permission_id"] == permission_id
            )
        ]
        after = len(space_permissions)
        return json.dumps({
            "status": "removed" if before != after else "not_found",
            "space_id": space_id,
            "group_id": group_id,
            "permission_id": permission_id
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_permission_from_group",
                "description": "Remove a permission from a group in a space",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "space_id": {"type": "integer"},
                        "group_id": {"type": "integer"},
                        "permission_id": {"type": "integer"}
                    },
                    "required": ["space_id", "group_id", "permission_id"]
                }
            }
        }
