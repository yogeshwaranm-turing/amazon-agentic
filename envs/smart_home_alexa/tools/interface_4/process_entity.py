import json
from typing import Any, Dict, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool


class ProcessEntity(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        entity_type: str,
        user_id: str,
        entity_id: Optional[str] = None,
        entity_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Manage entities in the smart home system: create, update, or delete.
        Requires user authentication and appropriate authorization.
        """
        # Authorization check
        if not user_id:
            return json.dumps({
                "error": "user_id is required for authentication"
            })

        # Verify user exists and is active
        users = data.get('users', {})
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

        # Admin-only operations
        admin_only_operations = {
            'create': ['user', 'device', 'skill', 'backup'],
            'delete': ['user', 'device', 'group', 'skill', 'backup']
        }

        if operation in admin_only_operations:
            if entity_type in admin_only_operations[operation] and user_role != 'Admin':
                return json.dumps({
                    "error": f"Admin authorization required to {operation} {entity_type}"
                })

        # For update operations on routines/scenes, verify user is Admin or creator
        if operation == 'update' and entity_type in ['routine', 'scene'] and user_role != 'Admin':
            collection_name = 'routines' if entity_type == 'routine' else 'scenes'
            collection = data.get(collection_name, {})
            existing_entity = collection.get(entity_id)
            if existing_entity and existing_entity.get('created_by_user_id') != user_id:
                return json.dumps({
                    "error": f"User not authorized to update this {entity_type}"
                })

        if operation not in ['create', 'update', 'delete']:
            return json.dumps({
                "error": f"Invalid operation: {operation}",
                "supported_operations": ['create', 'update', 'delete']
            })

        entity_type_mapping = {
            'user': ('users', 'user_id'),
            'device': ('devices', 'device_id'),
            'group': ('groups', 'group_id'),
            'routine': ('routines', 'routine_id'),
            'scene': ('scenes', 'scene_id'),
            'skill': ('skills', 'skill_id'),
            'announcement': ('announcements', 'announcement_id'),
            'session': ('sessions', 'session_id'),
            'report': ('reports', 'report_id'),
            'alert': ('system_alerts', 'alert_id'),
            'backup': ('backups', 'backup_id'),
            'geofence': ('geofence_configurations', 'geofence_id'),
            'notification_template': ('notification_templates', 'template_id'),
            'privacy_setting': ('privacy_settings', 'setting_id'),
            'device_network_config': ('device_network_config', 'config_id')
        }

        if entity_type not in entity_type_mapping:
            return json.dumps({
                "error": f"Invalid entity_type: {entity_type}",
                "supported_types": list(entity_type_mapping.keys())
            })

        collection_name, id_field = entity_type_mapping[entity_type]
        collection = data.setdefault(collection_name, {})

        timestamp = datetime.utcnow().isoformat() + "Z"

        # Validate references before operations
        if entity_data:
            ref_validation = ProcessEntity._validate_references(data, entity_type, entity_data)
            if ref_validation.get('error'):
                return json.dumps(ref_validation)

        # MAC address uniqueness check for devices
        if operation == 'create' and entity_type == 'device' and entity_data:
            mac_address = entity_data.get('mac_address')
            if mac_address:
                devices = data.get('devices', {})
                for device_id, device in devices.items():
                    if device.get('mac_address') == mac_address:
                        return json.dumps({
                            "error": f"Device with MAC address '{mac_address}' already exists (device_id: {device_id})"
                        })

        if operation == 'create':
            return ProcessEntity._create_entity(
                collection, id_field, entity_type, entity_data, timestamp, user_id
            )
        elif operation == 'update':
            return ProcessEntity._update_entity(
                collection, id_field, entity_type, entity_id, entity_data, timestamp, user_id
            )
        elif operation == 'delete':
            return ProcessEntity._delete_entity(
                collection, id_field, entity_type, entity_id, user_id
            )

    @staticmethod
    def _validate_references(data: Dict[str, Any], entity_type: str, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that referenced entities exist."""
        errors = []

        # Check user references
        user_fields = ['registered_by_user_id', 'created_by_user_id', 'user_id', 'enabled_by_user_id', 'resolved_by_user_id']
        for field in user_fields:
            if field in entity_data:
                user_id = entity_data[field]
                if user_id and user_id not in data.get('users', {}):
                    errors.append(f"Referenced user '{user_id}' not found")

        # Check device references
        if 'device_id' in entity_data and entity_type != 'device':
            device_id = entity_data['device_id']
            if device_id and device_id not in data.get('devices', {}):
                errors.append(f"Referenced device '{device_id}' not found")

        # Check group references
        if 'group_id' in entity_data and entity_type != 'group':
            group_id = entity_data['group_id']
            if group_id and group_id not in data.get('groups', {}):
                errors.append(f"Referenced group '{group_id}' not found")

        # Check routine references
        if 'routine_id' in entity_data and entity_type != 'routine':
            routine_id = entity_data['routine_id']
            if routine_id and routine_id not in data.get('routines', {}):
                errors.append(f"Referenced routine '{routine_id}' not found")

        if errors:
            return {"error": "; ".join(errors)}

        return {}

    @staticmethod
    def _generate_id(collection: Dict[str, Any], prefix: str = "") -> str:
        """Generate a new unique ID for an entity."""
        if not collection:
            return f"{prefix}1"

        max_id = 0
        for key in collection.keys():
            try:
                num = int(key.replace(prefix, ""))
                if num > max_id:
                    max_id = num
            except ValueError:
                continue

        return f"{prefix}{max_id + 1}"

    @staticmethod
    def _create_entity(
        collection: Dict[str, Any],
        id_field: str,
        entity_type: str,
        entity_data: Optional[Dict[str, Any]],
        timestamp: str,
        user_id: str
    ) -> str:
        """Create a new entity."""
        if not entity_data:
            return json.dumps({
                "error": "entity_data is required for create operation"
            })

        prefix_map = {
            'user': 'U',
            'device': 'D',
            'group': 'G',
            'routine': 'R',
            'scene': 'S',
            'skill': 'SK',
            'announcement': 'A',
            'session': 'SES',
            'report': 'REP',
            'alert': 'AL',
            'backup': 'B',
            'geofence': 'GF',
            'notification_template': 'NT',
            'privacy_setting': 'PS',
            'device_network_config': 'DNC'
        }

        prefix = prefix_map.get(entity_type, 'ENT')
        new_id = ProcessEntity._generate_id(collection, prefix)

        new_entity = dict(entity_data)
        new_entity[id_field] = new_id
        new_entity['created_at'] = timestamp
        new_entity['updated_at'] = timestamp

        ProcessEntity._apply_defaults(new_entity, entity_type)

        collection[new_id] = new_entity

        # Create audit log entry
        from .maintain_audit_logs import MaintainAuditLogs
        audit_entry = {
            "timestamp": timestamp,
            "user_id": user_id,
            "action_type": f"{entity_type}_create",
            "entity_type": entity_type,
            "entity_id": new_id,
            "action_details": json.dumps({"entity_data": entity_data}),
            "outcome": "success"
        }
        MaintainAuditLogs.invoke({"Access_Logs": {}}, operation="create_log", operation_data=audit_entry)

        return json.dumps({
            "operation": "create",
            "entity_type": entity_type,
            "entity_id": new_id,
            "success": True,
            "entity": new_entity
        })

    @staticmethod
    def _update_entity(
        collection: Dict[str, Any],
        id_field: str,
        entity_type: str,
        entity_id: Optional[str],
        entity_data: Optional[Dict[str, Any]],
        timestamp: str,
        user_id: str
    ) -> str:
        """Update an existing entity."""
        if not entity_id:
            return json.dumps({
                "error": "entity_id is required for update operation"
            })

        if not entity_data:
            return json.dumps({
                "error": "entity_data is required for update operation"
            })

        entity = collection.get(entity_id)
        if not entity:
            return json.dumps({
                "error": f"{entity_type} with ID '{entity_id}' not found"
            })

        for key, value in entity_data.items():
            if key != id_field and key != 'created_at':
                entity[key] = value

        entity['updated_at'] = timestamp

        # Create audit log entry
        from .maintain_audit_logs import MaintainAuditLogs
        audit_entry = {
            "timestamp": timestamp,
            "user_id": user_id,
            "action_type": f"{entity_type}_update",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action_details": json.dumps({"updated_fields": list(entity_data.keys())}),
            "outcome": "success"
        }
        MaintainAuditLogs.invoke({"Access_Logs": {}}, operation="create_log", operation_data=audit_entry)

        return json.dumps({
            "operation": "update",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "success": True,
            "entity": entity
        })

    @staticmethod
    def _delete_entity(
        collection: Dict[str, Any],
        id_field: str,
        entity_type: str,
        entity_id: Optional[str],
        user_id: str
    ) -> str:
        """Delete an entity."""
        if not entity_id:
            return json.dumps({
                "error": "entity_id is required for delete operation"
            })

        entity = collection.get(entity_id)
        if not entity:
            return json.dumps({
                "error": f"{entity_type} with ID '{entity_id}' not found"
            })

        deleted_entity = dict(entity)
        del collection[entity_id]

        # Create audit log entry
        from .maintain_audit_logs import MaintainAuditLogs
        from datetime import datetime
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "action_type": f"{entity_type}_delete",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action_details": json.dumps({"deleted_entity": deleted_entity}),
            "outcome": "success"
        }
        MaintainAuditLogs.invoke({"Access_Logs": {}}, operation="create_log", operation_data=audit_entry)

        return json.dumps({
            "operation": "delete",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "success": True,
            "deleted_entity": deleted_entity
        })

    @staticmethod
    def _apply_defaults(entity: Dict[str, Any], entity_type: str) -> None:
        """Apply default values for entity fields based on entity type."""
        defaults = {
            'user': {
                'account_status': 'active',
                'mfa_enabled': False,
                'mfa_method': 'none'
            },
            'device': {
                'connection_status': 'registered',
                'power_state': 'off',
                'alexa_skill_required': False
            },
            'routine': {
                'schedule_recurrence': 'daily',
                'status': 'enabled',
                'security_mode': 'none',
                'pin_required': False,
                'away_mode': False,
                'execution_count': 0
            },
            'scene': {
                'status': 'enabled',
                'security_mode': 'none',
                'pin_required': False,
                'trigger_count': 0
            },
            'skill': {
                'status': 'disabled',
                'account_linked': False,
                'linked_account_encrypted': True,
                'invocation_count': 0
            },
            'announcement': {
                'delivery_status': 'pending'
            },
            'session': {
                'status': 'active'
            },
            'alert': {
                'acknowledged': False,
                'resolved': False
            },
            'backup': {
                'encrypted': True,
                'checksum_algorithm': 'SHA256'
            },
            'geofence': {
                'is_active': True
            },
            'notification_template': {
                'is_active': True
            },
            'privacy_setting': {
                'microphone_enabled': True,
                'camera_enabled': True,
                'video_recording_enabled': True,
                'drop_in_permissions': 'allowed',
                'settings_encrypted': True
            },
            'device_network_config': {
                'is_active': True
            }
        }

        entity_defaults = defaults.get(entity_type, {})
        for key, value in entity_defaults.items():
            if key not in entity:
                entity[key] = value

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_entity",
                "description": """Manage entities in the smart home system. Supports create, update, and delete
                operations for users, devices, groups, routines, scenes, skills, announcements, sessions, reports,
                alerts, backups, geofences, notification templates, privacy settings, and device network configurations.
                Automatically generates IDs for new entities and applies appropriate defaults. Requires user authentication,
                validates references, checks MAC address uniqueness for devices, and creates audit log entries.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Operation to perform: 'create', 'update', or 'delete'",
                            "enum": ["create", "update", "delete"]
                        },
                        "entity_type": {
                            "type": "string",
                            "description": """Type of entity to manage. Supported types: 'user', 'device', 'group',
                            'routine', 'scene', 'skill', 'announcement', 'session', 'report', 'alert', 'backup',
                            'geofence', 'notification_template', 'privacy_setting', 'device_network_config'""",
                            "enum": ["user", "device", "group", "routine", "scene", "skill", "announcement",
                                     "session", "report", "alert", "backup", "geofence", "notification_template",
                                     "privacy_setting", "device_network_config"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the operation (required for authentication and authorization)"
                        },
                        "entity_id": {
                            "type": "string",
                            "description": """The unique identifier of the entity. Required for 'update' and 'delete'
                            operations. Not required for 'create' (auto-generated)."""
                        },
                        "entity_data": {
                            "type": "object",
                            "description": """The data for the entity. Required for 'create' and 'update' operations.
                            For 'create', include all required fields. For 'update', include only fields to change.
                            Common fields include: user_name, email_address, device_name, device_type, routine_name,
                            scene_name, etc. Refer to schema for entity-specific required fields."""
                        }
                    },
                    "required": ["operation", "entity_type", "user_id"]
                }
            }
        }
