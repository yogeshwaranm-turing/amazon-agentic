import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverEmployeeBenefits(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover employee benefits records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for employee benefits"
            })
        
        results = []
        employee_benefits = data.get("employee_benefits", {})
        
        for enrollment_id, benefits_data in employee_benefits.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    benefits_value = benefits_data.get(filter_key)
                    if benefits_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**benefits_data, "enrollment_id": enrollment_id})
            else:
                results.append({**benefits_data, "enrollment_id": enrollment_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "employee_benefits",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_employee_benefits",
                "description": "Discover employee benefits records. Filterable by enrollment_id (string), employee_id (string), plan_id (string), enrollment_date (date), status (enum: 'active', 'terminated', 'pending'), coverage_level (enum: 'employee_only', 'employee_spouse', 'employee_children', 'family'), beneficiary_name (string), beneficiary_relationship (string), created_at (timestamp), updated_at (timestamp).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False."
                        }
                    }
                }
            }
        }