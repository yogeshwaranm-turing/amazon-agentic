import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteAsset(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        asset_id: str
    ) -> str:
        assets = data.get("assets")
        depreciations = data.get("depreciations")
        disposals = data.get("disposals")
        
        if not isinstance(assets, dict):
            raise ValueError("Assets data is not in expected format.")
          
        if asset_id not in assets:
            raise ValueError(f"Asset ID {asset_id} does not exist.")
          
        # Soft-delete asset
        assets[asset_id]["status"] = "archived"
        
        # Cascade related entries to orphan state
        for dep in depreciations.values():
            if dep.get("asset_id") == asset_id:
                dep["asset_id"] = None
                
        for disp in disposals.values():
            if disp.get("asset_id") == asset_id:
                disp["asset_id"] = None
                
        return json.dumps({"asset_id": asset_id, "status": "archived"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_asset",
                "description": "Soft-delete an asset by archiving it and orphaning its related records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "asset_id": {"type": "string"}
                    },
                    "required": ["asset_id"]
                }
            }
        }