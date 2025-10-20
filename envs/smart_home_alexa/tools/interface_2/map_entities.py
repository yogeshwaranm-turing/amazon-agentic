import json
from typing import Any, Dict, Optional
from datetime import datetime
from tau_bench.envs.tool import Tool


class MapEntities(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        relationship_type: str,
        source_entity_id: str,
        target_entity_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Manage relationships between entities in the smart home system.

        Supports operations:
        - assign: Create a new relationship between entities
        - remove: Remove an existing relationship
        - update_reference: Update reference details in a relationship

        Relationship types:
        - device_to_group: Assign/remove device to/from group
        - device_to_routine: Add/remove device to/from routine
        - user_device_permissions: Manage user permissions for devices
        - user_group_permissions: Manage user permissions for groups
        - skill_device_permissions: Manage skill permissions for devices
        - routine_ownership: Update routine ownership
        - routine_device_reference: Update device references in routines
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
        admin_only_relationship_types = [
            'user_device_permissions',
            'user_group_permissions',
            'skill_device_permissions',
            'routine_ownership'
        ]

        if relationship_type in admin_only_relationship_types and user_role != 'Admin':
            return json.dumps({
                "error": f"Admin authorization required to manage {relationship_type}"
            })

        # Validate operation
        valid_operations = ['assign', 'remove', 'update_reference']
        if operation not in valid_operations:
            return json.dumps({
                "error": f"Invalid operation: {operation}",
                "supported_operations": valid_operations
            })

        # Validate relationship_type
        valid_relationship_types = [
            'device_to_group',
            'device_to_routine',
            'user_device_permissions',
            'user_group_permissions',
            'skill_device_permissions',
            'routine_ownership',
            'routine_device_reference'
        ]

        if relationship_type not in valid_relationship_types:
            return json.dumps({
                "error": f"Invalid relationship_type: {relationship_type}",
                "supported_types": valid_relationship_types
            })

        # Route to appropriate handler
        try:
            if relationship_type == 'device_to_group':
                return MapEntities._handle_device_to_group(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
            elif relationship_type == 'device_to_routine':
                return MapEntities._handle_device_to_routine(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
            elif relationship_type == 'user_device_permissions':
                return MapEntities._handle_user_device_permissions(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
            elif relationship_type == 'user_group_permissions':
                return MapEntities._handle_user_group_permissions(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
            elif relationship_type == 'skill_device_permissions':
                return MapEntities._handle_skill_device_permissions(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
            elif relationship_type == 'routine_ownership':
                return MapEntities._handle_routine_ownership(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
            elif relationship_type == 'routine_device_reference':
                return MapEntities._handle_routine_device_reference(
                    data, operation, source_entity_id, target_entity_id, user_id, relationship_data
                )
        except Exception as e:
            return json.dumps({
                "error": f"Operation failed: {str(e)}"
            })

    @staticmethod
    def _handle_device_to_group(
        data: Dict[str, Any],
        operation: str,
        device_id: str,
        group_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle device-to-group relationships"""
        devices = data.get('devices', {})
        groups = data.get('groups', {})

        device = devices.get(device_id)
        group = groups.get(group_id)

        if not device:
            return json.dumps({"error": f"Device {device_id} not found"})
        if not group:
            return json.dumps({"error": f"Group {group_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'assign':
            # Assign device to group
            device['group_id'] = group_id
            device['updated_at'] = timestamp

            # Add device to group's device list
            if 'device_ids' not in group:
                group['device_ids'] = []
            if device_id not in group['device_ids']:
                group['device_ids'].append(device_id)
            group['updated_at'] = timestamp

            return json.dumps({
                "success": True,
                "operation": "assign",
                "relationship_type": "device_to_group",
                "device_id": device_id,
                "group_id": group_id,
                "message": f"Device {device_id} assigned to group {group_id}"
            })

        elif operation == 'remove':
            # Remove device from group
            if device.get('group_id') == group_id:
                device['group_id'] = None
                device['updated_at'] = timestamp

            # Remove device from group's device list
            if 'device_ids' in group and device_id in group['device_ids']:
                group['device_ids'].remove(device_id)
                group['updated_at'] = timestamp

            return json.dumps({
                "success": True,
                "operation": "remove",
                "relationship_type": "device_to_group",
                "device_id": device_id,
                "group_id": group_id,
                "message": f"Device {device_id} removed from group {group_id}"
            })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for device_to_group"
            })

    @staticmethod
    def _handle_device_to_routine(
        data: Dict[str, Any],
        operation: str,
        device_id: str,
        routine_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle device-to-routine relationships"""
        devices = data.get('devices', {})
        routines = data.get('routines', {})
        routine_devices = data.get('routine_devices', {})

        device = devices.get(device_id)
        routine = routines.get(routine_id)

        if not device:
            return json.dumps({"error": f"Device {device_id} not found"})
        if not routine:
            return json.dumps({"error": f"Routine {routine_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'assign':
            # Create routine-device relationship
            rel_key = f"{routine_id}_{device_id}"

            if rel_key in routine_devices:
                return json.dumps({
                    "error": f"Device {device_id} already assigned to routine {routine_id}"
                })

            routine_devices[rel_key] = {
                "routine_id": routine_id,
                "device_id": device_id,
                "action": relationship_data.get('action') if relationship_data else None,
                "parameters": relationship_data.get('parameters') if relationship_data else {},
                "created_at": timestamp,
                "updated_at": timestamp
            }

            return json.dumps({
                "success": True,
                "operation": "assign",
                "relationship_type": "device_to_routine",
                "device_id": device_id,
                "routine_id": routine_id,
                "message": f"Device {device_id} assigned to routine {routine_id}"
            })

        elif operation == 'remove':
            # Remove routine-device relationship
            rel_key = f"{routine_id}_{device_id}"

            if rel_key in routine_devices:
                del routine_devices[rel_key]
                return json.dumps({
                    "success": True,
                    "operation": "remove",
                    "relationship_type": "device_to_routine",
                    "device_id": device_id,
                    "routine_id": routine_id,
                    "message": f"Device {device_id} removed from routine {routine_id}"
                })
            else:
                return json.dumps({
                    "error": f"Device {device_id} not assigned to routine {routine_id}"
                })

        elif operation == 'update_reference':
            # Update device reference in routine
            rel_key = f"{routine_id}_{device_id}"

            if rel_key not in routine_devices:
                return json.dumps({
                    "error": f"Device {device_id} not assigned to routine {routine_id}"
                })

            if relationship_data:
                routine_devices[rel_key].update(relationship_data)
                routine_devices[rel_key]['updated_at'] = timestamp

            return json.dumps({
                "success": True,
                "operation": "update_reference",
                "relationship_type": "device_to_routine",
                "device_id": device_id,
                "routine_id": routine_id,
                "message": f"Device reference updated in routine {routine_id}"
            })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for device_to_routine"
            })

    @staticmethod
    def _handle_user_device_permissions(
        data: Dict[str, Any],
        operation: str,
        user_id_target: str,
        device_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle user-device permission relationships"""
        users = data.get('users', {})
        devices = data.get('devices', {})
        user_device_perms = data.get('user_device_permissions', {})

        user_target = users.get(user_id_target)
        device = devices.get(device_id)

        if not user_target:
            return json.dumps({"error": f"User {user_id_target} not found"})
        if not device:
            return json.dumps({"error": f"Device {device_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'assign':
            # Grant user permission to device
            perm_key = f"{user_id_target}_{device_id}"

            if perm_key in user_device_perms:
                return json.dumps({
                    "error": f"User {user_id_target} already has permission for device {device_id}"
                })

            user_device_perms[perm_key] = {
                "user_id": user_id_target,
                "device_id": device_id,
                "permission_level": relationship_data.get('permission_level', 'full_control') if relationship_data else 'full_control',
                "granted_by_user_id": user_id,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Update user's authorized devices list
            if 'authorized_device_ids' not in user_target:
                user_target['authorized_device_ids'] = []
            if device_id not in user_target['authorized_device_ids']:
                user_target['authorized_device_ids'].append(device_id)

            return json.dumps({
                "success": True,
                "operation": "assign",
                "relationship_type": "user_device_permissions",
                "user_id": user_id_target,
                "device_id": device_id,
                "message": f"User {user_id_target} granted permission to device {device_id}"
            })

        elif operation == 'remove':
            # Revoke user permission from device
            perm_key = f"{user_id_target}_{device_id}"

            if perm_key in user_device_perms:
                del user_device_perms[perm_key]

            # Remove from user's authorized devices list
            if 'authorized_device_ids' in user_target and device_id in user_target['authorized_device_ids']:
                user_target['authorized_device_ids'].remove(device_id)

            return json.dumps({
                "success": True,
                "operation": "remove",
                "relationship_type": "user_device_permissions",
                "user_id": user_id_target,
                "device_id": device_id,
                "message": f"User {user_id_target} permission revoked for device {device_id}"
            })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for user_device_permissions"
            })

    @staticmethod
    def _handle_user_group_permissions(
        data: Dict[str, Any],
        operation: str,
        user_id_target: str,
        group_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle user-group permission relationships"""
        users = data.get('users', {})
        groups = data.get('groups', {})
        user_group_perms = data.get('user_group_permissions', {})

        user_target = users.get(user_id_target)
        group = groups.get(group_id)

        if not user_target:
            return json.dumps({"error": f"User {user_id_target} not found"})
        if not group:
            return json.dumps({"error": f"Group {group_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'assign':
            # Grant user permission to group
            perm_key = f"{user_id_target}_{group_id}"

            if perm_key in user_group_perms:
                return json.dumps({
                    "error": f"User {user_id_target} already has permission for group {group_id}"
                })

            user_group_perms[perm_key] = {
                "user_id": user_id_target,
                "group_id": group_id,
                "permission_level": relationship_data.get('permission_level', 'full_control') if relationship_data else 'full_control',
                "granted_by_user_id": user_id,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            # Update user's authorized groups list
            if 'authorized_group_ids' not in user_target:
                user_target['authorized_group_ids'] = []
            if group_id not in user_target['authorized_group_ids']:
                user_target['authorized_group_ids'].append(group_id)

            return json.dumps({
                "success": True,
                "operation": "assign",
                "relationship_type": "user_group_permissions",
                "user_id": user_id_target,
                "group_id": group_id,
                "message": f"User {user_id_target} granted permission to group {group_id}"
            })

        elif operation == 'remove':
            # Revoke user permission from group
            perm_key = f"{user_id_target}_{group_id}"

            if perm_key in user_group_perms:
                del user_group_perms[perm_key]

            # Remove from user's authorized groups list
            if 'authorized_group_ids' in user_target and group_id in user_target['authorized_group_ids']:
                user_target['authorized_group_ids'].remove(group_id)

            return json.dumps({
                "success": True,
                "operation": "remove",
                "relationship_type": "user_group_permissions",
                "user_id": user_id_target,
                "group_id": group_id,
                "message": f"User {user_id_target} permission revoked for group {group_id}"
            })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for user_group_permissions"
            })

    @staticmethod
    def _handle_skill_device_permissions(
        data: Dict[str, Any],
        operation: str,
        skill_id: str,
        device_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle skill-device permission relationships"""
        skills = data.get('skills', {})
        devices = data.get('devices', {})
        skill_device_perms = data.get('skill_device_permissions', {})

        skill = skills.get(skill_id)
        device = devices.get(device_id)

        if not skill:
            return json.dumps({"error": f"Skill {skill_id} not found"})
        if not device:
            return json.dumps({"error": f"Device {device_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'assign':
            # Grant skill permission to device
            perm_key = f"{skill_id}_{device_id}"

            if perm_key in skill_device_perms:
                return json.dumps({
                    "error": f"Skill {skill_id} already has permission for device {device_id}"
                })

            skill_device_perms[perm_key] = {
                "skill_id": skill_id,
                "device_id": device_id,
                "permission_granted": True,
                "granted_by_user_id": user_id,
                "created_at": timestamp,
                "updated_at": timestamp
            }

            return json.dumps({
                "success": True,
                "operation": "assign",
                "relationship_type": "skill_device_permissions",
                "skill_id": skill_id,
                "device_id": device_id,
                "message": f"Skill {skill_id} granted permission to device {device_id}"
            })

        elif operation == 'remove':
            # Revoke skill permission from device
            perm_key = f"{skill_id}_{device_id}"

            if perm_key in skill_device_perms:
                del skill_device_perms[perm_key]
                return json.dumps({
                    "success": True,
                    "operation": "remove",
                    "relationship_type": "skill_device_permissions",
                    "skill_id": skill_id,
                    "device_id": device_id,
                    "message": f"Skill {skill_id} permission revoked for device {device_id}"
                })
            else:
                return json.dumps({
                    "error": f"Skill {skill_id} does not have permission for device {device_id}"
                })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for skill_device_permissions"
            })

    @staticmethod
    def _handle_routine_ownership(
        data: Dict[str, Any],
        operation: str,
        routine_id: str,
        new_owner_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle routine ownership updates"""
        routines = data.get('routines', {})
        users = data.get('users', {})

        routine = routines.get(routine_id)
        new_owner = users.get(new_owner_id)

        if not routine:
            return json.dumps({"error": f"Routine {routine_id} not found"})
        if not new_owner:
            return json.dumps({"error": f"User {new_owner_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'update_reference':
            # Update routine ownership
            old_owner_id = routine.get('created_by_user_id')
            routine['created_by_user_id'] = new_owner_id
            routine['updated_at'] = timestamp

            return json.dumps({
                "success": True,
                "operation": "update_reference",
                "relationship_type": "routine_ownership",
                "routine_id": routine_id,
                "old_owner_id": old_owner_id,
                "new_owner_id": new_owner_id,
                "message": f"Routine {routine_id} ownership transferred to {new_owner_id}"
            })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for routine_ownership. Use 'update_reference'."
            })

    @staticmethod
    def _handle_routine_device_reference(
        data: Dict[str, Any],
        operation: str,
        routine_id: str,
        device_id: str,
        user_id: str,
        relationship_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle routine device reference updates"""
        routines = data.get('routines', {})
        devices = data.get('devices', {})
        routine_devices = data.get('routine_devices', {})

        routine = routines.get(routine_id)
        device = devices.get(device_id)

        if not routine:
            return json.dumps({"error": f"Routine {routine_id} not found"})
        if not device:
            return json.dumps({"error": f"Device {device_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        if operation == 'update_reference':
            # Update device reference in routine
            rel_key = f"{routine_id}_{device_id}"

            if rel_key not in routine_devices:
                return json.dumps({
                    "error": f"Device {device_id} not assigned to routine {routine_id}"
                })

            if relationship_data:
                routine_devices[rel_key].update(relationship_data)
                routine_devices[rel_key]['updated_at'] = timestamp

            return json.dumps({
                "success": True,
                "operation": "update_reference",
                "relationship_type": "routine_device_reference",
                "routine_id": routine_id,
                "device_id": device_id,
                "message": f"Device reference updated in routine {routine_id}"
            })

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported for routine_device_reference. Use 'update_reference'."
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "map_entities",
                "description": """Manage relationships between entities in the smart home system. Supports operations
                to assign, remove, and update references between entities including device-to-group, device-to-routine,
                user permissions, skill permissions, and routine ownership. Requires user authentication and appropriate
                authorization (Admin required for permission management).""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Operation to perform: 'assign' (create relationship), 'remove' (delete relationship), 'update_reference' (modify relationship)",
                            "enum": ["assign", "remove", "update_reference"]
                        },
                        "relationship_type": {
                            "type": "string",
                            "description": """Type of relationship to manage:
                            - 'device_to_group': Assign/remove device to/from group
                            - 'device_to_routine': Add/remove device to/from routine
                            - 'user_device_permissions': Manage user permissions for devices (Admin only)
                            - 'user_group_permissions': Manage user permissions for groups (Admin only)
                            - 'skill_device_permissions': Manage skill permissions for devices (Admin only)
                            - 'routine_ownership': Update routine ownership (Admin only)
                            - 'routine_device_reference': Update device references in routines""",
                            "enum": ["device_to_group", "device_to_routine", "user_device_permissions",
                                     "user_group_permissions", "skill_device_permissions", "routine_ownership",
                                     "routine_device_reference"]
                        },
                        "source_entity_id": {
                            "type": "string",
                            "description": "Source entity ID (e.g., device_id, user_id, skill_id, routine_id depending on relationship type)"
                        },
                        "target_entity_id": {
                            "type": "string",
                            "description": "Target entity ID (e.g., group_id, routine_id, device_id, user_id depending on relationship type)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the operation (required for authentication and authorization)"
                        },
                        "relationship_data": {
                            "type": "object",
                            "description": """Optional additional relationship-specific data. Examples:
                            - For device_to_routine: {'action': 'turn_on', 'parameters': {...}}
                            - For user permissions: {'permission_level': 'full_control' or 'restricted'}"""
                        }
                    },
                    "required": ["operation", "relationship_type", "source_entity_id", "target_entity_id", "user_id"]
                }
            }
        }
