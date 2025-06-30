from tau_bench.envs.tool import Tool
from typing import Any, Dict, List

class IdentifyCriticalUnresolved(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], risks: List[str]) -> List[str]:
        unresolved = []
        for risk_id in risks:
            risk = data["compliance_risks"].get(risk_id)
            if not risk:
                continue
            if risk.get("severity") == "critical" and not risk.get("compliance_action_id"):
                unresolved.append(risk_id)
        return unresolved

    @staticmethod
    def get_info():
        return {
            "name": "identify_critical_unresolved",
            "description": "Identifies critical risks without linked compliance actions.",
            "parameters": {
                "risks": "List[str]"
            },
            "returns": "List[str]"
        }