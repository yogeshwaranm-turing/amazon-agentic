import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class InspectEntityStatus(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        entity_type: str,
        entity_id: str,
        user_id: str,
        include_health_info: bool = False
    ) -> str:
        """
        Get the status information for a specific entity in the smart home system.
        Requires user authentication and appropriate authorization.
        """
        # Authorization check
        if not user_id:
            return json.dumps({
                "error": "user_id is required for authentication"
            })

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

        user_role = user.get('role')

        # Admin role required for user, skill, backup, firmware_update status
        admin_only_entities = ['user', 'skill', 'backup', 'firmware_update']
        if entity_type in admin_only_entities and user_role != 'Admin':
            return json.dumps({
                "error": f"Admin authorization required to check {entity_type} status"
            })

        # For devices, verify user has access (unless Admin)
        if entity_type == 'device' and user_role != 'Admin':
            from .has_auth_access import HasAuthAccess
            auth_check = json.loads(HasAuthAccess.invoke(
                data,
                authorization_type="device_access",
                user_id=user_id,
                device_id=entity_id
            ))
            if not auth_check.get('authorized', False):
                return json.dumps({
                    "error": f"User not authorized to access device {entity_id}"
                })

        entity_type_mapping = {
            'user': ('users', 'user_id', ['account_status', 'mfa_enabled', 'last_login_at']),
            'device': ('devices', 'device_id', ['connection_status', 'power_state', 'battery_level', 
                                                  'signal_strength', 'last_communication_timestamp']),
            'routine': ('routines', 'routine_id', ['status', 'last_execution_timestamp', 
                                                     'next_execution_timestamp', 'last_execution_outcome']),
            'scene': ('scenes', 'scene_id', ['status', 'last_triggered_at', 'trigger_count']),
            'skill': ('skills', 'skill_id', ['status', 'account_linked', 'token_expiry', 
                                              'last_invocation_at', 'invocation_count']),
            'session': ('sessions', 'session_id', ['status', 'start_time', 'expiration_time']),
            'alert': ('system_alerts', 'alert_id', ['alert_type', 'priority', 'acknowledged', 
                                                      'resolved', 'acknowledged_at', 'resolved_at']),
            'backup': ('backups', 'backup_id', ['backup_location_type', 'encrypted', 
                                                 'retention_until', 'verification_status']),
            'firmware_update': ('device_firmware_history', 'history_id', ['update_status', 
                                                                            'priority_level', 
                                                                            'update_started_at', 
                                                                            'update_completed_at']),
            'announcement': ('announcements', 'announcement_id', ['delivery_status', 'delivery_time'])
        }
        
        if entity_type not in entity_type_mapping:
            return json.dumps({
                "error": f"Invalid entity_type: {entity_type}",
                "supported_types": list(entity_type_mapping.keys())
            })
        
        collection_name, id_field, status_fields = entity_type_mapping[entity_type]
        collection = data.get(collection_name, {})
        
        entity = collection.get(entity_id)
        
        if not entity:
            return json.dumps({
                "error": f"{entity_type} with ID '{entity_id}' not found"
            })
        
        result = {
            "entity_type": entity_type,
            "entity_id": entity_id
        }
        
        for field in status_fields:
            if field in entity:
                result[field] = entity[field]
        
        if include_health_info and entity_type == 'device':
            device_health = data.get('device_health_history', {})
            health_records = []
            
            for health_record in device_health.values():
                if health_record.get('device_id') == entity_id:
                    health_records.append({
                        'timestamp': health_record.get('timestamp'),
                        'health_status': health_record.get('health_status'),
                        'health_score': health_record.get('health_score'),
                        'error_category': health_record.get('error_category'),
                        'error_details': health_record.get('error_details')
                    })
            
            health_records.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            result['health_history'] = health_records[:5]
            
            network_config = data.get('device_network_config', {})
            for config in network_config.values():
                if config.get('device_id') == entity_id:
                    result['network_status'] = {
                        'network_name': config.get('network_name'),
                        'ip_address': config.get('ip_address'),
                        'is_active': config.get('is_active'),
                        'last_network_change_timestamp': config.get('last_network_change_timestamp')
                    }
                    break
            
            privacy = data.get('privacy_settings', {})
            for setting in privacy.values():
                if setting.get('device_id') == entity_id:
                    result['privacy_settings'] = {
                        'microphone_enabled': setting.get('microphone_enabled'),
                        'camera_enabled': setting.get('camera_enabled'),
                        'video_recording_enabled': setting.get('video_recording_enabled'),
                        'drop_in_permissions': setting.get('drop_in_permissions')
                    }
                    break

        # Create audit log entry
        from .control_audit_logs import ControlAuditLogs
        from datetime import datetime

        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "action_type": "entity_status_check",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action_details": json.dumps({
                "include_health_info": include_health_info
            }),
            "outcome": "success"
        }

        ControlAuditLogs.invoke(data, operation="create_log", operation_data=audit_entry)

        return json.dumps(result)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "inspect_entity_status",
                "description": """Get the current status information for a specific entity in the smart home system.
                Supports users, devices, routines, scenes, skills, sessions, alerts, backups, firmware updates,
                and announcements. For devices, can optionally include detailed health information, network status,
                and privacy settings. Requires user authentication and Admin role for sensitive entities.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": """Type of entity to query. Supported types: 'user', 'device', 'routine',
                            'scene', 'skill', 'session', 'alert', 'backup', 'firmware_update', 'announcement'""",
                            "enum": ["user", "device", "routine", "scene", "skill", "session", "alert",
                                     "backup", "firmware_update", "announcement"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "The unique identifier of the entity"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the status check (required for authentication and authorization)"
                        },
                        "include_health_info": {
                            "type": "boolean",
                            "description": """Only applicable for 'device' entity_type. If true, includes device health 
                            history, network status, and privacy settings. Default: false"""
                        }
                    },
                    "required": ["entity_type", "entity_id", "user_id"]
                }
            }
        }

