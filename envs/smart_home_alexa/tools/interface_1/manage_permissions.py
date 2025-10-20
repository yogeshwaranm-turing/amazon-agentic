import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from tau_bench.envs.tool import Tool


class ManagePermissions(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        permission_type: str,
        subject_id: str,
        target_ids: Union[List[str], str],
        user_id: str,
        permission_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Manage user and skill permissions for devices and groups.

        Supports operations:
        - grant: Grant permissions to user/skill for devices/groups
        - revoke: Revoke permissions from user/skill for devices/groups

        Permission types:
        - user_device: Manage user permissions for devices
        - user_group: Manage user permissions for groups
        - skill_device: Manage skill permissions for devices
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

        # Only Admins can manage permissions
        if user_role != 'Admin':
            return json.dumps({
                "error": "Admin authorization required to manage permissions"
            })

        # Validate operation
        valid_operations = ['grant', 'revoke']
        if operation not in valid_operations:
            return json.dumps({
                "error": f"Invalid operation: {operation}",
                "supported_operations": valid_operations
            })

        # Validate permission_type
        valid_permission_types = ['user_device', 'user_group', 'skill_device']
        if permission_type not in valid_permission_types:
            return json.dumps({
                "error": f"Invalid permission_type: {permission_type}",
                "supported_types": valid_permission_types
            })

        # Parse target_ids if it's a string (comma-separated)
        if isinstance(target_ids, str):
            target_id_list = [t.strip() for t in target_ids.split(",")]
        elif isinstance(target_ids, list):
            target_id_list = target_ids
        else:
            return json.dumps({
                "error": "target_ids must be a comma-separated string or list"
            })

        if not target_id_list:
            return json.dumps({
                "error": "target_ids cannot be empty"
            })

        # Route to appropriate handler
        try:
            if permission_type == 'user_device':
                return ManagePermissions._handle_user_device_permissions(
                    data, operation, subject_id, target_id_list, user_id, permission_data
                )
            elif permission_type == 'user_group':
                return ManagePermissions._handle_user_group_permissions(
                    data, operation, subject_id, target_id_list, user_id, permission_data
                )
            elif permission_type == 'skill_device':
                return ManagePermissions._handle_skill_device_permissions(
                    data, operation, subject_id, target_id_list, user_id, permission_data
                )
        except Exception as e:
            return json.dumps({
                "error": f"Operation failed: {str(e)}"
            })

    @staticmethod
    def _handle_user_device_permissions(
        data: Dict[str, Any],
        operation: str,
        user_id_target: str,
        device_ids: List[str],
        user_id: str,
        permission_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle user-device permissions (batch operation)"""
        users = data.get('users', {})
        devices = data.get('devices', {})
        user_device_perms = data.get('user_device_permissions', {})

        user_target = users.get(user_id_target)
        if not user_target:
            return json.dumps({"error": f"User {user_id_target} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"
        permission_level = permission_data.get('permission_level', 'full_control') if permission_data else 'full_control'

        results = {
            "success": True,
            "operation": operation,
            "permission_type": "user_device",
            "subject_id": user_id_target,
            "total_targets": len(device_ids),
            "successful": [],
            "failed": []
        }

        if operation == 'grant':
            # Grant user permissions to multiple devices
            for device_id in device_ids:
                device = devices.get(device_id)
                if not device:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Device not found"
                    })
                    continue

                perm_key = f"{user_id_target}_{device_id}"

                # Check if permission already exists
                if perm_key in user_device_perms:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Permission already exists"
                    })
                    continue

                # Create permission
                user_device_perms[perm_key] = {
                    "user_id": user_id_target,
                    "device_id": device_id,
                    "permission_level": permission_level,
                    "granted_by_user_id": user_id,
                    "created_at": timestamp,
                    "updated_at": timestamp
                }

                # Update user's authorized devices list
                if 'authorized_device_ids' not in user_target:
                    user_target['authorized_device_ids'] = []
                if device_id not in user_target['authorized_device_ids']:
                    user_target['authorized_device_ids'].append(device_id)

                results["successful"].append({
                    "device_id": device_id,
                    "permission_level": permission_level
                })

            results["successful_count"] = len(results["successful"])
            results["failed_count"] = len(results["failed"])
            results["message"] = f"Granted permissions to {results['successful_count']} of {results['total_targets']} devices"

            return json.dumps(results)

        elif operation == 'revoke':
            # Revoke user permissions from multiple devices
            for device_id in device_ids:
                device = devices.get(device_id)
                if not device:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Device not found"
                    })
                    continue

                perm_key = f"{user_id_target}_{device_id}"

                # Check if permission exists
                if perm_key not in user_device_perms:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Permission does not exist"
                    })
                    continue

                # Remove permission
                del user_device_perms[perm_key]

                # Remove from user's authorized devices list
                if 'authorized_device_ids' in user_target and device_id in user_target['authorized_device_ids']:
                    user_target['authorized_device_ids'].remove(device_id)

                results["successful"].append({
                    "device_id": device_id
                })

            results["successful_count"] = len(results["successful"])
            results["failed_count"] = len(results["failed"])
            results["message"] = f"Revoked permissions from {results['successful_count']} of {results['total_targets']} devices"

            return json.dumps(results)

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported"
            })

    @staticmethod
    def _handle_user_group_permissions(
        data: Dict[str, Any],
        operation: str,
        user_id_target: str,
        group_ids: List[str],
        user_id: str,
        permission_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle user-group permissions (batch operation)"""
        users = data.get('users', {})
        groups = data.get('groups', {})
        user_group_perms = data.get('user_group_permissions', {})

        user_target = users.get(user_id_target)
        if not user_target:
            return json.dumps({"error": f"User {user_id_target} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"
        permission_level = permission_data.get('permission_level', 'full_control') if permission_data else 'full_control'

        results = {
            "success": True,
            "operation": operation,
            "permission_type": "user_group",
            "subject_id": user_id_target,
            "total_targets": len(group_ids),
            "successful": [],
            "failed": []
        }

        if operation == 'grant':
            # Grant user permissions to multiple groups
            for group_id in group_ids:
                group = groups.get(group_id)
                if not group:
                    results["failed"].append({
                        "group_id": group_id,
                        "reason": "Group not found"
                    })
                    continue

                perm_key = f"{user_id_target}_{group_id}"

                # Check if permission already exists
                if perm_key in user_group_perms:
                    results["failed"].append({
                        "group_id": group_id,
                        "reason": "Permission already exists"
                    })
                    continue

                # Create permission
                user_group_perms[perm_key] = {
                    "user_id": user_id_target,
                    "group_id": group_id,
                    "permission_level": permission_level,
                    "granted_by_user_id": user_id,
                    "created_at": timestamp,
                    "updated_at": timestamp
                }

                # Update user's authorized groups list
                if 'authorized_group_ids' not in user_target:
                    user_target['authorized_group_ids'] = []
                if group_id not in user_target['authorized_group_ids']:
                    user_target['authorized_group_ids'].append(group_id)

                results["successful"].append({
                    "group_id": group_id,
                    "permission_level": permission_level
                })

            results["successful_count"] = len(results["successful"])
            results["failed_count"] = len(results["failed"])
            results["message"] = f"Granted permissions to {results['successful_count']} of {results['total_targets']} groups"

            return json.dumps(results)

        elif operation == 'revoke':
            # Revoke user permissions from multiple groups
            for group_id in group_ids:
                group = groups.get(group_id)
                if not group:
                    results["failed"].append({
                        "group_id": group_id,
                        "reason": "Group not found"
                    })
                    continue

                perm_key = f"{user_id_target}_{group_id}"

                # Check if permission exists
                if perm_key not in user_group_perms:
                    results["failed"].append({
                        "group_id": group_id,
                        "reason": "Permission does not exist"
                    })
                    continue

                # Remove permission
                del user_group_perms[perm_key]

                # Remove from user's authorized groups list
                if 'authorized_group_ids' in user_target and group_id in user_target['authorized_group_ids']:
                    user_target['authorized_group_ids'].remove(group_id)

                results["successful"].append({
                    "group_id": group_id
                })

            results["successful_count"] = len(results["successful"])
            results["failed_count"] = len(results["failed"])
            results["message"] = f"Revoked permissions from {results['successful_count']} of {results['total_targets']} groups"

            return json.dumps(results)

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported"
            })

    @staticmethod
    def _handle_skill_device_permissions(
        data: Dict[str, Any],
        operation: str,
        skill_id: str,
        device_ids: List[str],
        user_id: str,
        permission_data: Optional[Dict[str, Any]]
    ) -> str:
        """Handle skill-device permissions (batch operation)"""
        skills = data.get('skills', {})
        devices = data.get('devices', {})
        skill_device_perms = data.get('skill_device_permissions', {})

        skill = skills.get(skill_id)
        if not skill:
            return json.dumps({"error": f"Skill {skill_id} not found"})

        timestamp = datetime.utcnow().isoformat() + "Z"

        results = {
            "success": True,
            "operation": operation,
            "permission_type": "skill_device",
            "subject_id": skill_id,
            "total_targets": len(device_ids),
            "successful": [],
            "failed": []
        }

        if operation == 'grant':
            # Grant skill permissions to multiple devices
            for device_id in device_ids:
                device = devices.get(device_id)
                if not device:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Device not found"
                    })
                    continue

                perm_key = f"{skill_id}_{device_id}"

                # Check if permission already exists
                if perm_key in skill_device_perms:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Permission already exists"
                    })
                    continue

                # Create permission
                skill_device_perms[perm_key] = {
                    "skill_id": skill_id,
                    "device_id": device_id,
                    "permission_granted": True,
                    "granted_by_user_id": user_id,
                    "created_at": timestamp,
                    "updated_at": timestamp
                }

                results["successful"].append({
                    "device_id": device_id
                })

            results["successful_count"] = len(results["successful"])
            results["failed_count"] = len(results["failed"])
            results["message"] = f"Granted permissions to {results['successful_count']} of {results['total_targets']} devices"

            return json.dumps(results)

        elif operation == 'revoke':
            # Revoke skill permissions from multiple devices
            for device_id in device_ids:
                device = devices.get(device_id)
                if not device:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Device not found"
                    })
                    continue

                perm_key = f"{skill_id}_{device_id}"

                # Check if permission exists
                if perm_key not in skill_device_perms:
                    results["failed"].append({
                        "device_id": device_id,
                        "reason": "Permission does not exist"
                    })
                    continue

                # Remove permission
                del skill_device_perms[perm_key]

                results["successful"].append({
                    "device_id": device_id
                })

            results["successful_count"] = len(results["successful"])
            results["failed_count"] = len(results["failed"])
            results["message"] = f"Revoked permissions from {results['successful_count']} of {results['total_targets']} devices"

            return json.dumps(results)

        else:
            return json.dumps({
                "error": f"Operation {operation} not supported"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_permissions",
                "description": """Manage user and skill permissions for devices and groups in batch operations.
                Supports granting and revoking permissions for multiple targets at once. Requires Admin authorization.
                Returns detailed results including successful and failed operations.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Operation to perform: 'grant' (add permissions) or 'revoke' (remove permissions)",
                            "enum": ["grant", "revoke"]
                        },
                        "permission_type": {
                            "type": "string",
                            "description": """Type of permission to manage:
                            - 'user_device': User permissions for devices
                            - 'user_group': User permissions for groups
                            - 'skill_device': Skill permissions for devices""",
                            "enum": ["user_device", "user_group", "skill_device"]
                        },
                        "subject_id": {
                            "type": "string",
                            "description": "Subject identifier - User ID (for user_device, user_group) or Skill ID (for skill_device)"
                        },
                        "target_ids": {
                            "description": "List of target IDs (device IDs or group IDs) or comma-separated string. Batch operations supported.",
                            "oneOf": [
                                {"type": "array", "items": {"type": "string"}},
                                {"type": "string"}
                            ]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "ID of the user performing the operation (required for authentication, must be Admin)"
                        },
                        "permission_data": {
                            "type": "object",
                            "description": "Optional permission details. For user permissions, can include 'permission_level': 'full_control' or 'restricted'"
                        }
                    },
                    "required": ["operation", "permission_type", "subject_id", "target_ids", "user_id"]
                }
            }
        }
