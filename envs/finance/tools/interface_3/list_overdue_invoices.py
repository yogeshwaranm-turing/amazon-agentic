import json
from datetime import datetime, timezone
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListOverdueInvoices(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any], 
        as_of_date: str = None
    ) -> str:
        invs = data.get("invoices", {})
        today = as_of_date or datetime.now(timezone.utc).date().isoformat() 
        overdue: List[Dict[str,Any]] = []
        
        for inv in invs.values():
            if inv.get("status") == "overdue" and inv.get("due_date") < today:
                overdue.append(inv)

        return json.dumps(overdue)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"list_overdue_invoices",
            "description":"List invoices past due date.",
            "parameters":{
                "type":"object",
                "properties":{"as_of_date":{"type":"string","format":"date"}}
            }
        }}