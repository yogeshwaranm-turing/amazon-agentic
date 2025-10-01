import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverMetricsEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover metrics entities.
        
        Supported entities:
        - metrics: Incident metrics records
        """
        if entity_type not in ["metrics"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'metrics'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("metrics", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "metric_id": str(entity_id)})
            else:
                results.append({**entity_data, "metric_id": str(entity_id)})
        
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
                "name": "discover_metrics_entities",
                "description": "Discover metrics entities. Entity types: 'metrics' (incident metrics records; filterable by metric_id (string), incident_id (string), metric_type (enum: 'MTTA', 'MTTD', 'MTTR', 'MTTM', 'FTR'), value_minutes (int), target_minutes (int), recorded_at (timestamp), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'metrics'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For metrics, filters are: metric_id (string), incident_id (string), metric_type (enum: 'MTTA', 'MTTD', 'MTTR', 'MTTM', 'FTR'), value_minutes (int), target_minutes (int), recorded_at (timestamp), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
