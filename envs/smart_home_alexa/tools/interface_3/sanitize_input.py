import json
import re
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool


class SanitizeInput(Tool):
    ENUMS = {
        'role': ['Admin', 'Household_Member', 'Guest'],
        'permission_level': ['full_control', 'restricted', 'read_only', 'execute_only'],
        'account_status': ['active', 'suspended', 'expired'],
        'device_type': [
            'light', 'lock', 'thermostat', 'camera', 'sensor', 'speaker', 'switch', 'plug',
            'appliance', 'echo_device', 'hub', 'temperature_sensor', 'humidity_sensor',
            'motion_sensor', 'door_window_sensor', 'smoke_detector', 'smart_tv',
            'streaming_device', 'soundbar', 'air_purifier', 'humidifier', 'dehumidifier',
            'space_heater', 'air_conditioner'
        ],
        'device_category': ['security', 'climate', 'lighting', 'entertainment', 'appliance', 
                           'sensor', 'voice_assistant', 'networking'],
        'network_protocol': ['WiFi', 'Zigbee', 'Bluetooth', 'Matter', 'ZWave', 'Thread'],
        'connection_status': ['registered', 'online', 'offline', 'error', 'maintenance', 'reconnecting'],
        'power_state': ['on', 'off', 'standby'],
        'health_status': ['healthy', 'warning', 'critical', 'unknown'],
        'routine_type': ['comfort', 'security', 'awareness', 'custom'],
        'trigger_type': ['time', 'sunrise', 'sunset', 'location', 'sensor', 'voice', 'manual', 
                        'geofence', 'scheduled'],
        'schedule_recurrence': ['daily', 'weekdays', 'weekends', 'specific_dates', 'specific_days', 
                               'once', 'seasonal'],
        'routine_status': ['enabled', 'disabled', 'error'],
        'security_mode': ['armed_away', 'armed_stay', 'disarm', 'none'],
        'skill_status': ['enabled', 'disabled'],
        'outcome': ['success', 'failure', 'error'],
        'action_type': [
            'device_add', 'device_remove', 'device_update', 'user_create', 'user_remove',
            'user_update', 'routine_create', 'routine_modify', 'routine_delete', 'routine_execute',
            'group_create', 'group_update', 'group_remove', 'skill_enable', 'skill_disable',
            'privacy_settings_update', 'mfa_enable', 'firmware_update', 'system_backup',
            'system_restore', 'connection_troubleshoot', 'health_check', 'security_scene_create',
            'security_scene_modify', 'device_network_update', 'device_network_change',
            'guest_access_create', 'guest_access_revoke', 'scene_trigger', 'announcement_send',
            'session_create', 'session_expire', 'report_generate'
        ],
        'entity_type': ['device', 'user', 'routine', 'group', 'skill', 'backup', 'system', 
                       'geofence', 'scene', 'announcement', 'session', 'report'],
        'group_type': ['location', 'function'],
        'backup_location_type': ['cloud', 'local'],
        'alert_type': ['security', 'system', 'device_failure', 'connectivity', 'battery_low',
                      'firmware_available', 'temperature_threshold', 'unauthorized_access'],
        'alert_priority': ['low', 'medium', 'high', 'critical'],
        'firmware_update_status': ['available', 'pending', 'in_progress', 'completed', 'failed', 
                                  'rolled_back'],
        'mfa_method': ['sms', 'authenticator_app', 'none'],
        'drop_in_permission': ['allowed', 'restricted', 'disabled'],
        'notification_type': ['email', 'sms', 'push'],
        'geofence_event': ['enter', 'exit', 'dwell'],
        'device_action_type': [
            'turn_on', 'turn_off', 'set_temperature', 'lock', 'unlock', 'arm', 'disarm',
            'set_brightness', 'set_color', 'play_media', 'pause_media', 'send_notification',
            'wait', 'trigger_scene'
        ],
        'scene_trigger_type': ['manual', 'location', 'scheduled', 'routine'],
        'session_status': ['active', 'expired', 'revoked'],
        'delivery_status': ['pending', 'delivered', 'failed'],
        'report_type': ['lifecycle', 'energy', 'health', 'performance', 'security', 'usage'],
        'update_priority': ['critical', 'normal', 'optional'],
        'error_category': [
            'none', 'firmware_error', 'network_error', 'hardware_error', 'configuration_error',
            'authentication_error', 'timeout_error', 'battery_error', 'sensor_error',
            'communication_error', 'unknown_error'
        ],
        'target_type': ['device', 'group']
    }
    
    ENTITY_SCHEMAS = {
        'users': {
            'required': ['user_name', 'email_address', 'role', 'permission_level'],
            'fields': {
                'user_id': 'string',
                'user_name': 'string',
                'email_address': 'email',
                'phone_number': 'phone',
                'role': 'enum:role',
                'permission_level': 'enum:permission_level',
                'account_status': 'enum:account_status',
                'guest_access_expiration': 'timestamp',
                'guest_access_duration_days': 'int',
                'mfa_enabled': 'boolean',
                'mfa_method': 'enum:mfa_method'
            }
        },
        'devices': {
            'required': ['device_name', 'device_type', 'device_category', 'mac_address', 
                        'manufacturer', 'model', 'network_protocol', 'registered_by_user_id'],
            'fields': {
                'device_id': 'string',
                'device_name': 'string',
                'device_type': 'enum:device_type',
                'device_category': 'enum:device_category',
                'mac_address': 'mac',
                'manufacturer': 'string',
                'model': 'string',
                'firmware_version': 'string',
                'network_protocol': 'enum:network_protocol',
                'group_id': 'string',
                'connection_status': 'enum:connection_status',
                'battery_level': 'int',
                'signal_strength': 'int',
                'power_state': 'enum:power_state',
                'alexa_skill_required': 'boolean'
            }
        },
        'routines': {
            'required': ['routine_name', 'routine_type', 'trigger_type', 'created_by_user_id'],
            'fields': {
                'routine_id': 'string',
                'routine_name': 'string',
                'routine_type': 'enum:routine_type',
                'trigger_type': 'enum:trigger_type',
                'trigger_value': 'string',
                'schedule_recurrence': 'enum:schedule_recurrence',
                'status': 'enum:routine_status',
                'security_mode': 'enum:security_mode',
                'pin_required': 'boolean',
                'away_mode': 'boolean',
                'execution_count': 'int'
            }
        },
        'scenes': {
            'required': ['scene_name', 'trigger_type', 'created_by_user_id'],
            'fields': {
                'scene_id': 'string',
                'scene_name': 'string',
                'trigger_type': 'enum:scene_trigger_type',
                'security_mode': 'enum:security_mode',
                'pin_required': 'boolean',
                'status': 'enum:routine_status',
                'trigger_count': 'int'
            }
        },
        'skills': {
            'required': ['skill_name', 'skill_provider'],
            'fields': {
                'skill_id': 'string',
                'skill_name': 'string',
                'skill_provider': 'string',
                'account_linked': 'boolean',
                'status': 'enum:skill_status',
                'invocation_count': 'int'
            }
        },
        'groups': {
            'required': ['group_name', 'group_type', 'created_by_user_id'],
            'fields': {
                'group_id': 'string',
                'group_name': 'string',
                'group_type': 'enum:group_type',
                'description': 'string',
                'parent_group_id': 'string'
            }
        },
        'system_alerts': {
            'required': ['alert_type', 'priority', 'message'],
            'fields': {
                'alert_id': 'string',
                'alert_type': 'enum:alert_type',
                'priority': 'enum:alert_priority',
                'message': 'string',
                'affected_device_id': 'string',
                'acknowledged': 'boolean',
                'resolved': 'boolean'
            }
        },
        'backups': {
            'required': ['backup_location_type', 'storage_identifier', 'checksum', 
                        'backup_type', 'created_by_user_id'],
            'fields': {
                'backup_id': 'string',
                'backup_location_type': 'enum:backup_location_type',
                'storage_identifier': 'string',
                'checksum': 'string',
                'encrypted': 'boolean',
                'backup_type': 'string'
            }
        }
    }
    
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        validation_type: str,
        entity_type: Optional[str] = None,
        entity_data: Optional[Dict[str, Any]] = None,
        field_name: Optional[str] = None,
        field_value: Optional[Any] = None
    ) -> str:
        """
        Validate input data against schema constraints.
        """
        if validation_type == 'enum':
            return SanitizeInput._validate_enum(field_name, field_value)
        elif validation_type == 'entity':
            return SanitizeInput._validate_entity(entity_type, entity_data)
        elif validation_type == 'field':
            return SanitizeInput._validate_field(field_name, field_value, entity_type)
        elif validation_type == 'list_enums':
            return SanitizeInput._list_enums()
        elif validation_type == 'entity_schema':
            return SanitizeInput._get_entity_schema(entity_type)
        else:
            return json.dumps({
                "error": f"Invalid validation_type: {validation_type}",
                "supported_types": ['enum', 'entity', 'field', 'list_enums', 'entity_schema']
            })
    
    @staticmethod
    def _validate_enum(field_name: Optional[str], field_value: Optional[Any]) -> str:
        """Validate if a value is valid for a specific enum field."""
        if not field_name:
            return json.dumps({
                "error": "field_name is required for enum validation"
            })
        
        if field_name not in SanitizeInput.ENUMS:
            return json.dumps({
                "valid": False,
                "error": f"Unknown enum type: {field_name}",
                "available_enums": list(SanitizeInput.ENUMS.keys())
            })
        
        valid_values = SanitizeInput.ENUMS[field_name]
        is_valid = field_value in valid_values
        
        return json.dumps({
            "valid": is_valid,
            "field_name": field_name,
            "field_value": field_value,
            "valid_values": valid_values,
            "message": "Valid" if is_valid else f"Invalid value. Must be one of: {valid_values}"
        })
    
    @staticmethod
    def _validate_entity(entity_type: Optional[str], entity_data: Optional[Dict[str, Any]]) -> str:
        """Validate complete entity data against schema."""
        if not entity_type:
            return json.dumps({
                "error": "entity_type is required for entity validation"
            })
        
        if not entity_data:
            return json.dumps({
                "error": "entity_data is required for entity validation"
            })
        
        if entity_type not in SanitizeInput.ENTITY_SCHEMAS:
            return json.dumps({
                "valid": False,
                "error": f"Unknown entity type: {entity_type}",
                "available_types": list(SanitizeInput.ENTITY_SCHEMAS.keys())
            })
        
        schema = SanitizeInput.ENTITY_SCHEMAS[entity_type]
        errors = []
        warnings = []
        
        for required_field in schema['required']:
            if required_field not in entity_data:
                errors.append(f"Missing required field: {required_field}")
        
        for field_name, field_value in entity_data.items():
            if field_name not in schema['fields']:
                warnings.append(f"Unknown field: {field_name}")
                continue
            
            field_type = schema['fields'][field_name]
            validation_result = SanitizeInput._validate_field_type(
                field_name, field_value, field_type
            )
            
            if not validation_result['valid']:
                errors.append(validation_result['error'])
        
        is_valid = len(errors) == 0
        
        return json.dumps({
            "valid": is_valid,
            "entity_type": entity_type,
            "errors": errors,
            "warnings": warnings,
            "message": "Valid entity data" if is_valid else "Entity validation failed"
        })
    
    @staticmethod
    def _validate_field(
        field_name: Optional[str],
        field_value: Optional[Any],
        entity_type: Optional[str] = None
    ) -> str:
        """Validate a single field."""
        if not field_name:
            return json.dumps({
                "error": "field_name is required for field validation"
            })
        
        field_type = SanitizeInput._get_field_type(field_name, entity_type)
        
        if not field_type:
            return json.dumps({
                "valid": False,
                "error": f"Unknown field: {field_name}"
            })
        
        result = SanitizeInput._validate_field_type(field_name, field_value, field_type)
        return json.dumps(result)
    
    @staticmethod
    def _validate_field_type(field_name: str, field_value: Any, field_type: str) -> Dict[str, Any]:
        """Validate a field against its type."""
        if field_value is None:
            return {"valid": True, "field_name": field_name, "message": "Null value accepted"}
        
        if field_type.startswith('enum:'):
            enum_name = field_type.split(':')[1]
            valid_values = SanitizeInput.ENUMS.get(enum_name, [])
            is_valid = field_value in valid_values
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": f"Invalid enum value. Must be one of: {valid_values}" if not is_valid else None
            }
        
        elif field_type == 'string':
            is_valid = isinstance(field_value, str)
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Must be a string" if not is_valid else None
            }
        
        elif field_type == 'int':
            is_valid = isinstance(field_value, int) or (isinstance(field_value, str) and field_value.isdigit())
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Must be an integer" if not is_valid else None
            }
        
        elif field_type == 'boolean':
            is_valid = isinstance(field_value, bool)
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Must be a boolean" if not is_valid else None
            }
        
        elif field_type == 'email':
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = isinstance(field_value, str) and re.match(email_pattern, field_value) is not None
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Invalid email format" if not is_valid else None
            }
        
        elif field_type == 'phone':
            phone_pattern = r'^\+?[\d\s\-\(\)]+$'
            is_valid = isinstance(field_value, str) and re.match(phone_pattern, field_value) is not None
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Invalid phone number format" if not is_valid else None
            }
        
        elif field_type == 'mac':
            mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            is_valid = isinstance(field_value, str) and re.match(mac_pattern, field_value) is not None
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Invalid MAC address format (expected: XX:XX:XX:XX:XX:XX)" if not is_valid else None
            }
        
        elif field_type == 'timestamp':
            timestamp_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
            is_valid = isinstance(field_value, str) and re.match(timestamp_pattern, field_value) is not None
            return {
                "valid": is_valid,
                "field_name": field_name,
                "field_type": field_type,
                "error": "Invalid timestamp format (expected: YYYY-MM-DDTHH:MM:SS)" if not is_valid else None
            }
        
        return {"valid": True, "field_name": field_name, "field_type": field_type}
    
    @staticmethod
    def _get_field_type(field_name: str, entity_type: Optional[str] = None) -> Optional[str]:
        """Get the field type for a given field name."""
        if entity_type and entity_type in SanitizeInput.ENTITY_SCHEMAS:
            schema = SanitizeInput.ENTITY_SCHEMAS[entity_type]
            return schema['fields'].get(field_name)
        
        for schema in SanitizeInput.ENTITY_SCHEMAS.values():
            if field_name in schema['fields']:
                return schema['fields'][field_name]
        
        return None
    
    @staticmethod
    def _list_enums() -> str:
        """List all available enums and their values."""
        return json.dumps({
            "enums": SanitizeInput.ENUMS
        })
    
    @staticmethod
    def _get_entity_schema(entity_type: Optional[str]) -> str:
        """Get the schema for a specific entity type."""
        if not entity_type:
            return json.dumps({
                "error": "entity_type is required",
                "available_types": list(SanitizeInput.ENTITY_SCHEMAS.keys())
            })
        
        if entity_type not in SanitizeInput.ENTITY_SCHEMAS:
            return json.dumps({
                "error": f"Unknown entity type: {entity_type}",
                "available_types": list(SanitizeInput.ENTITY_SCHEMAS.keys())
            })
        
        return json.dumps({
            "entity_type": entity_type,
            "schema": SanitizeInput.ENTITY_SCHEMAS[entity_type]
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "sanitize_input",
                "description": """Validate input data against schema constraints. Supports validation of enum values, 
                complete entity data, individual fields, and provides schema information. Can validate enums like role, 
                device_type, connection_status, etc., and entity data for users, devices, routines, scenes, and more. 
                Checks required fields, data types, formats (email, phone, MAC address), and enum constraints.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "validation_type": {
                            "type": "string",
                            "description": """Type of validation to perform:
                            - 'enum': Validate if a value is valid for a specific enum
                            - 'entity': Validate complete entity data including required fields
                            - 'field': Validate a single field value
                            - 'list_enums': List all available enums and their values
                            - 'entity_schema': Get the schema for a specific entity type""",
                            "enum": ["enum", "entity", "field", "list_enums", "entity_schema"]
                        },
                        "entity_type": {
                            "type": "string",
                            "description": """Entity type for validation. Used with 'entity', 'field', and 'entity_schema' 
                            validation types. Examples: 'users', 'devices', 'routines', 'scenes', 'skills', 'groups', 
                            'system_alerts', 'backups'"""
                        },
                        "entity_data": {
                            "type": "object",
                            "description": """Complete entity data to validate. Required for 'entity' validation type. 
                            Should include all required fields and any optional fields to validate."""
                        },
                        "field_name": {
                            "type": "string",
                            "description": """Field name to validate. Required for 'enum' and 'field' validation types. 
                            Examples: 'role', 'device_type', 'connection_status', 'email_address', 'mac_address'"""
                        },
                        "field_value": {
                            "description": """Value to validate for the field. Required for 'enum' and 'field' validation 
                            types. Type depends on field (string, int, boolean, etc.)"""
                        }
                    },
                    "required": ["validation_type"]
                }
            }
        }

