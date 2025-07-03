import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateDepreciationEntry(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        depreciation_id: str,
        new_amount: float
    ) -> str:
        depreciations = data.get("depreciations")
        assets = data.get("assets")
        
        if depreciation_id not in depreciations:
            raise ValueError(f"Depreciation {depreciation_id} not found.")
          
        dep = depreciations[depreciation_id]
        asset_id = dep.get("asset_id")
        
        if asset_id not in assets:
            raise ValueError("Associated asset not found.")
          
        # update amount and recalculate rate
        dep["amount"] = new_amount
        dep["depreciation_rate"] = new_amount / dep.get("book_value_start",1)
        
        # re-reconcile subsequent entries
        bv = dep.get("book_value_start") - new_amount
        sorted_deps = sorted(
            [d for d in depreciations.values() if d.get("asset_id")==asset_id],
            key=lambda x: x.get("fiscal_year")
        )
        for d in sorted_deps:
            old_amount = d.get("amount", 0)
            if d.get("depreciation_id") == depreciation_id:
                d["book_value_end"] = bv
            elif d.get("fiscal_year") >= dep.get("fiscal_year"):
                amt = bv * d.get("depreciation_rate")
                d["amount"] = amt
                d["book_value_start"] = bv
                d["accumulated_depreciation"] = amt + (d.get("accumulated_depreciation", 0) - old_amount)
                bv = bv - amt
                d["book_value_end"] = bv
        assets[asset_id]["current_book_value"] = bv
        
        return json.dumps(dep)

    @staticmethod
    def get_info() -> Dict[str,Any]:
        return {
            "type": "function",
            "function": {
                "name": "update_depreciation_entry",
                "description": "Modify a depreciation entry and reconcile book values.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "depreciation_id": {"type": "string"},
                        "new_amount": {"type": "number"}
                    },
                    "required": [
                        "depreciation_id",
                        "new_amount"
                    ]
                }
            }
        }