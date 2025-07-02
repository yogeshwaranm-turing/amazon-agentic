
import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class RemoveWorkerFromOrg(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str) -> str:
        workers = data.get("workers", {})
        contracts = data.get("contracts", {})
        payroll_items = data.get("payroll_items", {})

        if worker_id not in workers:
            raise ValueError("Worker not found")
        if any(c["worker_id"] == worker_id and c["status"] in ["active", "signed"]
               for c in contracts.values()):
            raise ValueError("Worker has active contracts")
        if any(p["worker_id"] == worker_id for p in payroll_items.values()):
            raise ValueError("Worker is tied to payroll")

        del workers[worker_id]
        return json.dumps({"worker_id": worker_id})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_worker_from_org",
                "description": "Removes a worker from the organization if not tied to active contracts or payroll",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "worker_id": {
                            "type": "string",
                            "description": "Worker ID to be removed"
                        }
                    },
                    "required": ["worker_id"]
                }
            }
        }
