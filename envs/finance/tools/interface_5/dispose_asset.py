import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DisposeAsset(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        asset_id: str,
        disposed_at: str,
        proceeds: float,
        disposal_method: str = "unknown",
        disposal_reason: str = "unknown",
        notes: Optional[str] = None
    ) -> str:
        # Validate presence of assets and disposals structures
        assets = data.get("assets")
        disposals = data.get("disposals")
        if not isinstance(assets, dict):
            raise ValueError("Assets data is not in the expected format.")
        if not isinstance(disposals, dict):
            raise ValueError("Disposals data is not in the expected format.")

        # Check that the asset exists
        if asset_id not in assets:
            raise ValueError(f"Asset ID {asset_id} does not exist in the asset data.")

        # Validate disposed_at timestamp
        if not disposed_at:
            raise ValueError("Disposed at date must be provided.")
        
        # Use the disposed_at parameter directly (assuming it's already in ISO format)
        disposed_dt = disposed_at

        # Validate proceeds value
        if not isinstance(proceeds, (int, float)) or proceeds < 0:
            raise ValueError("Proceeds must be a non-negative number.")

        # Generate a unique disposal ID based on disposed_at date and quarter
        quarter = (int(disposed_at[5:7]) - 1) // 3 + 1
        disp_id = f"DISP-{asset_id}-{disposed_at[:4]}Q{quarter}"

        # Create the disposal record
        record = {
            "disposal_id": disp_id,
            "asset_id": asset_id,
            "disposed_at": disposed_dt,
            "disposal_method": disposal_method,
            "disposal_reason": disposal_reason,
            "sale_details": None,
            "proceeds": proceeds,
            "book_value_at_disposal": 0.0,
            "gain_or_loss": -proceeds,
            "gl_account": "FIXED_ASSET_LOSS",
            "tax_treatment": "ordinary_loss",
            "approved_by": None,
            "approved_at": None,
            "notes": notes
        }
        # Store disposal record
        disposals[disp_id] = record

        # Update the asset's status and disposal details
        asset = assets[asset_id]
        asset["status"] = "disposed"
        asset["disposal_date"] = disposed_dt
        asset["disposal_proceeds"] = proceeds

        return json.dumps(record)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "dispose_asset",
                "description": "Record disposal of an asset and update its status.",
                "parameters": {
                "type": "object",
                "properties": {
                    "asset_id": { "type": "string" },
                    "disposed_at": {
                        "type": "string",
                        "description": "ISO format timestamp."
                    },
                    "proceeds": { "type": "number" },
                    "disposal_method": {
                        "type": "string",
                        "description": "Method of disposal (e.g., donation, trade-in, scrap, sale).",
                        "enum": ["donation", "trade-in", "scrap", "sale", "unknown"]
                    },
                    "disposal_reason": {
                        "type": "string",
                        "description": "Reason for disposal."
                    },
                    "notes": {
                        "type": "string",
                        "description": "Optional notes about the disposal."
                    }
                },
                "required": ["asset_id", "disposed_at", "proceeds"]
                }
            }
        }
