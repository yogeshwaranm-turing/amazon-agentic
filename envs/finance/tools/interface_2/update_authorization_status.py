import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateAuthorizationStatus(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      auth_id: str, 
      status: str
    ) -> str:
        auths = data.get("authorizations", {})
        auth = auths.get(auth_id)
        
        if not auth:
            raise KeyError(f"Authorization {auth_id} not found")
          
        auth["status"] = status
        auth["authorized_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(auth)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"update_authorization_status",
            "description":"Capture, expire, or void an existing authorization.",
            "parameters":{
                "type":"object",
                "properties":{ "auth_id":{"type":"string"}, "status":{"type":"string"} },
                "required":["auth_id","status"]
            }
        }}