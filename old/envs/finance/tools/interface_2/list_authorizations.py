import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListAuthorizations(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      account_id: str, 
      status: str = None
    ) -> str:
        auths = data.get("authorizations", {}).values()
        result = [a for a in auths if a.get("account_id") == account_id]
        
        if status:
            result = [a for a in result if a.get("status") == status]
            
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
              "name": "list_authorizations",
              "description": "Retrieve authorizations for an account.",
              "parameters": {
                  "type": "object",
                  "properties": {
                    "account_id": {
                      "type": "string"
                    },
                    "status": {
                      "type": "string"
                    }
                  },
                  "required": ["account_id"]
              }
            }
        }