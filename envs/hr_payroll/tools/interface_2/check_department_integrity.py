from typing import Dict, Any
from tau_bench.envs.tool import Tool

class CheckDepartmentIntegrity(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], department_id: str) -> str:
        departments = data["org_departments"]
        if department_id not in departments:
            raise ValueError("Department not found")
        dept = departments[department_id]
        if not dept.get("name") or not dept.get("organization_id"):
            return "Invalid department configuration"
        return "Department is structurally valid"

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "name": "check_department_integrity",
            "description": "Validates whether a department entry is correctly structured.",
            "parameters": {
                "department_id": {"type": "string", "description": "ID of the department"}
            },
            "returns": {"type": "string", "description": "Validation status"}
        }