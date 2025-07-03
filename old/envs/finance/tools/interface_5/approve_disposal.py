import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from datetime import datetime

class ApproveDisposal(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        disposal_id: str,
        approved_by: str
    ) -> str:
        disposals = data.get("disposals")
        assets = data.get("assets")
        
        if disposal_id not in disposals:
            raise ValueError(f"Disposal {disposal_id} not found.")
          
        disp = disposals[disposal_id]
        aid = disp.get("asset_id")
        if aid and aid in assets:
            bv = disp.get("book_value_at_disposal",0)
            if disp.get("tax_treatment") == "capital_gain" and disp.get("proceeds", 0) < bv:
                raise ValueError("Proceeds must exceed book value for capital gain.")
            disp["approved_by"] = approved_by
            disp["approved_at"] = "2025-01-01T00:00:00Z"
            # update GL account
            disp["gl_account"] = "FIXED_ASSET_DISPOSAL" if disp.get("tax_treatment")=="capital_gain" else "FIXED_ASSET_LOSS"
            return json.dumps(disp)
          
        raise ValueError("Associated asset not found or already orphaned.")

    @staticmethod
    def get_info() -> Dict[str,Any]:
        return {
            "type": "function",
            "function": {
                "name": "approve_disposal",
                "description": "Approve a disposal and update its accounting.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "disposal_id": {"type": "string"},
                        "approved_by": {"type": "string"}
                    },
                    "required": ["disposal_id", "approved_by"]
                }
            }
        }