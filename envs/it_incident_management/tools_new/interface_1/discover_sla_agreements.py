import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverSlaAgreements(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover SLA agreement entities.
        
        Supported entities:
        - sla_agreements: SLA agreement records by sla_id, subscription_id, severity_level, response_time_minutes, resolution_time_hours, availability_percentage
        """
        if entity_type not in ["sla_agreements"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'sla_agreements'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("sla_agreements", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "sla_id": str(entity_id)})
            else:
                results.append({**entity_data, "sla_id": str(entity_id)})
        
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
                "name": "discover_sla_agreements",
                "description": "Discover SLA agreement entities. Entity types: 'sla_agreements' (SLA agreement records; filterable by sla_id (string), subscription_id (string), severity_level (enum: 'P1', 'P2', 'P3', 'P4'), response_time_minutes (integer), resolution_time_hours (integer), availability_percentage (decimal), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'sla_agreements'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For sla_agreements, filters are: sla_id (string), subscription_id (string), severity_level (enum: 'P1', 'P2', 'P3', 'P4'), response_time_minutes (integer), resolution_time_hours (integer), availability_percentage (decimal), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
