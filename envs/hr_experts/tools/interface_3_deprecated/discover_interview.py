
import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverInterview(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover interview records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for interviews"
            })
        
        results = []
        interviews = data.get("interviews", {})
        
        for interview_id, interview_data in interviews.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    interview_value = interview_data.get(filter_key)
                    if interview_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**interview_data, "interview_id": interview_id})
            else:
                results.append({**interview_data, "interview_id": interview_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "interviews",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_interview",
                "description": "Discover interview records. Filterable by interview_id (string), application_id (string), interviewer_id (string), interview_type (enum: 'phone_screening', 'technical', 'behavioral', 'panel', 'final'), scheduled_date (timestamp), duration_minutes (integer), status (enum: 'scheduled', 'completed', 'cancelled', 'no_show'), overall_rating (enum: 'excellent', 'good', 'average', 'below_average', 'poor'), recommendation (enum: 'strong_hire', 'hire', 'no_hire', 'strong_no_hire'), created_at (timestamp), updated_at (timestamp).",
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