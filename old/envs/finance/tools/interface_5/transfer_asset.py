import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class TransferAsset(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        asset_id: str,
        from_user: str,
        to_user: str,
        notes: str = None
    ) -> str:
        assets = data.get("assets")
        users = data.get("users")
        
        if not all(isinstance(d, dict) for d in [assets, users]):
            raise ValueError("Data format is not as expected.")
          
        if asset_id not in assets:
            raise ValueError(f"Asset {asset_id} not found.")
          
        if from_user not in users or to_user not in users:
            raise ValueError("One or both users not found.")
          
        if assets[asset_id].get("user_id") != from_user:
            raise ValueError("Asset is not currently assigned to from_user.")
          
        # Transfer
        assets[asset_id]["user_id"] = to_user

        return json.dumps({
            "asset_id": asset_id,
            "from_user": from_user,
            "to_user": to_user,
            "notes": notes
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_asset",
                "description": "Move an asset from one user to another.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "asset_id": {"type": "string"},
                        "from_user": {"type": "string"},
                        "to_user": {"type": "string"},
                        "notes": {"type": "string"}
                    },
                    "required": ["asset_id","from_user","to_user"]
                }
            }
        }