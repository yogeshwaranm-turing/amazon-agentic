import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverBenefitsPlan(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover benefits plan records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for benefits plans"
            })
        
        results = []
        benefits_plans = data.get("benefits_plans", {})
        
        for plan_id, plan_data in benefits_plans.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    plan_value = plan_data.get(filter_key)
                    if plan_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**plan_data, "plan_id": plan_id})
            else:
                results.append({**plan_data, "plan_id": plan_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "benefits_plans",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_benefits_plan",
                "description": "Discover benefits plan records. Filterable by plan_id (string), plan_name (string), plan_type (enum: 'health_insurance', 'dental', 'vision', 'life_insurance', 'disability', 'retirement_401k', 'pto', 'flexible_spending'), provider (string), employee_cost (decimal), employer_cost (decimal), status (enum: 'active', 'inactive'), effective_date (date), expiration_date (date), created_at (timestamp), updated_at (timestamp).",
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