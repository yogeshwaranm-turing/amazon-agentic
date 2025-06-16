import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class VoidAuthorization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        auth_id: str
    ) -> str:
        auths = data["authorizations"]
        auth = auths.get(auth_id)
        
        if not auth:
            raise Exception("NotFound")
        
        auth["status"] = "voided"
        auth["voided_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(auth)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "void_authorization",
                "description": "Void a pending authorization.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "auth_id": {
                            "type": "string"
                        }
                    },
                    "required": ["auth_id"]
                }
            }
        }