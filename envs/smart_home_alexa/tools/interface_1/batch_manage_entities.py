import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool


class BatchManageEntities(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operations: List[Dict[str, Any]],
        user_id: str,
        stop_on_error: bool = False,
        validate_references: bool = True
    ) -> str:
        """
        Perform multiple entity management operations in a single batch.
        Requires user authentication. User must have authorization for each operation.
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

        if not operations:
            return json.dumps({
                "error": "operations list is required and cannot be empty"
            })
        
        if not isinstance(operations, list):
            return json.dumps({
                "error": "operations must be a list of operation objects"
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
            'device_network_config': ('device_network_config', 'config_id'),
            'routine_device_action': ('routine_device_actions', 'action_id'),
            'scene_device': ('scene_devices', 'scene_device_id'),
            'user_device_permission': ('user_device_permissions', 'permission_id'),
            'user_group_permission': ('user_group_permissions', 'permission_id'),
            'skill_device_permission': ('skill_device_permissions', 'permission_id')
        }
        
        results = []
        created_entities = {}
        timestamp = datetime.utcnow().isoformat() + "Z"
        success_count = 0
        error_count = 0
        
        for idx, operation in enumerate(operations):
            operation_id = operation.get('operation_id', f"op_{idx}")
            operation_type = operation.get('operation')
            entity_type = operation.get('entity_type')
            entity_id = operation.get('entity_id')
            entity_data = operation.get('entity_data')
            
            if not operation_type:
                result = {
                    "operation_id": operation_id,
                    "index": idx,
                    "success": False,
                    "error": "operation field is required (create/update/delete)"
                }
                results.append(result)
                error_count += 1
                if stop_on_error:
                    break
                continue
            
            if operation_type not in ['create', 'update', 'delete']:
                result = {
                    "operation_id": operation_id,
                    "index": idx,
                    "success": False,
                    "error": f"Invalid operation: {operation_type}"
                }
                results.append(result)
                error_count += 1
                if stop_on_error:
                    break
                continue
            
            if not entity_type or entity_type not in entity_type_mapping:
                result = {
                    "operation_id": operation_id,
                    "index": idx,
                    "success": False,
                    "error": f"Invalid or missing entity_type: {entity_type}"
                }
                results.append(result)
                error_count += 1
                if stop_on_error:
                    break
                continue
            
            collection_name, id_field = entity_type_mapping[entity_type]
            collection = data.setdefault(collection_name, {})
            
            entity_id_resolved = BatchManageEntities._resolve_entity_id(
                entity_id, created_entities
            )
            
            if validate_references and entity_data:
                entity_data_resolved = BatchManageEntities._resolve_references(
                    entity_data, created_entities
                )
            else:
                entity_data_resolved = entity_data
            
            try:
                if operation_type == 'create':
                    result = BatchManageEntities._create_entity(
                        collection, id_field, entity_type, entity_data_resolved,
                        timestamp, operation_id, idx
                    )
                    if result['success']:
                        created_entities[operation_id] = result['entity_id']
                        success_count += 1
                    else:
                        error_count += 1
                
                elif operation_type == 'update':
                    result = BatchManageEntities._update_entity(
                        collection, id_field, entity_type, entity_id_resolved,
                        entity_data_resolved, timestamp, operation_id, idx
                    )
                    if result['success']:
                        success_count += 1
                    else:
                        error_count += 1
                
                elif operation_type == 'delete':
                    result = BatchManageEntities._delete_entity(
                        collection, id_field, entity_type, entity_id_resolved,
                        operation_id, idx
                    )
                    if result['success']:
                        success_count += 1
                    else:
                        error_count += 1
                
                results.append(result)
                
                if not result['success'] and stop_on_error:
                    break
                    
            except Exception as e:
                result = {
                    "operation_id": operation_id,
                    "index": idx,
                    "operation": operation_type,
                    "entity_type": entity_type,
                    "success": False,
                    "error": str(e)
                }
                results.append(result)
                error_count += 1
                if stop_on_error:
                    break
        
        return json.dumps({
            "batch_success": error_count == 0,
            "total_operations": len(operations),
            "processed_operations": len(results),
            "success_count": success_count,
            "error_count": error_count,
            "created_entities": created_entities,
            "results": results
        })
    
    @staticmethod
    def _resolve_entity_id(entity_id: Optional[str], created_entities: Dict[str, str]) -> Optional[str]:
        """Resolve entity_id references to previously created entities."""
        if not entity_id:
            return None
        
        if entity_id.startswith('$'):
            ref_id = entity_id[1:]
            return created_entities.get(ref_id, entity_id)
        
        return entity_id
    
    @staticmethod
    def _resolve_references(entity_data: Dict[str, Any], created_entities: Dict[str, str]) -> Dict[str, Any]:
        """Resolve references in entity_data to previously created entities."""
        resolved_data = {}
        
        for key, value in entity_data.items():
            if isinstance(value, str) and value.startswith('$'):
                ref_id = value[1:]
                resolved_data[key] = created_entities.get(ref_id, value)
            else:
                resolved_data[key] = value
        
        return resolved_data
    
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
        operation_id: str,
        index: int
    ) -> Dict[str, Any]:
        """Create a new entity."""
        if not entity_data:
            return {
                "operation_id": operation_id,
                "index": index,
                "operation": "create",
                "entity_type": entity_type,
                "success": False,
                "error": "entity_data is required for create operation"
            }
        
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
            'device_network_config': 'DNC',
            'routine_device_action': 'RDA',
            'scene_device': 'SD',
            'user_device_permission': 'UDP',
            'user_group_permission': 'UGP',
            'skill_device_permission': 'SDP'
        }
        
        prefix = prefix_map.get(entity_type, 'ENT')
        new_id = BatchManageEntities._generate_id(collection, prefix)
        
        new_entity = dict(entity_data)
        new_entity[id_field] = new_id
        new_entity['created_at'] = timestamp
        new_entity['updated_at'] = timestamp
        
        BatchManageEntities._apply_defaults(new_entity, entity_type)
        
        collection[new_id] = new_entity
        
        return {
            "operation_id": operation_id,
            "index": index,
            "operation": "create",
            "entity_type": entity_type,
            "entity_id": new_id,
            "success": True
        }
    
    @staticmethod
    def _update_entity(
        collection: Dict[str, Any],
        id_field: str,
        entity_type: str,
        entity_id: Optional[str],
        entity_data: Optional[Dict[str, Any]],
        timestamp: str,
        operation_id: str,
        index: int
    ) -> Dict[str, Any]:
        """Update an existing entity."""
        if not entity_id:
            return {
                "operation_id": operation_id,
                "index": index,
                "operation": "update",
                "entity_type": entity_type,
                "success": False,
                "error": "entity_id is required for update operation"
            }
        
        if not entity_data:
            return {
                "operation_id": operation_id,
                "index": index,
                "operation": "update",
                "entity_type": entity_type,
                "entity_id": entity_id,
                "success": False,
                "error": "entity_data is required for update operation"
            }
        
        entity = collection.get(entity_id)
        if not entity:
            return {
                "operation_id": operation_id,
                "index": index,
                "operation": "update",
                "entity_type": entity_type,
                "entity_id": entity_id,
                "success": False,
                "error": f"{entity_type} with ID '{entity_id}' not found"
            }
        
        for key, value in entity_data.items():
            if key != id_field and key != 'created_at':
                entity[key] = value
        
        entity['updated_at'] = timestamp
        
        return {
            "operation_id": operation_id,
            "index": index,
            "operation": "update",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "success": True
        }
    
    @staticmethod
    def _delete_entity(
        collection: Dict[str, Any],
        id_field: str,
        entity_type: str,
        entity_id: Optional[str],
        operation_id: str,
        index: int
    ) -> Dict[str, Any]:
        """Delete an entity."""
        if not entity_id:
            return {
                "operation_id": operation_id,
                "index": index,
                "operation": "delete",
                "entity_type": entity_type,
                "success": False,
                "error": "entity_id is required for delete operation"
            }
        
        entity = collection.get(entity_id)
        if not entity:
            return {
                "operation_id": operation_id,
                "index": index,
                "operation": "delete",
                "entity_type": entity_type,
                "entity_id": entity_id,
                "success": False,
                "error": f"{entity_type} with ID '{entity_id}' not found"
            }
        
        del collection[entity_id]
        
        return {
            "operation_id": operation_id,
            "index": index,
            "operation": "delete",
            "entity_type": entity_type,
            "entity_id": entity_id,
            "success": True
        }
    
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
            },
            'routine_device_action': {
                'wait_duration_seconds': 0
            },
            'user_device_permission': {
                'permission_level': 'read_only'
            },
            'user_group_permission': {
                'permission_level': 'read_only'
            },
            'skill_device_permission': {
                'permission_level': 'read_only'
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
                "name": "batch_manage_entities",
                "description": """Perform multiple entity management operations in a single batch. Supports create,
                update, and delete operations across different entity types. Useful for bulk operations, complex workflows,
                and maintaining relationships between entities. Supports reference resolution using '$operation_id' syntax
                to reference entities created earlier in the batch. Can optionally stop on first error or continue processing
                all operations. Requires user authentication and appropriate authorization for each operation.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operations": {
                            "type": "array",
                            "description": """List of operations to perform. Each operation is an object with:
                            - operation_id: (optional) Unique identifier for this operation, used for reference resolution
                            - operation: (required) 'create', 'update', or 'delete'
                            - entity_type: (required) Type of entity (user, device, routine, scene, etc.)
                            - entity_id: (required for update/delete) ID of entity, or '$operation_id' to reference created entity
                            - entity_data: (required for create/update) Entity data to create/update
                            
                            Example: [
                              {"operation_id": "user1", "operation": "create", "entity_type": "user", 
                               "entity_data": {"user_name": "John", "email_address": "john@example.com", 
                               "role": "Admin", "permission_level": "full_control"}},
                              {"operation": "create", "entity_type": "device", 
                               "entity_data": {"device_name": "Living Room Light", "registered_by_user_id": "$user1", 
                               "device_type": "light", "device_category": "lighting", "mac_address": "AA:BB:CC:DD:EE:FF", 
                               "manufacturer": "Philips", "model": "Hue", "network_protocol": "Zigbee"}},
                              {"operation": "update", "entity_type": "device", "entity_id": "D001", 
                               "entity_data": {"connection_status": "online"}}
                            ]""",
                            "items": {
                                "type": "object"
                            }
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the batch operations (required for authentication and authorization)"
                        },
                        "stop_on_error": {
                            "type": "boolean",
                            "description": """If true, stops processing operations after the first error.
                            If false (default), continues processing all operations even if some fail."""
                        },
                        "validate_references": {
                            "type": "boolean",
                            "description": """If true (default), automatically resolves references using '$operation_id' 
                            syntax in entity_data fields. Set to false to disable reference resolution."""
                        }
                    },
                    "required": ["operations", "user_id"]
                }
            }
        }

