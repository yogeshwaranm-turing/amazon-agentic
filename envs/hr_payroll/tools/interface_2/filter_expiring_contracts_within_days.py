from tau_bench.envs.tool import Tool
from typing import Any, Dict, List
from datetime import datetime, timedelta

class FilterExpiringContractsWithinDays(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], contracts: List[str], days: int) -> List[str]:
        result = []
        today = datetime.utcnow().date()
        deadline = today + timedelta(days=days)
        for contract_id in contracts:
            contract = data["contracts"].get(contract_id)
            if not contract or contract.get("status") != "active":
                continue
            end_date = datetime.strptime(contract["end_date"], "%Y-%m-%d").date()
            if today <= end_date <= deadline:
                result.append(contract_id)
        return result

    @staticmethod
    def get_info():
        return {
            "name": "filter_expiring_contracts_within_days",
            "description": "Filters active contracts that are expiring within the given number of days.",
            "parameters": {
                "contracts": "List[str]",
                "days": "int"
            },
            "returns": "List[str]"
        }