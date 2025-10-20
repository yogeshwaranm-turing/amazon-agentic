import json
from typing import Any, Dict, List
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class GetSlaBreachIncidents(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], client_id: str = None, start_date: str = None, end_date: str = None, status: str = None) -> str:
        """
        Retrieves incidents that have breached their Service Level Agreements (SLAs).
        Only incidents with 'resolved_at' or 'closed_at' timestamps are considered for resolution SLA breaches.
        """
        # Define SLA_MATRIX inside the function
        SLA_MATRIX = {
            'premium': {
                'P1': {'response': (15, 30), 'resolution': (120, 240)},
                'P2': {'response': (60, 120), 'resolution': (480, 1440)},
                'P3': {'response': (240, 480), 'resolution': (2880, 4320)},
                'P4': {'response': (1440, 2880), 'resolution': (7680, 7680)}
            },
            'standard': {
                'P1': {'response': (60, 120), 'resolution': (480, 1440)},
                'P2': {'response': (240, 480), 'resolution': (1440, 2880)},
                'P3': {'response': (1440, 1440), 'resolution': (4320, 7200)},
                'P4': {'response': (2880, 4320), 'resolution': (10080, 10080)}
            },
            'basic': {
                'P1': {'response': (240, 480), 'resolution': (1440, 2880)},
                'P2': {'response': (1440, 1440), 'resolution': (4320, 7200)},
                'P3': {'response': (2880, 4320), 'resolution': (7200, 14400)},
                'P4': {'response': (7200, 10080), 'resolution': (20160, 20160)}
            }
        }
        
        incidents_data = data.get("incidents", {})
        sla_agreements_data = data.get("sla_agreements", {})
        incident_ci_data = data.get("incident_configuration_items", {})
        ci_client_assignments_data = data.get("ci_client_assignments", {})
        
        breach_incidents = []
        
        # Parse date filters
        filter_start_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        filter_end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        
        # Helper function to find client_id for an incident through CI relationships
        # Schema: incidents -> incident_configuration_items -> configuration_items -> ci_client_assignments -> clients
        def get_incident_client_id(incident_id: str) -> str:
            # Find CIs affected by this incident
            affected_ci_ids = []
            for relationship_id, relationship in incident_ci_data.items():
                if relationship.get("incident_id") == incident_id:
                    affected_ci_ids.append(relationship.get("ci_id"))
            
            if not affected_ci_ids:
                return None
            
            # Find client assignments for these CIs
            for assignment_id, assignment in ci_client_assignments_data.items():
                if assignment.get("ci_id") in affected_ci_ids:
                    return assignment.get("client_id")
            
            return None
        
        for incident_id, incident in incidents_data.items():
            # Only consider incidents that have been resolved or closed
            if not incident.get("resolved_at") and not incident.get("closed_at"):
                continue
            
            # Apply status filter
            if status and incident.get("status") != status:
                continue
            
            # Apply time range filter based on detection_time
            detection_time_str = incident.get("detection_time")
            if not detection_time_str:
                continue
            
            try:
                # Handle various datetime formats
                if detection_time_str.endswith('Z'):
                    detection_time_str = detection_time_str[:-1] + '+00:00'
                incident_detection_dt = datetime.fromisoformat(detection_time_str)
                
                if filter_start_dt and incident_detection_dt < filter_start_dt:
                    continue
                if filter_end_dt and incident_detection_dt > filter_end_dt:
                    continue
            except ValueError:
                continue
            
            # Get client_id through CI relationships
            incident_client_id = get_incident_client_id(incident_id)
            if not incident_client_id:
                continue
            
            # Apply client_id filter
            if client_id and incident_client_id != client_id:
                continue
            
            incident_severity = incident.get("severity")
            if not incident_severity:
                continue
            
            # Find the SLA agreement for the incident's client
            client_sla = None
            for sla_id, sla_agreement in sla_agreements_data.items():
                if sla_agreement.get("client_id") == incident_client_id and sla_agreement.get("status") == "active":
                    client_sla = sla_agreement
                    break
            
            if not client_sla:
                continue
            
            client_tier = client_sla.get("tier")
            if not client_tier or client_tier not in SLA_MATRIX:
                continue
            
            sla_config = SLA_MATRIX[client_tier].get(incident_severity)
            if not sla_config:
                continue
            
            # Use the maximum resolution time from the range as the target
            expected_resolution_minutes = sla_config['resolution'][1]
            
            # Calculate actual resolution duration
            resolved_at_str = incident.get("resolved_at") or incident.get("closed_at")
            try:
                if resolved_at_str.endswith('Z'):
                    resolved_at_str = resolved_at_str[:-1] + '+00:00'
                incident_resolved_dt = datetime.fromisoformat(resolved_at_str)
                
                actual_resolution_duration_minutes = (incident_resolved_dt - incident_detection_dt).total_seconds() / 60
                
                # Check for SLA breach
                if actual_resolution_duration_minutes > expected_resolution_minutes:
                    incident_copy = incident.copy()
                    incident_copy["client_id"] = incident_client_id
                    incident_copy["sla_tier"] = client_tier
                    incident_copy["expected_resolution_minutes"] = expected_resolution_minutes
                    incident_copy["actual_resolution_minutes"] = round(actual_resolution_duration_minutes, 2)
                    incident_copy["breach_by_minutes"] = round(actual_resolution_duration_minutes - expected_resolution_minutes, 2)
                    breach_incidents.append(incident_copy)
            except ValueError:
                continue
        
        return json.dumps({
            "success": True,
            "count": len(breach_incidents),
            "breach_incidents": breach_incidents
        }, indent=2)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "retrieve_sla_breach_incidents",
                "description": "Retrieves incidents that have breached their Service Level Agreements (SLAs).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_id": {
                            "type": "string",
                            "description": "Optional: Filter incidents by a specific client ID."
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Optional: Start date for the time range (YYYY-MM-DD)."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "Optional: End date for the time range (YYYY-MM-DD)."
                        },
                        "status": {
                            "type": "string",
                            "description": "Optional: Filter incidents by status (open, in_progress, monitoring, resolved, closed)."
                        }
                    },
                    "required": []
                }
            }
        }