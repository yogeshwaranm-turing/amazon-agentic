import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateRefundStatus(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      refund_id: str, 
      status: str
    ) -> str:
        refs = data.get("refunds", {})
        ref = refs.get(refund_id)
        
        if not ref:
            raise KeyError(f"Refund {refund_id} not found")
          
        ref["status"] = status
        ref["processed_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(ref)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"update_refund_status",
            "description":"Change refund status (e.g. pending → completed).",
            "parameters":{
                "type":"object",
                "properties":{
                    "refund_id":{"type":"string"},
                    "status":{"type":"string"}
                },
                "required":["refund_id","status"]
            }
        }}