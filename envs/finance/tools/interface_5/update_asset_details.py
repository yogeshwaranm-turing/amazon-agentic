import json
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
        asset["updated_at"] = "2025-06-15T15:00:00"
        
        return json.dumps(asset)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_asset_details",
                "description": "Modify fields on an existing asset.",
                "parameters": {
                "type": "object",
                "properties": {
                    "asset_id": { "type": "string" },
                    "updates": { 
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["active", "disposed", "maintenance"],
                                "description": "The status of the asset to update to"
                            },
                            "name": {
                                "type": "string"
                            },
                            "description": {
                                "type": "string"
                            },
                            "location": {
                                "type": "string"
                            },
                            "department": {
                                "type": "string"
                            },
                            "vendor": {
                                "type": "string"
                            },
                            "salvage_value": {
                                "type": "number"
                            },
                            "useful_life_years": {
                                "type": "number"
                            },
                            "depreciation_method": {
                                "type": "string",
                                "enum": ["straight_line", "double_declining"]
                            },
                            "current_book_value": {
                                "type": "number"
                            },
                            "maintenance_schedule": {
                                "type": "object",
                                "properties": {
                                    "last_maintenance": {
                                        "type": "string",
                                        "format": "date"
                                    },
                                    "next_due": {
                                        "type": "number",
                                        "format": "date"
                                    }
                                }
                            }
                        }
                    }
                },
                "required": ["asset_id", "updates"]
                }
            }
        }
