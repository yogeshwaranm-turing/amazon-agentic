import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListAssetsByCategory(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      category: str
    ) -> str:
        assets = data.get("assets", {})
        
        results: List[Dict[str, Any]] = [a for a in assets.values() if a.get("category") == category]
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "list_assets_by_category",
            "description": "Return all assets matching a given category.",
            "parameters": {
              "type": "object",
              "properties": { "category": { "type": "string" } },
              "required": ["category"]
            }
          }
        }
