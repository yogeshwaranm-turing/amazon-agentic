import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class CaptureAuthorization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        auth_id: str, 
        capture_amount: float
    ) -> str:
        auths = data["authorizations"]
        auth = auths.get(auth_id)
        
        if not auth:
            raise Exception("NotFound")
        
        if auth["amount"] < capture_amount:
            raise Exception("CaptureAmountExceedsAuthorization")
        
        auth["status"] = "captured"
        auth["capture_details"]["captured_at"] = datetime.now(timezone.utc).isoformat()
        auth["capture_details"]["captured_amount"] = capture_amount
        
        return json.dumps(auth)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "capture_authorization",
                "description": "Capture a pending authorization.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "auth_id": {
                            "type": "string"
                        },
                        "capture_amount": {
                            "type": "number"
                        }
                    },
                    "required": ["auth_id", "capture_amount"]
                }
            }
        }