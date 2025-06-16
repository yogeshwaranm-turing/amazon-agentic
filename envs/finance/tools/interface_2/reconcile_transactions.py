import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ReconcileTransactions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        # simplistic match refunds to reversed txns and deposits to credit txns
        txns = data.get("transactions", {})
        refunds = data.get("refunds", {})
        matched: List[Dict[str,Any]] = []
        
        for ref in refunds.values():
            txn = txns.get(ref["transaction_id"])
            if txn and txn.get("status")=="reversed":
                matched.append({"refund_id": ref["refund_id"], "transaction_id": txn["transaction_id"]})
                
        return json.dumps(matched)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{
            "name":"reconcile_transactions",
            "description":"Match refunds to reversed transactions for reconciliation.",
            "parameters":{ "type":"object", "properties":{} }
        }}