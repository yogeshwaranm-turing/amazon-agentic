
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class TerminateWorkerContract(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], contract_id: str) -> str:
        contracts = data.get("contracts", {})
        if contract_id not in contracts:
            raise ValueError("Contract not found")

        contracts[contract_id]["status"] = "terminated"
        contracts[contract_id]["end_date"] = "2025-07-01"
        return json.dumps({"contract_id": contract_id, "status": "terminated"})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "terminate_worker_contract",
                "description": "Ends a contract and updates its status to terminated",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contract_id": {
                            "type": "string",
                            "description": "The ID of the contract to be terminated"
                        }
                    },
                    "required": ["contract_id"]
                }
            }
        }
