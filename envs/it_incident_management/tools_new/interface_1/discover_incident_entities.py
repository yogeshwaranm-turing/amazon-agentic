import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool


class DiscoverIncidentEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Dict[str, Any] = None) -> str:
        """
        Discover incident entities.
        
        Supported entities:
        - incidents: Incident records
        """
        if entity_type not in ["incidents"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be 'incidents'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": f"Invalid data format for {entity_type}"
            })
        
        results = []
        entities = data.get("incidents", {})
        
        for entity_id, entity_data in entities.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    entity_value = entity_data.get(filter_key)
                    if entity_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**entity_data, "incident_id": str(entity_id)})
            else:
                results.append({**entity_data, "incident_id": str(entity_id)})
        
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
                "name": "discover_incident_entities",
                "description": "Discover incident entities. Entity types: 'incidents' (incident records; filterable by incident_id (string), incident_code (string), title (string), reporter_id (string), assigned_manager_id (string), client_id (string), component_id (string), severity (enum: 'P1', 'P2', 'P3', 'P4'), status (enum: 'open', 'in_progress', 'resolved', 'closed'), impact (enum: 'critical', 'high', 'medium', 'low'), urgency (enum: 'critical', 'high', 'medium', 'low'), category (enum: 'system_outage', 'performance_degradation', 'security_incident', 'data_corruption', 'integration_failure', 'network_issue', 'hardware_failure', 'software_bug', 'configuration_error', 'capacity_issue', 'backup_failure', 'authentication_failure', 'api_error', 'database_issue', 'service_unavailable'), detection_source (enum: 'client_reported', 'internally_detected', 'monitoring_alert', 'vendor_reported', 'scheduled_maintenance', 'emergency_maintenance'), detected_at (timestamp), resolved_at (timestamp), closed_at (timestamp), rto_breach (boolean: True/False), sla_breach (boolean: True/False), is_recurring (boolean: True/False), downtime_minutes (int), created_at (timestamp), updated_at (timestamp)).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of entity to discover: 'incidents'"
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False. For incidents, filters are: incident_id (string), incident_code (string), title (string), reporter_id (string), assigned_manager_id (string), client_id (string), component_id (string), severity (enum: 'P1', 'P2', 'P3', 'P4'), status (enum: 'open', 'in_progress', 'resolved', 'closed'), impact (enum: 'critical', 'high', 'medium', 'low'), urgency (enum: 'critical', 'high', 'medium', 'low'), category (enum: 'system_outage', 'performance_degradation', 'security_incident', 'data_corruption', 'integration_failure', 'network_issue', 'hardware_failure', 'software_bug', 'configuration_error', 'capacity_issue', 'backup_failure', 'authentication_failure', 'api_error', 'database_issue', 'service_unavailable'), detection_source (enum: 'client_reported', 'internally_detected', 'monitoring_alert', 'vendor_reported', 'scheduled_maintenance', 'emergency_maintenance'), detected_at (timestamp), resolved_at (timestamp), closed_at (timestamp), rto_breach (boolean: True/False), sla_breach (boolean: True/False), is_recurring (boolean: True/False), downtime_minutes (int), created_at (timestamp), updated_at (timestamp)"
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
