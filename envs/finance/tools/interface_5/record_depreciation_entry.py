import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RecordDepreciationEntry(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        asset_id: str,
        fiscal_year: int,
        fiscal_period: str,
        period_start: str,
        period_end: str
    ) -> str:
        assets = data.get("assets")
        depreciations = data.setdefault("depreciations", {})
        
        if asset_id not in assets:
            raise ValueError(f"Asset {asset_id} not found.")
          
        asset = assets[asset_id]
        bv_start = asset.get("current_book_value", 0)
        life = asset.get("useful_life_years")
        method = asset.get("depreciation_method")
        
        if method == "straight_line":
            rate = 1 / life
        else:
            rate = 2 / life
            
        amount = bv_start * rate
        # determine previous accumulated
        prev_acc = 0
        for dep in depreciations.values():
            if dep.get("asset_id") == asset_id and dep.get("fiscal_year") == fiscal_year:
                prev_acc += dep.get("amount",0)
                
        acc_dep = prev_acc + amount
        bv_end = bv_start - amount
        dep_id = f"DEP-{asset_id}-{fiscal_year}"
        record = {
            "depreciation_id": dep_id,
            "asset_id": asset_id,
            "fiscal_year": fiscal_year,
            "fiscal_period": fiscal_period,
            "period_start": period_start,
            "period_end": period_end,
            "method": method,
            "depreciation_rate": rate,
            "amount": amount,
            "accumulated_depreciation": acc_dep,
            "book_value_start": bv_start,
            "book_value_end": bv_end,
            "salvage_value": asset.get("salvage_value"),
            "journal_entry_ref": f"JE-{fiscal_year}-{asset_id}"
        }
        
        depreciations[dep_id] = record
        asset["current_book_value"] = bv_end
        
        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"record_depreciation_entry",
                "description":"Add a depreciation entry and update book value.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "asset_id":{"type":"string"},
                        "fiscal_year":{"type":"integer"},
                        "fiscal_period":{"type":"string"},
                        "period_start":{"type":"string"},
                        "period_end":{"type":"string"}
                    },
                    "required":["asset_id","fiscal_year","fiscal_period","period_start","period_end"]
                }
            }
        }