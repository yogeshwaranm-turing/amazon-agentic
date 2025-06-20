import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetDepreciationSchedule(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        asset_id: str
    ) -> str:
        deps = data.get("depreciations", {}).values()
        
        if not deps:
            raise Exception("NoDepreciationEntriesFound")
        
        if not asset_id:
            raise Exception("AssetIdRequired")
        
        if not isinstance(asset_id, str):
            raise Exception("InvalidAssetIdType")
        
        schedule = [d for d in deps if d.get("asset_id") == asset_id]
        
        return json.dumps(schedule)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_depreciation_schedule",
                "description": "Retrieve depreciation entries for an asset.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "asset_id": {
                            "type": "string"
                        }
                    },
                    "required": ["asset_id"]
                }
            }
        }