import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverEmployeeEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover employee entities.
        
        Supported entities:
        - employees: Employee records by employee_id, user_id, position_id, hire_date, employment_status, manager_id, date_of_birth, address, hourly_rate, created_at, updated_at
        """
        if entity_type not in ["employees"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'employees'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("employees", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "employee_id": entity_id})
            else:
                results.append({**entity_data, "employee_id": entity_id})
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_employee_entities",
                "description": "Discover employee entities. Entity types: 'employees' (employee records; filterable by employee_id (string), user_id (string), position_id (string), hire_date (date), employment_status (enum: 'active', 'terminated', 'on_leave', 'suspended'), manager_id (string), date_of_birth (date), address (string), hourly_rate (integer), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'employees'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For employees, filters are: employee_id (string), user_id (string), position_id (string), hire_date (date), employment_status (enum: 'active', 'terminated', 'on_leave', 'suspended'), manager_id (string), date_of_birth (date), address (string), hourly_rate (integer), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
