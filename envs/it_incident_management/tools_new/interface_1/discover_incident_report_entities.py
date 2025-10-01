import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverIncidentReportEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident report entities.
        
        Supported entities:
        - incident_reports: Incident report records
        """
        if entity_type not in ["incident_reports"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'incident_reports'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("incident_reports", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "report_id": str(entity_id)})
            else:
                results.append({**entity_data, "report_id": str(entity_id)})
        
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
                "name": "discover_incident_report_entities",
                "description": "Discover incident report entities. Entity types: 'incident_reports' (incident report records; filterable by report_id (string), incident_id (string), report_type (enum: 'executive_summary', 'technical_details', 'business_impact', 'compliance_report', 'post_mortem'), generated_by_id (string), generated_at (timestamp), status (enum: 'draft', 'completed', 'distributed'), created_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'incident_reports'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For incident_reports, filters are: report_id (string), incident_id (string), report_type (enum: 'executive_summary', 'technical_details', 'business_impact', 'compliance_report', 'post_mortem'), generated_by_id (string), generated_at (timestamp), status (enum: 'draft', 'completed', 'distributed'), created_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
