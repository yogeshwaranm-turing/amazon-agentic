import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class VerifyAuthorization(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        authorization_type: str,
        user_id: str,
        required_role: Optional[str] = None,
        device_id: Optional[str] = None,
        routine_id: Optional[str] = None,
        group_id: Optional[str] = None
    ) -> str:
        """
        Verify user authorization for operations.
        
        Supported authorization types:
        - user_role: Verify user has required role (Admin, Household_Member, Guest)
        - user_device_access: Verify user has access to specific device
        - user_role_or_ownership: Verify user has required role OR owns the resource
        - device_access: Verify user can access device (includes group permissions)
        - profile_ownership: Verify user owns the profile/resource
        - user_group_access: Verify user has access to specific group
        - user_routine_access: Verify user has access to specific routine
        - batch_device_access: Verify user has access to multiple devices
        - skill_management: Verify user can manage skills (Admin only)
        """
        
        VALID_AUTHORIZATION_TYPES = [
            "user_role",
            "user_device_access",
            "user_role_or_ownership",
            "device_access",
            "profile_ownership",
            "user_group_access",
            "user_routine_access",
            "batch_device_access",
            "skill_management"
        ]
        
        if authorization_type not in VALID_AUTHORIZATION_TYPES:
            return json.dumps({
                "success": False,
                "error": f"Invalid authorization_type '{authorization_type}'. Must be one of: {', '.join(VALID_AUTHORIZATION_TYPES)}"
            })
        
        if not user_id:
            return json.dumps({
                "success": False,
                "error": "user_id is required"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # Route to appropriate authorization handler
        try:
            if authorization_type == "user_role":
                return VerifyAuthorization._check_user_role(data, user_id, required_role)
            
            elif authorization_type == "user_device_access":
                return VerifyAuthorization._check_user_device_access(data, user_id, device_id)
            
            elif authorization_type == "user_role_or_ownership":
                return VerifyAuthorization._check_user_role_or_ownership(data, user_id, required_role, routine_id)
            
            elif authorization_type == "device_access":
                return VerifyAuthorization._check_device_access(data, user_id, device_id)
            
            elif authorization_type == "profile_ownership":
                return VerifyAuthorization._check_profile_ownership(data, user_id, routine_id)
            
            elif authorization_type == "user_group_access":
                return VerifyAuthorization._check_user_group_access(data, user_id, group_id)
            
            elif authorization_type == "user_routine_access":
                return VerifyAuthorization._check_user_routine_access(data, user_id, routine_id)
            
            elif authorization_type == "batch_device_access":
                return VerifyAuthorization._check_batch_device_access(data, user_id, device_id)
            
            elif authorization_type == "skill_management":
                return VerifyAuthorization._check_skill_management(data, user_id)
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Authorization check failed: {str(e)}"
            })
    
    # ==================== Authorization Handler Methods ====================
    
    @staticmethod
    def _check_user_role(data: Dict[str, Any], user_id: str, required_role: Optional[str]) -> str:
        """Verify user has required role"""
        if not required_role:
            return json.dumps({
                "success": False,
                "error": "required_role is required for user_role authorization type"
            })
        
        VALID_ROLES = ["Admin", "Household_Member", "Guest"]
        
        if required_role not in VALID_ROLES:
            return json.dumps({
                "success": False,
                "error": f"Invalid required_role '{required_role}'. Must be one of: {', '.join(VALID_ROLES)}"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "user_role": user_role,
                "required_role": required_role,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Check if user has required role
        authorized = user_role == required_role
        
        return json.dumps({
            "success": True,
            "authorized": authorized,
            "user_id": user_id,
            "user_role": user_role,
            "required_role": required_role,
            "account_status": account_status
        })
    
    @staticmethod
    def _check_user_device_access(data: Dict[str, Any], user_id: str, device_id: Optional[str]) -> str:
        """Verify user has access to specific device"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required for user_device_access authorization type"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        permission_level = user.get("permission_level", "full_control")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "device_id": device_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Admins have access to all devices
        if user_role == "Admin":
            return json.dumps({
                "success": True,
                "authorized": True,
                "user_id": user_id,
                "user_role": user_role,
                "device_id": device_id,
                "access_reason": "Admin has full access"
            })
        
        # For restricted users, check authorized_device_ids
        if permission_level == "restricted":
            authorized_device_ids = user.get("authorized_device_ids", [])
            authorized = device_id in authorized_device_ids
            
            return json.dumps({
                "success": True,
                "authorized": authorized,
                "user_id": user_id,
                "user_role": user_role,
                "device_id": device_id,
                "permission_level": permission_level,
                "reason": "Device in authorized list" if authorized else "Device not in authorized list"
            })
        
        # Full control users have access to all devices
        return json.dumps({
            "success": True,
            "authorized": True,
            "user_id": user_id,
            "user_role": user_role,
            "device_id": device_id,
            "permission_level": permission_level,
            "access_reason": "Full control permission"
        })
    
    @staticmethod
    def _check_user_role_or_ownership(data: Dict[str, Any], user_id: str, required_role: Optional[str], routine_id: Optional[str]) -> str:
        """Verify user has required role OR owns the resource"""
        if not required_role and not routine_id:
            return json.dumps({
                "success": False,
                "error": "Either required_role or routine_id must be provided"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Check role if required_role provided
        has_required_role = False
        if required_role:
            has_required_role = user_role == required_role
        
        # Check ownership if routine_id provided
        is_owner = False
        if routine_id:
            routines = data.get("routines", {})
            routine = routines.get(routine_id, {})
            created_by = routine.get("created_by_user_id")
            is_owner = created_by == user_id
        
        authorized = has_required_role or is_owner
        
        authorization_reason = []
        if has_required_role:
            authorization_reason.append(f"Has required role: {required_role}")
        if is_owner:
            authorization_reason.append(f"Owns resource: {routine_id}")
        
        return json.dumps({
            "success": True,
            "authorized": authorized,
            "user_id": user_id,
            "user_role": user_role,
            "has_required_role": has_required_role,
            "is_owner": is_owner,
            "authorization_reason": ", ".join(authorization_reason) if authorization_reason else "No authorization"
        })
    
    @staticmethod
    def _check_device_access(data: Dict[str, Any], user_id: str, device_id: Optional[str]) -> str:
        """Verify user can access device (includes group permissions)"""
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required for device_access authorization type"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        permission_level = user.get("permission_level", "full_control")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "device_id": device_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Admins have access to all devices
        if user_role == "Admin":
            return json.dumps({
                "success": True,
                "authorized": True,
                "user_id": user_id,
                "user_role": user_role,
                "device_id": device_id,
                "access_method": "admin_role"
            })
        
        # Check direct device access
        authorized_device_ids = user.get("authorized_device_ids", [])
        has_direct_access = device_id in authorized_device_ids
        
        # Check group-based access
        devices = data.get("devices", {})
        device = devices.get(device_id, {})
        device_group_id = device.get("group_id")
        
        has_group_access = False
        if device_group_id:
            authorized_group_ids = user.get("authorized_group_ids", [])
            has_group_access = device_group_id in authorized_group_ids
        
        authorized = has_direct_access or has_group_access or permission_level == "full_control"
        
        access_method = None
        if has_direct_access:
            access_method = "direct_device_permission"
        elif has_group_access:
            access_method = "group_permission"
        elif permission_level == "full_control":
            access_method = "full_control_permission"
        
        return json.dumps({
            "success": True,
            "authorized": authorized,
            "user_id": user_id,
            "user_role": user_role,
            "device_id": device_id,
            "access_method": access_method,
            "permission_level": permission_level
        })
    
    @staticmethod
    def _check_profile_ownership(data: Dict[str, Any], user_id: str, routine_id: Optional[str]) -> str:
        """Verify user owns the profile/resource"""
        if not routine_id:
            return json.dumps({
                "success": False,
                "error": "routine_id is required for profile_ownership authorization type"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        account_status = user.get("account_status", "active")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "routine_id": routine_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Check ownership
        routines = data.get("routines", {})
        routine = routines.get(routine_id)
        
        if not routine:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"Routine {routine_id} not found"
            })
        
        created_by = routine.get("created_by_user_id")
        is_owner = created_by == user_id
        
        return json.dumps({
            "success": True,
            "authorized": is_owner,
            "user_id": user_id,
            "routine_id": routine_id,
            "is_owner": is_owner,
            "created_by": created_by
        })
    
    @staticmethod
    def _check_user_group_access(data: Dict[str, Any], user_id: str, group_id: Optional[str]) -> str:
        """Verify user has access to specific group"""
        if not group_id:
            return json.dumps({
                "success": False,
                "error": "group_id is required for user_group_access authorization type"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        permission_level = user.get("permission_level", "full_control")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "group_id": group_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Admins have access to all groups
        if user_role == "Admin":
            return json.dumps({
                "success": True,
                "authorized": True,
                "user_id": user_id,
                "user_role": user_role,
                "group_id": group_id,
                "access_reason": "Admin has full access"
            })
        
        # Check authorized groups
        authorized_group_ids = user.get("authorized_group_ids", [])
        authorized = group_id in authorized_group_ids or permission_level == "full_control"
        
        return json.dumps({
            "success": True,
            "authorized": authorized,
            "user_id": user_id,
            "user_role": user_role,
            "group_id": group_id,
            "permission_level": permission_level
        })
    
    @staticmethod
    def _check_user_routine_access(data: Dict[str, Any], user_id: str, routine_id: Optional[str]) -> str:
        """Verify user has access to specific routine"""
        if not routine_id:
            return json.dumps({
                "success": False,
                "error": "routine_id is required for user_routine_access authorization type"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "routine_id": routine_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Admins have access to all routines
        if user_role == "Admin":
            return json.dumps({
                "success": True,
                "authorized": True,
                "user_id": user_id,
                "user_role": user_role,
                "routine_id": routine_id,
                "access_reason": "Admin has full access"
            })
        
        # Check if user created the routine
        routines = data.get("routines", {})
        routine = routines.get(routine_id)
        
        if not routine:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"Routine {routine_id} not found"
            })
        
        created_by = routine.get("created_by_user_id")
        authorized = created_by == user_id
        
        return json.dumps({
            "success": True,
            "authorized": authorized,
            "user_id": user_id,
            "user_role": user_role,
            "routine_id": routine_id,
            "is_creator": authorized
        })
    
    @staticmethod
    def _check_batch_device_access(data: Dict[str, Any], user_id: str, device_ids: Optional[str]) -> str:
        """Verify user has access to multiple devices"""
        if not device_ids:
            return json.dumps({
                "success": False,
                "error": "device_ids is required for batch_device_access authorization type"
            })
        
        # Parse device_ids if it's a string (comma-separated)
        if isinstance(device_ids, str):
            device_id_list = [d.strip() for d in device_ids.split(",")]
        elif isinstance(device_ids, list):
            device_id_list = device_ids
        else:
            return json.dumps({
                "success": False,
                "error": "device_ids must be a comma-separated string or list"
            })
        
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Admins have access to all devices
        if user_role == "Admin":
            return json.dumps({
                "success": True,
                "authorized": True,
                "user_id": user_id,
                "user_role": user_role,
                "device_count": len(device_id_list),
                "all_authorized": True,
                "access_reason": "Admin has full access"
            })
        
        # Check each device
        authorized_device_ids = user.get("authorized_device_ids", [])
        authorized_group_ids = user.get("authorized_group_ids", [])
        permission_level = user.get("permission_level", "full_control")
        
        devices = data.get("devices", {})
        
        authorized_devices = []
        unauthorized_devices = []
        
        for device_id in device_id_list:
            # Check direct access
            has_direct_access = device_id in authorized_device_ids
            
            # Check group access
            device = devices.get(device_id, {})
            device_group_id = device.get("group_id")
            has_group_access = device_group_id in authorized_group_ids if device_group_id else False
            
            if has_direct_access or has_group_access or permission_level == "full_control":
                authorized_devices.append(device_id)
            else:
                unauthorized_devices.append(device_id)
        
        all_authorized = len(unauthorized_devices) == 0
        
        return json.dumps({
            "success": True,
            "authorized": all_authorized,
            "user_id": user_id,
            "user_role": user_role,
            "device_count": len(device_id_list),
            "authorized_count": len(authorized_devices),
            "unauthorized_count": len(unauthorized_devices),
            "all_authorized": all_authorized,
            "unauthorized_devices": unauthorized_devices if unauthorized_devices else None
        })
    
    @staticmethod
    def _check_skill_management(data: Dict[str, Any], user_id: str) -> str:
        """Verify user can manage skills (Admin only)"""
        users = data.get("users", {})
        user = users.get(user_id)
        
        if not user:
            return json.dumps({
                "success": False,
                "authorized": False,
                "error": f"User {user_id} not found"
            })
        
        user_role = user.get("role")
        account_status = user.get("account_status", "active")
        
        # Check if account is active
        if account_status != "active":
            return json.dumps({
                "success": True,
                "authorized": False,
                "user_id": user_id,
                "reason": f"Account status is '{account_status}', not 'active'"
            })
        
        # Only Admins can manage skills
        authorized = user_role == "Admin"
        
        return json.dumps({
            "success": True,
            "authorized": authorized,
            "user_id": user_id,
            "user_role": user_role,
            "can_manage_skills": authorized,
            "reason": "Admin role required for skill management" if not authorized else "Admin has skill management access"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "verify_authorization",
                "description": "Verify user authorization for operations. Authorization types: 'user_role' (verify user has required role; requires user_id, required_role: 'Admin', 'Household_Member', or 'Guest'), 'user_device_access' (verify user has access to device; requires user_id, device_id), 'user_role_or_ownership' (verify user has role OR owns resource; requires user_id, required_role or routine_id), 'device_access' (verify user can access device including group permissions; requires user_id, device_id), 'profile_ownership' (verify user owns profile/resource; requires user_id, routine_id), 'user_group_access' (verify user has access to group; requires user_id, group_id), 'user_routine_access' (verify user has access to routine; requires user_id, routine_id), 'batch_device_access' (verify user has access to multiple devices; requires user_id, device_ids as comma-separated string or list), 'skill_management' (verify user can manage skills, Admin only; requires user_id).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "authorization_type": {
                            "type": "string",
                            "enum": [
                                "user_role",
                                "user_device_access",
                                "user_role_or_ownership",
                                "device_access",
                                "profile_ownership",
                                "user_group_access",
                                "user_routine_access",
                                "batch_device_access",
                                "skill_management"
                            ],
                            "description": "Type of authorization check to perform"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User identifier (required for all authorization types)"
                        },
                        "required_role": {
                            "type": "string",
                            "enum": ["Admin", "Household_Member", "Guest"],
                            "description": "Required role for operation (used with user_role and user_role_or_ownership types)"
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Device ID for device-specific authorization (used with user_device_access, device_access types) or comma-separated device IDs for batch_device_access"
                        },
                        "routine_id": {
                            "type": "string",
                            "description": "Routine ID for ownership checks (used with user_role_or_ownership, profile_ownership, user_routine_access types)"
                        },
                        "group_id": {
                            "type": "string",
                            "description": "Group ID for group access checks (used with user_group_access type)"
                        }
                    },
                    "required": ["authorization_type", "user_id"]
                }
            }
        }