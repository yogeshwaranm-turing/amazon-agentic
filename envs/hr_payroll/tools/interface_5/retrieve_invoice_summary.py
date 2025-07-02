
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool
from collections import defaultdict

class RetrieveInvoiceSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        invoices = data.get("invoices", {})
        summary = defaultdict(float)
        for invoice in invoices.values():
            org_id = invoice["organization_id"]
            summary[org_id] += invoice.get("amount", 0)
        return json.dumps(dict(summary))

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_invoice_summary",
                "description": "Fetches total invoice amounts grouped by organization",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
