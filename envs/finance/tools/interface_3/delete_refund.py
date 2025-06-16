import json
from typing import Any, Dict
from datetime import datetime, timezone
from tau_bench.envs.tool import Tool

class DeleteRefund(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      refund_id: str
    ) -> str:
        refs = data.get("refunds", {})
        ref = refs.pop(refund_id, None)
        
        if not ref:
            raise KeyError(f"Refund {refund_id} not found")
          
        ref["status"] = "voided"
        ref["processed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        return json.dumps(ref)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"delete_refund",
            "description":"Void an existing refund entry.",
            "parameters":{
                "type":"object",
                "properties":{ "refund_id":{"type":"string"} },
                "required":["refund_id"]
            }
        }}