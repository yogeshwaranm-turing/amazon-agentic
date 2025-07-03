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
                        "updates":{
                            "type":"object",
                            "properties": {
                                "status": {
                                    "type": "string",
                                    "enum": ["cancelled", "issued", "overdue", "paid"],
                                    "description": "The status of the invoice to update to"
                                },
                                "tax_rate": {
                                    "type": "number"
                                },
                                "notes": {
                                    "type": "string"
                                },
                                "line_items": {
                                    "type": "object",
                                    "properties": {
                                        "description": {
                                            "type": "string"
                                        },
                                        "quantity": {
                                            "type": "number"
                                        },
                                        "unit_price": {
                                            "type": "number"
                                        },
                                        "line_total": {
                                            "type": "number"
                                        }
                                    }
                                },
                                "billing_address": {
                                    "type": "object",
                                    "properties": {
                                        "street": {
                                            "type": "string"
                                        },
                                        "city": {
                                            "type": "string"
                                        },
                                        "state": {
                                            "type": "string"
                                        },
                                        "postal_code": {
                                            "type": "string"
                                        },
                                        "country": {
                                            "type": "string"
                                        }
                                    }
                                },
                            }
                        }
                    },
                    "required":["invoice_id","updates"]
                }
            }
        }