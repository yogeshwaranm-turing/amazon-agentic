import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from datetime import datetime

class DisposeAsset(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        asset_id: str, 
        disposed_at: str, 
        proceeds: float
    ) -> str:
        disposals = data["disposals"]
        
        if not isinstance(disposals, dict):
            raise ValueError("Disposal data is not in the expected format.")
        
        if asset_id not in data["assets"]:
            raise ValueError(f"Asset ID {asset_id} does not exist in the asset data.")
        
        if not disposed_at:
            raise ValueError("Disposed at date must be provided.")
        try:
            disposed_at = datetime.fromisoformat(disposed_at)
        except ValueError:
            raise ValueError("Disposed at date must be in ISO format (YYYY-MM-DDTHH:MM:SS).")
        
        if not isinstance(proceeds, (int, float)) or proceeds < 0:
            raise ValueError("Proceeds must be a non-negative number.")
        
        current_time = datetime.now()
        quarter = (current_time.month - 1) // 3 + 1
        disp_id = f"DISP-{asset_id}-{current_time.year}Q{quarter}"
        
        record = {
            "disposal_id": disp_id,
            "asset_id": asset_id,
            "disposed_at": disposed_at,
            "disposal_method": "unknown",
            "disposal_reason": "unknown",
            "sale_details": None,
            "proceeds": proceeds,
            "book_value_at_disposal": 0.0,
            "gain_or_loss": -proceeds,
            "gl_account": "FIXED_ASSET_LOSS",
            "tax_treatment": "ordinary_loss",
            "approved_by": None,
            "approved_at": None,
            "notes": None
        }
        disposals[disp_id] = record
        
        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "dispose_asset",
                "description": "Record disposal of an asset.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "asset_id": {
                            "type": "string"
                        },
                        "disposed_at": {
                            "type": "string"
                        },
                        "proceeds": {
                            "type": "number"
                        }
                    },
                    "required": ["asset_id", "disposed_at", "proceeds"]
                }
            }
        }