from typing import Dict, Any
from tau_bench.envs.tool import Tool
from collections import defaultdict

class GetDepartmentWorkerSummary(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], organization_id: str) -> Dict[str, int]:
        workers = data["workers"]
        summary = defaultdict(int)

        for worker in workers.values():
            if worker["organization_id"] == organization_id:
                dept = worker.get("department", "Unassigned")
                summary[dept] += 1

        return dict(summary)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "get_department_worker_summary",
            "description": "Count number of workers per department in an organization.",
            "parameters": {
                "organization_id": {"type": "string", "description": "Organization ID"}
            },
            "returns": {"type": "object", "description": "Mapping of department names to worker counts"}
        }