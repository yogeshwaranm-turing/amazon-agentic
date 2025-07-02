import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AssignAssetToUser(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        asset_id: str,
        user_id: str,
        notes: str = None
    ) -> str:
        assets = data.get("assets")
        users = data.get("users")
        
        if not isinstance(assets, dict) or not isinstance(users, dict):
            raise ValueError("Data format is not as expected.")
          
        if asset_id not in assets:
            raise ValueError(f"Asset {asset_id} not found.")
          
        if user_id not in users:
            raise ValueError(f"User {user_id} not found.")
          
        # Update assignment
        assets[asset_id]["user_id"] = user_id
        
        return json.dumps({
            "asset_id": asset_id,
            "user_id": user_id,
            "assigned_at": "2025-01-01T00:00:00Z",
            "notes": notes
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "assign_asset_to_user",
                "description": "Link an asset to a user, allowing the user to manage the asset.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "asset_id": {"type": "string"},
                        "user_id": {"type": "string"},
                        "notes": {"type": "string"},
                    },
                    "required": ["asset_id", "user_id"]
                }
            }
        }