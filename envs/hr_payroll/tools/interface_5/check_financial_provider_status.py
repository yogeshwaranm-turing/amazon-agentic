from typing import Dict, Any
from tau_bench.envs.tool import Tool

class CheckFinancialProviderStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], provider_id: str) -> Dict[str, str]:
        return {"provider_id": provider_id, "status": "active"}

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "check_financial_provider_status",
                "description": "Check if a financial provider (bank, fintech) is active and usable.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "provider_id": {"type": "string"}
                    },
                    "required": ["provider_id"]
                }
            }
        }