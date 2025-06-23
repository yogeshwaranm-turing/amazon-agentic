import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateNextDepreciation(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        asset_id: str
    ) -> str:
        assets = data.get("assets")
        
        if asset_id not in assets:
            raise ValueError(f"Asset {asset_id} not found.")
          
        asset = assets[asset_id]
        bv = asset.get("current_book_value",0)
        life = asset.get("useful_life_years")
        method = asset.get("depreciation_method")
        rate = (1/life) if method=="straight_line" else (2/life)
        amt = bv * rate
        ref = f"JE-2025-{asset_id}"
        result = {"amount": amt, "journal_entry_ref": ref}
        
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str,Any]:
        return {
            "type": "function",
            "function": {
                "name": "calculate_next_depreciation",
                "description": "Compute the next depreciation amount and reference.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "asset_id": {"type": "string"}
                    },
                    "required":["asset_id"]
                }
            }
        }