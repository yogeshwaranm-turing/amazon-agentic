import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class RetrieveUserEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Uretrieve user entities.
        
        Supported entities:
        - users: User records by user_id, first_name, last_name, email, phone_number, role, status, mfa_enabled, created_at, updated_at
        """
        if entity_type not in ["users"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'users'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("users", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "user_id": entity_id})
            else:
                results.append({**entity_data, "user_id": entity_id})
        
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
                "name": "retrieve_user_entities",
                "description": "Uretrieve user entities. Entity types: 'users' (user records; filterable by user_id (string), first_name (string), last_name (string), email (string), phone_number (string), role (enum: 'hr_director', 'hr_manager', 'recruiter', 'payroll_administrator', 'hiring_manager', 'finance_officer', 'it_administrator', 'compliance_officer', 'employee'), status (enum: 'active', 'inactive', 'suspended'), mfa_enabled (boolean), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'users'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For users, filters are: user_id (string), first_name (string), last_name (string), email (string), phone_number (string), role (enum: 'hr_director', 'hr_manager', 'recruiter', 'payroll_administrator', 'hiring_manager', 'finance_officer', 'it_administrator', 'compliance_officer', 'employee'), status (enum: 'active', 'inactive', 'suspended'), mfa_enabled (boolean), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }

