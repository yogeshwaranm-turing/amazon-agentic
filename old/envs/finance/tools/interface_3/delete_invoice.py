import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DeleteInvoice(Tool):
    @staticmethod
    def invoke(
      data: Dict[str, Any], 
      invoice_id: str
    ) -> str:
        invs = data["invoices"]
        inv = invs.pop(invoice_id, None)
        
        if not inv:
            raise KeyError(f"Invoice {invoice_id} not found")
          
        inv["status"] = "cancelled"
        
        return json.dumps(inv)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"delete_invoice",
                "description":"Cancel (void) an invoice.",
                "parameters":{
                    "type":"object",
                    "properties":{"invoice_id":{"type":"string"}},
                    "required":["invoice_id"]
                }
            }
        }