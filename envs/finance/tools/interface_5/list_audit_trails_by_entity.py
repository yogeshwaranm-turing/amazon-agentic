import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListAuditTrailsByEntity(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      entity: str, 
      entity_id: str
    ) -> str:
        trails = data.get("audit_trails", {})
        
        results: List[Dict[str, Any]] = [a for a in trails.values() if a.get("entity") == entity and a.get("entity_id") == entity_id]
        
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "list_audit_trails_by_entity",
            "description": "Fetch audit trail entries for a specific entity and ID.",
            "parameters": {
              "type": "object",
              "properties": {
                "entity": { "type": "string" },
                "entity_id": { "type": "string" }
              },
              "required": ["entity", "entity_id"]
            }
          }
        }
