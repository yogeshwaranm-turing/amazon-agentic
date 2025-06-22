import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteDepreciationEntry(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        depreciation_id: str
    ) -> str:
        depreciations = data.get("depreciations")
        assets = data.get("assets")
        
        if depreciation_id not in depreciations:
            raise ValueError(f"Depreciation {depreciation_id} not found.")
          
        dep = depreciations.pop(depreciation_id)
        asset_id = dep.get("asset_id")
        if asset_id not in assets:
            raise ValueError("Associated asset not found.")
          
        # Recalculate from purchase cost
        asset = assets[asset_id]
        bv = asset.get("cost")
        remaining = sorted(
            [d for d in depreciations.values() if d.get("asset_id")==asset_id],
            key=lambda x: x.get("fiscal_year")
        )
        for d in remaining:
            rate = d.get("depreciation_rate")
            amt = bv * rate
            d["book_value_start"] = bv
            d["amount"] = amt
            d["book_value_end"] = bv - amt
            d["accumulated_depreciation"] = d.get("accumulated_depreciation", 0)
            bv -= amt
        asset["current_book_value"] = bv
        
        return json.dumps({"deleted": depreciation_id})

    @staticmethod
    def get_info() -> Dict[str,Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_depreciation_entry",
                "description": "Remove a depreciation entry and reconcile book values.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "depreciation_id": {"type": "string"}
                    },
                    "required": ["depreciation_id"]
                }
            }
        }