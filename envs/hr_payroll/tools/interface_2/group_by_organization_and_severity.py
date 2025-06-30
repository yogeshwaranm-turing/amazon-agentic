from tau_bench.envs.tool import Tool
from typing import Any, Dict, List
from collections import defaultdict

class GroupByOrganizationAndSeverity(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], risks: List[str]) -> Dict[str, Dict[str, List[str]]]:
        result = defaultdict(lambda: defaultdict(list))
        for risk_id in risks:
            risk = data["compliance_risks"].get(risk_id)
            if not risk:
                continue
            org_id = risk.get("organization_id")
            severity = risk.get("severity")
            result[org_id][severity].append(risk_id)
        return result

    @staticmethod
    def get_info():
        return {
            "name": "group_by_organization_and_severity",
            "description": "Groups compliance risks by organization and severity.",
            "parameters": {
                "risks": "List[str]"
            },
            "returns": "Dict[str, Dict[str, List[str]]]"
        }