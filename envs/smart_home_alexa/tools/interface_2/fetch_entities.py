import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class FetchEntities(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        user_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = 0
    ) -> str:
        """
        Query entities from the smart home database with flexible filtering.
        Requires user authentication and appropriate authorization.
        """
        # Authorization check
        if not user_id:
            return json.dumps({
                "error": "user_id is required for authentication"
            })

        # Import here to avoid circular dependency
        from .validate_access import ValidateAccess

        # Verify user exists and is active
        users = data.get('Users', {})
        user = users.get(user_id)
        if not user:
            return json.dumps({
                "error": f"User {user_id} not found"
            })

        if user.get('account_status') != 'active':
            return json.dumps({
                "error": f"User account is {user.get('account_status')}, not active"
            })

        # Check authorization based on entity type
        user_role = user.get('role')
        sensitive_entities = ['Users', 'Skills', 'Backups', 'Access_Logs']

        if entity_type in sensitive_entities and user_role != 'Admin':
            return json.dumps({
                "error": f"Admin authorization required to query {entity_type}"
            })

        if not entity_type:
            return json.dumps({
                "error": "entity_type is required",
                "available_entities": list(data.keys())
            })
        
        entities = data.get(entity_type, {})
        
        if not entities:
            return json.dumps({
                "error": f"Entity type '{entity_type}' not found",
                "available_entities": list(data.keys())
            })
        
        results = []
        
        entity_list = list(entities.values()) if isinstance(entities, dict) else entities
        
        for entity in entity_list:
            if filters:
                match = True
                for key, value in filters.items():
                    entity_value = FetchEntities._get_nested_value(entity, key)
                    
                    if isinstance(value, dict) and any(op in value for op in ['$eq', '$ne', '$gt', '$lt', '$gte', '$lte', '$in', '$like']):
                        if not FetchEntities._match_operator(entity_value, value):
                            match = False
                            break
                    else:
                        if isinstance(entity_value, str) and isinstance(value, str):
                            if entity_value.lower() != value.lower():
                                match = False
                                break
                        elif entity_value != value:
                            match = False
                            break
                
                if match:
                    results.append(entity)
            else:
                results.append(entity)
        
        total_count = len(results)
        start_idx = offset or 0
        end_idx = start_idx + limit if limit else len(results)
        paginated_results = results[start_idx:end_idx]

        # Create audit log entry
        from .handle_audit_logs import HandleAuditLogs
        from datetime import datetime

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "action_type": "entity_query",
            "entity_type": entity_type,
            "entity_id": None,
            "action_details": json.dumps({
                "filters": filters,
                "result_count": total_count
            }),
            "outcome": "success"
        }

        HandleAuditLogs.invoke(data, operation="create_log", operation_data=audit_entry)

        return json.dumps({
            "entity_type": entity_type,
            "total_count": total_count,
            "returned_count": len(paginated_results),
            "offset": start_idx,
            "results": paginated_results
        })
    
    @staticmethod
    def _get_nested_value(obj: Any, key: str) -> Any:
        """Get value from nested dictionary using dot notation."""
        keys = key.split('.')
        value = obj
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
        return value
    
    @staticmethod
    def _match_operator(entity_value: Any, filter_value: Dict[str, Any]) -> bool:
        """Match entity value against filter operators."""
        for op, val in filter_value.items():
            if op == '$eq':
                if entity_value != val:
                    return False
            elif op == '$ne':
                if entity_value == val:
                    return False
            elif op == '$gt':
                if entity_value is None or entity_value <= val:
                    return False
            elif op == '$lt':
                if entity_value is None or entity_value >= val:
                    return False
            elif op == '$gte':
                if entity_value is None or entity_value < val:
                    return False
            elif op == '$lte':
                if entity_value is None or entity_value > val:
                    return False
            elif op == '$in':
                if entity_value not in val:
                    return False
            elif op == '$like':
                if entity_value is None or val.lower() not in str(entity_value).lower():
                    return False
        return True
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Metadata for the fetch_entities tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "fetch_entities",
                "description": """Query any entity type from the smart home database with flexible filtering.
                Supports querying users, devices, routines, groups, scenes, skills, announcements, sessions,
                reports, system_alerts, backups, access_logs, and more. Filters can use simple equality or
                advanced operators like $eq, $ne, $gt, $lt, $gte, $lte, $in, $like. Requires user authentication
                and Admin role for sensitive entities (Users, Skills, Backups, Access_Logs).""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": """Type of entity to query. Common types include: 'users', 'devices',
                            'routines', 'groups', 'scenes', 'skills', 'announcements', 'sessions', 'reports',
                            'system_alerts', 'backups', 'access_logs', 'routine_execution_logs',
                            'device_health_history', 'firmware_versions', 'privacy_settings', etc."""
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the query (required for authentication and authorization)"
                        },
                        "filters": {
                            "type": "object",
                            "description": """Optional filters as key-value pairs. Supports dot notation for nested 
                            fields and advanced operators. Examples: {'role': 'Admin'}, {'status': {'$eq': 'active'}}, 
                            {'battery_level': {'$lt': 20}}, {'device_type': {'$in': ['light', 'lock']}}, 
                            {'device_name': {'$like': 'living'}}"""
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (for pagination)"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Number of results to skip (for pagination, default: 0)"
                        }
                    },
                    "required": ["entity_type", "user_id"]
                }
            }
        }

