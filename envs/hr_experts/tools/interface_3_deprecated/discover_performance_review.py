import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverPerformanceReview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover performance review records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for performance reviews"
            })
        
        results = []
        performance_reviews = data.get("performance_reviews", {})
        
        for review_id, review_data in performance_reviews.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    review_value = review_data.get(filter_key)
                    if review_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**review_data, "review_id": review_id})
            else:
                results.append({**review_data, "review_id": review_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "performance_reviews",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_performance_review",
                "description": "Discover performance review records. Filterable by review_id (string), employee_id (string), reviewer_id (string), review_period_start (date), review_period_end (date), review_type (enum: 'annual', 'quarterly', 'probationary', 'project_based'), overall_rating (enum: 'exceeds_expectations', 'meets_expectations', 'below_expectations', 'unsatisfactory'), status (enum: 'draft', 'submitted', 'approved'), created_at (timestamp), updated_at (timestamp).",
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