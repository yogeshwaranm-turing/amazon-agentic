from tau_bench.envs.tool import Tool
from typing import Any, Dict

class CompareWorkerAndPositionDepartments(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], worker_id: str, position_id: str) -> bool:
        position = data["hr_positions"].get(position_id)
        if not position:
            raise ValueError("Position not found.")
        expected_dept = position.get("department_id")

        for wp in data["worker_positions"].values():
            if wp["worker_id"] == worker_id and wp["position_id"] == position_id:
                actual_dept = wp.get("department_id")
                return actual_dept != expected_dept
        return False

    @staticmethod
    def get_info():
        return {
            "name": "compare_worker_and_position_departments",
            "description": "Checks if a worker's department on their position mismatches the expected department.",
            "parameters": {
                "worker_id": "str",
                "position_id": "str"
            },
            "returns": "bool"
        }