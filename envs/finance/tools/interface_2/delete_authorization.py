import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteAuthorization(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      auth_id: str
    ) -> str:
        auths = data.get("authorizations", {})
        auth = auths.pop(auth_id, None)
        
        if not auth:
            raise KeyError(f"Authorization {auth_id} not found")
          
        auth["status"] = "voided"
        
        return json.dumps(auth)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"delete_authorization",
            "description":"Remove an authorization hold.",
            "parameters":{
                "type":"object",
                "properties":{ "auth_id":{"type":"string"} },
                "required":["auth_id"]
            }
        }}