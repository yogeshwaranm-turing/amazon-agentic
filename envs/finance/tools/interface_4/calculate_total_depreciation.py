import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CalculateTotalDepreciation(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      asset_id: str, 
      start_period: str, 
      end_period: str
    ) -> str:
        deps = data.get("depreciations", {})
        
        total = 0.0
        for d in deps.values():
            if d.get("asset_id") == asset_id and start_period <= d.get("period_start") <= end_period:
                total += d.get("amount", 0.0)
                
        return json.dumps(
          {
            "asset_id": asset_id, 
            "total_depreciation": total, 
            "start_period": start_period, 
            "end_period": end_period
          }
        )

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "calculate_total_depreciation",
            "description": "Sum depreciation amounts for an asset within a date range.",
            "parameters": {
              "type": "object",
              "properties": {
                "asset_id": { "type": "string" },
                "start_period": { "type": "string", "format": "date" },
                "end_period": { "type": "string", "format": "date" }
              },
              "required": ["asset_id", "start_period", "end_period"]
            }
          }
        }
