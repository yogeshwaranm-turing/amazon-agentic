import json
from datetime import datetime, timezone
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class UpdateInvoiceDetails(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      invoice_id: str, 
      updates: Dict[str, Any]
    ) -> str:
        invs = data["invoices"]
        inv = invs.get(invoice_id)
        
        if not inv:
            raise KeyError(f"Invoice {invoice_id} not found")
          
        inv.update(updates)
        inv["issued_at"] = datetime.now(timezone.utc).isoformat()
        
        return json.dumps(inv)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"update_invoice_details",
                "description":"Modify invoice fields.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "invoice_id":{"type":"string"},
                        "updates":{"type":"object","additionalProperties":"true"}
                    },
                    "required":["invoice_id","updates"]
                }
            }
        }