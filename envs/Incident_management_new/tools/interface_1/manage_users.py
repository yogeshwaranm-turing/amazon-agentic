import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageUsers(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, user_data: Dict[str, Any] = None, user_id: str = None) -> str:
        """
        Create or update user records.
        
        Actions:
        - create: Create new user record (requires user_data with first_name, last_name, email, role, timezone, status)
        - update: Update existing user record (requires user_id and user_data with changes)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        # Access users data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for users"
            })
        
        users = data.get("users", {})
        
        if action == "create":
            if not user_data:
                return json.dumps({
                    "success": False,
                    "error": "user_data is required for create action"
                })
            
            # Validate required fields for creation
            required_fields = ["first_name", "last_name", "email", "role", "timezone", "status"]
            missing_fields = [field for field in required_fields if field not in user_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Missing required fields for user creation: {', '.join(missing_fields)}"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["client_id", "vendor_id", "first_name", "last_name", "email", "phone", "role", "department", "timezone", "status"]
            invalid_fields = [field for field in user_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for user creation: {', '.join(invalid_fields)}"
                })
            
            # Validate role enum
            valid_roles = ["incident_manager", "technical_support", "account_manager", "executive", "vendor_contact", "system_administrator", "client_contact"]
            if user_data["role"] not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                })
            
            # Validate status enum
            valid_statuses = ["active", "inactive", "on_leave"]
            if user_data["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Check for duplicate email
            email = user_data["email"].strip().lower()
            for existing_user in users.values():
                if existing_user.get("email", "").strip().lower() == email:
                    return json.dumps({
                        "success": False,
                        "error": f"User with email '{user_data['email']}' already exists"
                    })
            
            # Generate new user ID
            new_user_id = generate_id(users)
            
            # Create new user record
            new_user = {
                "user_id": str(new_user_id),
                "client_id": user_data.get("client_id"),
                "vendor_id": user_data.get("vendor_id"),
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "phone": user_data.get("phone"),
                "role": user_data["role"],
                "department": user_data.get("department"),
                "timezone": user_data["timezone"],
                "status": user_data["status"],
                "created_at": "2025-10-01T00:00:00",
                "updated_at": "2025-10-01T00:00:00"
            }
            
            users[str(new_user_id)] = new_user
            return json.dumps(new_user)
        
        elif action == "update":
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "user_id is required for update action"
                })
            
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"User {user_id} not found"
                })
            
            if not user_data:
                return json.dumps({
                    "success": False,
                    "error": "user_data is required for update action"
                })
            
            # Validate only allowed fields are present for updates
            allowed_update_fields = ["client_id", "vendor_id", "first_name", "last_name", "email", "phone", "role", "department", "timezone", "status"]
            invalid_fields = [field for field in user_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for user update: {', '.join(invalid_fields)}"
                })
            
            # Validate role enum if provided
            if "role" in user_data:
                valid_roles = ["incident_manager", "technical_support", "account_manager", "executive", "vendor_contact", "system_administrator", "client_contact"]
                if user_data["role"] not in valid_roles:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid role. Must be one of: {', '.join(valid_roles)}"
                    })
            
            # Validate status enum if provided
            if "status" in user_data:
                valid_statuses = ["active", "inactive", "on_leave"]
                if user_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Check for duplicate email if updating email
            if "email" in user_data:
                new_email = user_data["email"].strip().lower()
                for existing_user_id, existing_user in users.items():
                    if (existing_user_id != user_id and 
                        existing_user.get("email", "").strip().lower() == new_email):
                        return json.dumps({
                            "success": False,
                            "error": f"User with email '{user_data['email']}' already exists"
                        })
            
            # Update user record
            current_user = users[user_id].copy()
            for key, value in user_data.items():
                current_user[key] = value
            
            current_user["updated_at"] = "2025-10-01T00:00:00"
            users[user_id] = current_user
            
            return json.dumps(current_user)
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_users",
                "description": "Create or update user records in the incident management system. This tool manages the complete user lifecycle including creation of new user records and updates to existing user configurations. For creation, establishes new user records with comprehensive validation to ensure data integrity and business rule adherence. For updates, modifies existing user records while maintaining data integrity. Validates user roles, prevents duplicate emails, and manages user status according to business rules. Essential for user management, access control, and incident assignment operations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new user record, 'update' to modify existing user record",
                            "enum": ["create", "update"]
                        },
                        "user_data": {
                            "type": "object",
                            "description": "User data object. For create: requires first_name, last_name, email (unique), role (enum), timezone, status (enum), with optional client_id, vendor_id, phone, department. For update: includes user fields to change. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "client_id": {
                                    "type": "string",
                                    "description": "Associated client ID (optional)"
                                },
                                "vendor_id": {
                                    "type": "string",
                                    "description": "Associated vendor ID (optional)"
                                },
                                "first_name": {
                                    "type": "string",
                                    "description": "User's first name (required for create)"
                                },
                                "last_name": {
                                    "type": "string",
                                    "description": "User's last name (required for create)"
                                },
                                "email": {
                                    "type": "string",
                                    "description": "User's email address (must be unique across all users, required for create)"
                                },
                                "phone": {
                                    "type": "string",
                                    "description": "User's phone number (optional)"
                                },
                                "role": {
                                    "type": "string",
                                    "description": "User's role (incident_manager, technical_support, account_manager, executive, vendor_contact, system_administrator, client_contact)",
                                    "enum": ["incident_manager", "technical_support", "account_manager", "executive", "vendor_contact", "system_administrator", "client_contact"]
                                },
                                "department": {
                                    "type": "string",
                                    "description": "User's department (optional)"
                                },
                                "timezone": {
                                    "type": "string",
                                    "description": "User's timezone (required for create)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "User operational status (active, inactive, on_leave)",
                                    "enum": ["active", "inactive", "on_leave"]
                                }
                            }
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }
