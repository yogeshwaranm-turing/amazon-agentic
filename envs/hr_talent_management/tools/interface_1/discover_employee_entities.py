# Auto-generated — DO NOT EDIT BY HAND
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DiscoverEmployeeEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], mode: str, employee_id: str = None, email: str = None, department_id: str = None, location_id: str = None, employment_status: str = None, limit: int = None, offset: int = None) -> str:
        def mask(emp):
            emp = dict(emp)
            emp.pop("tax_id", None)
            emp.pop("bank_account_number", None)
            emp.pop("routing_number", None)
            return emp

        mode = (mode or "").lower()
        if mode not in {"employees.search","employees.get","onboarding.search_by_employee"}:
            raise ValueError("mode must be employees.search|employees.get|onboarding.search_by_employee")

        employees = data.get("employees", {})
        onboarding = data.get("onboarding_checklists", {})
        limit = int(limit or 50)
        offset = int(offset or 0)

        if mode == "employees.search":
            out = []
            for _, rec in employees.items():
                if employee_id and rec.get("employee_id") != employee_id: continue
                if email and rec.get("work_email") != email: continue
                if department_id and rec.get("department_id") != department_id: continue
                if location_id and rec.get("location_id") != location_id: continue
                if employment_status and rec.get("employment_status") != employment_status: continue
                out.append(mask(rec))
            return json.dumps({"items": out[offset:offset+limit], "next_offset": offset + min(len(out), limit)})

        if mode == "employees.get":
            if not employee_id:
                raise ValueError("employee_id is required for employees.get")
            rec = None
            for _, r in employees.items():
                if r.get("employee_id") == employee_id:
                    rec = r; break
            if not rec:
                raise ValueError(f"Employee {employee_id} not found")
            return json.dumps({"item": mask(rec)})

        # onboarding.search_by_employee
        out = []
        for _, r in onboarding.items():
            if employee_id and r.get("employee_id") != employee_id: continue
            out.append(r)
        return json.dumps({"items": out[offset:offset+limit], "next_offset": offset + min(len(out), limit)})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_employee_entities",
                "description": 'Search or fetch employee records (masked) and onboarding checklists.',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "str"},
                        "employee_id": {"type": "str"},
                        "email": {"type": "str"},
                        "department_id": {"type": "str"},
                        "location_id": {"type": "str"},
                        "employment_status": {"type": "str"},
                        "limit": {"type": "integer"},
                        "offset": {"type": "integer"}
                    },
                    "required": ["mode"]
                }
            }
        }

def discover_employee_entities(data: Dict[str, Any], **kwargs) -> str:
    return DiscoverEmployeeEntities.invoke(data, **kwargs)
