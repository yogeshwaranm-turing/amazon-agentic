import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class ListWorkersByOrg(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], organization_id: str) -> str:
        workers = data.get("workers", {})
        result: List[Dict[str, Any]] = [
            worker for worker in workers.values() if worker.get("organization_id") == organization_id
        ]
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "list_workers_by_org",
                "description": "List all workers associated with a specific organization.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "organization_id": {
                            "type": "string",
                            "description": "Organization ID to fetch workers for."
                        }
                    },
                    "required": ["organization_id"]
                }
            }
        }
