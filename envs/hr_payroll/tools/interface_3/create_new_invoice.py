
import json
import uuid
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateNewInvoice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], contract_id: str, amount: float, due_date: str) -> str:
        contracts = data.get("contracts", {})
        if contract_id not in contracts:
            raise ValueError("Contract not found")

        worker_id = contracts[contract_id]["worker_id"]
        org_id = contracts[contract_id]["organization_id"]

        invoices = data.setdefault("invoices", {})
        invoice_id = str(uuid.uuid4())
        invoices[invoice_id] = {
            "worker_id": worker_id,
            "organization_id": org_id,
            "issue_date": "2025-07-01",
            "due_date": due_date,
            "amount": round(amount, 2),
            "status": "issued",
            "currency": contracts[contract_id]["currency"]
        }

        return json.dumps({"invoice_id": invoice_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_new_invoice",
                "description": "Generates a new invoice based on a contract",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "The ID of the contract for which the invoice is issued"
                        },
                        "amount": {
                            "type": "number",
                            "description": "The total amount to invoice"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "The due date for the invoice in YYYY-MM-DD format"
                        }
                    },
                    "required": ["contract_id", "amount", "due_date"]
                }
            }
        }
