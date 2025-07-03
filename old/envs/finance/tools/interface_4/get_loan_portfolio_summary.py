import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GetLoanPortfolioSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        lns = data.get("loans", {})
        summary: Dict[str, Any] = {"active":0,"paid_off":0,"total_principal":0.0}
        
        for l in lns.values():
            status = l.get("status")
            summary.setdefault(status, 0)
            summary[status] += 1
            summary["total_principal"] += l.get("principal_amount",0.0)
            
        return json.dumps(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
          "type": "function",
          "function": {
            "name": "get_loan_portfolio_summary",
            "description": "Aggregate loan counts and total principal by status.",
            "parameters": { "type": "object", "properties": {} }
          }
        }
