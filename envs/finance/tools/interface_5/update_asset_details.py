import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateAssetDetails(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      asset_id: str, 
      updates: Dict[str, Any]
    ) -> str:
        assets = data.get("assets", {})
        asset = assets.get(asset_id)
        
        if not asset:
            raise KeyError(f"Asset {asset_id} not found")
          
        asset.update(updates)
        asset["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(asset)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"update_asset_details",
            "description":"Modify fields on an existing asset.",
            "parameters":{
                "type":"object",
                "properties":{ "asset_id":{"type":"string"}, "updates":{"type":"object","additionalProperties":"true"} },
                "required":["asset_id","updates"]
            }
        }}