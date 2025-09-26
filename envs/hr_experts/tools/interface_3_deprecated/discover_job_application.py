import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverJobApplication(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover job application records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for job applications"
            })
        
        results = []
        applications = data.get("job_applications", {})
        
        for app_id, app_data in applications.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    app_value = app_data.get(filter_key)
                    if app_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**app_data, "application_id": app_id})
            else:
                results.append({**app_data, "application_id": app_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "job_applications",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_job_application",
                "description": "Discover job application records. Filterable by application_id (string), candidate_id (string), position_id (string), application_date (date), status (enum: 'submitted', 'under_review', 'screening', 'interviewing', 'offer_made', 'accepted', 'rejected', 'withdrawn'), recruiter_id (string), ai_screening_score (decimal), final_decision (enum: 'hire', 'reject', 'hold'), created_at (timestamp), updated_at (timestamp).",
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