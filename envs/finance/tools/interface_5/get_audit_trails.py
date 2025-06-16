import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetAuditTrails(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        entity: str, 
        entity_id: str, 
        limit: int = 20
    ) -> str:
        trails = data["audit_trails"].values()
        
        if not trails:
            raise Exception("NoAuditTrailsFound")
        
        if not entity or not entity_id:
            raise Exception("EntityAndEntityIdRequired")
        
        if not isinstance(entity, str) or not isinstance(entity_id, str):
            raise Exception("InvalidEntityOrEntityIdType")
        
        if not isinstance(trails, List):
            raise Exception("InvalidAuditTrailsDataType")
        
        # Filter trails by entity and entity_id
        if not isinstance(limit, int) or limit <= 0:
            raise Exception("InvalidLimitType")
        
        filtered = [t for t in trails if t.get("entity") == entity and t.get("entity_id") == entity_id]
        filtered.sort(key=lambda x: x.get("performed_at"), reverse=True)
        
        return json.dumps(filtered[:limit])

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_audit_trails",
                "description": "Fetch recent audit trails for an entity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity": {
                            "type": "string"
                        },
                        "entity_id": {
                            "type": "string"
                        },
                        "limit": {
                            "type": "integer"
                        }
                    },
                    "required": ["entity", "entity_id"]
                }
            }
        }