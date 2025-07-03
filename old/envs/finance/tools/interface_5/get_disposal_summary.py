import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetDisposalSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], start_date: str, end_date: str) -> str:
        dsps = data.get("disposals", {})
        summary = []
        for d in dsps.values():
            if start_date <= d.get("disposed_at")[:10] <= end_date:
                summary.append({
                  "disposal_id": d.get("disposal_id"), 
                  "asset_id": d.get("asset_id"), 
                  "proceeds": d.get("proceeds"), 
                  "gain_or_loss": d.get("gain_or_loss")
                })
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "get_disposal_summary",
            "description": "List disposal events and financial impact between dates.",
            "parameters": {
              "type": "object",
              "properties": {
                "start_date": { "type": "string", "format": "date" },
                "end_date": { "type": "string", "format": "date" }
              },
              "required": ["start_date", "end_date"]
            }
          }
        }
