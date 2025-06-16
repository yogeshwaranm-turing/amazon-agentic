import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListRefundsByReason(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      reason: str
    ) -> str:
        refs = data.get("refunds", {})
        
        results: List[Dict[str, Any]] = [r for r in refs.values() if r.get("reason") == reason]
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "list_refunds_by_reason",
            "description": "Return refunds filtered by reason.",
            "parameters": {
              "type": "object",
              "properties": { "reason": { "type": "string" } },
              "required": ["reason"]
            }
          }
        }
