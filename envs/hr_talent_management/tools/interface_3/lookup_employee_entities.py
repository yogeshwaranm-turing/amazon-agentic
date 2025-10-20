import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class LookupEmployeeEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover and retrieve employee-related entities including employees and onboarding checklists.

        entity_type: "employees" | "onboarding_checklists"
        filters: optional dict with exact-match filtering and date range support
        Returns: {"entities": list, "count": int, "message": str}
        """

        if entity_type not in ["employees", "onboarding_checklists"]:
            return json.dumps({
                "success": False,
                "error": "Halt: Missing entity_type or invalid entity_type - must be one of: employees, onboarding_checklists"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: Discovery tool execution failed due to system errors - invalid data format"
            })
         

        def apply_exact_filters(record: Dict[str, Any], exact_filter_keys: List[str], filters_obj: Dict[str, Any]) -> bool:
            for key in exact_filter_keys:
                if key in filters_obj:
                    if record.get(key) != filters_obj[key]:
                        return False
            return True

        def in_date_range(date_value: Optional[str], start_key: str, end_key: str, filters_obj: Dict[str, Any]) -> bool:
            if not date_value:
                return False if (start_key in filters_obj or end_key in filters_obj) else True
            if start_key in filters_obj and date_value < filters_obj[start_key]:
                return False
            if end_key in filters_obj and date_value > filters_obj[end_key]:
                return False
            return True

        results: List[Dict[str, Any]] = []

        if entity_type == "employees":
            employees = data.get("employees", {})

            # Supported employee filters
            employee_exact_keys = [
                "employee_id", "candidate_id", "first_name", "last_name", "employee_type", 
                "department_id", "location_id", "job_title", "tax_id", "work_email", 
                "phone_number", "manager_id", "tax_filing_status", "employment_status"
            ]

            for employee_id, employee in employees.items():
                record = {**employee}

                # Exact-match filters
                if filters:
                    if not apply_exact_filters(record, employee_exact_keys, filters):
                        continue

                    # Date range filters for start_date
                    if not in_date_range(record.get("start_date"), "start_date_from", "start_date_to", filters):
                        continue

                # ensure id present as string
                record["employee_id"] = str(employee_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "employees",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        if entity_type == "onboarding_checklists":
            checklists = data.get("onboarding_checklists", {})

            # Supported onboarding checklist filters
            checklist_exact_keys = [
                "checklist_id", "employee_id", "candidate_name", "position", 
                "hiring_manager_id", "pre_onboarding_status", "background_check_status", 
                "document_verification_status", "it_provisioning_status", "orientation_completed", 
                "benefits_enrollment_status", "overall_status"
            ]

            for checklist_id, checklist in checklists.items():
                record = {**checklist}

                # Exact-match filters
                if filters:
                    if not apply_exact_filters(record, checklist_exact_keys, filters):
                        continue

                    # Date range filters for start_date
                    if not in_date_range(record.get("start_date"), "start_date_from", "start_date_to", filters):
                        continue

                # ensure id present as string
                record["checklist_id"] = str(checklist_id)
                results.append(record)

            return json.dumps({
                "success": True,
                "entity_type": "onboarding_checklists",
                "count": len(results),
                "entities": results,
                "filters_applied": filters or {}
            })

        return json.dumps({
            "success": False,
            "error": "Halt: Missing entity_type or invalid entity_type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lookup_employee_entities",
                "description": "Discover and retrieve employee-related entities including employees and onboarding checklists.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of employee entity to discover. Valid values: 'employees', 'onboarding_checklists'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters for discovery. For employees: employee_id, candidate_id, first_name, last_name, employee_type, department_id, location_id, job_title, start_date_from, start_date_to, tax_id, work_email, phone_number, manager_id, tax_filing_status, employment_status. For onboarding_checklists: checklist_id, employee_id, candidate_name, start_date_from, start_date_to, position, hiring_manager_id, pre_onboarding_status, background_check_status, document_verification_status, it_provisioning_status, orientation_completed, benefits_enrollment_status, overall_status"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }