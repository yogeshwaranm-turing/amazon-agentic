import json
import re
from datetime import datetime
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AdministerOnboardingOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage employee onboarding operations including checklist creation and updates.
        
        Operations:
        - create_checklist: Create new onboarding checklist (requires employee_id, start_date, position, hiring_manager_id, user_id)
        - update_checklist: Update existing onboarding checklist (requires checklist_id and optional status fields)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Convert MM-DD-YYYY to YYYY-MM-DD for internal storage
                date_pattern = r'^\d{2}-\d{2}-\d{4}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be MM-DD-YYYY"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert MM-DD-YYYY to YYYY-MM-DD"""
            if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                month, day, year = date_str.split('-')
                return f"{year}-{month}-{day}"
            return date_str
        
        def validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
            """Validate status field against allowed values"""
            if status_value and status_value not in valid_statuses:
                return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
            return None
        
        # Validate operation_type
        valid_operations = ["create_checklist", "update_checklist"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "checklist_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "checklist_id": None,
                "message": "Invalid data format for onboarding operations"
            })
        
        onboarding_checklists = data.get("onboarding_checklists", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        
        if operation_type == "create_checklist":
            # Validate required fields for checklist creation
            required_fields = ["employee_id", "start_date", "position", "hiring_manager_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Missing required fields for checklist creation: {', '.join(missing_fields)}"
                })
            
            # Validate employee exists
            if str(kwargs["employee_id"]) not in employees:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Employee {kwargs['employee_id']} not found"
                })
            
            # Validate hiring manager exists
            if str(kwargs["hiring_manager_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Hiring manager {kwargs['hiring_manager_id']} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["start_date"], "start_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": date_error
                })
            
            # Check for existing checklist for this employee
            for checklist in onboarding_checklists.values():
                if checklist.get("employee_id") == str(kwargs["employee_id"]):
                    return json.dumps({
                        "success": False,
                        "checklist_id": None,
                        "message": f"Onboarding checklist already exists for employee {kwargs['employee_id']}"
                    })
            
            # Generate new checklist ID and create record
            new_checklist_id = generate_id(onboarding_checklists)
            timestamp = datetime.now().isoformat()
            
            new_checklist = {
                "checklist_id": str(new_checklist_id),
                "employee_id": str(kwargs["employee_id"]),
                "start_date": convert_date_format(kwargs["start_date"]),
                "position": kwargs["position"],
                "hiring_manager_id": str(kwargs["hiring_manager_id"]),
                "pre_onboarding_status": "pending",
                "background_check_status": "pending",
                "background_check_cleared_date": None,
                "document_verification_status": "pending",
                "it_provisioning_status": "pending",
                "orientation_completed": False,
                "orientation_date": None,
                "benefits_enrollment_status": "pending",
                "overall_status": "not_started",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            onboarding_checklists[str(new_checklist_id)] = new_checklist
            
            return json.dumps({
                "success": True,
                "checklist": new_checklist,
                "message": f"Onboarding checklist {new_checklist_id} created successfully for employee {kwargs['employee_id']}"
            })
        
        elif operation_type == "update_checklist":
            # Validate required fields for checklist update
            if "checklist_id" not in kwargs or kwargs["checklist_id"] is None:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": "checklist_id is required for checklist update"
                })
            
            # Validate checklist exists
            if str(kwargs["checklist_id"]) not in onboarding_checklists:
                return json.dumps({
                    "success": False,
                    "checklist_id": None,
                    "message": f"Checklist {kwargs['checklist_id']} not found"
                })
            
            # Validate status fields if provided
            status_validations = [
                ("pre_onboarding_status", ["pending", "in_progress", "completed"]),
                ("background_check_status", ["pending", "in_progress", "passed", "failed"]),
                ("document_verification_status", ["pending", "verified", "failed"]),
                ("it_provisioning_status", ["pending", "in_progress", "completed"]),
                ("benefits_enrollment_status", ["pending", "in_progress", "completed"]),
                ("overall_status", ["not_started", "in_progress", "completed"])
            ]
            
            for field_name, valid_statuses in status_validations:
                if field_name in kwargs and kwargs[field_name] is not None:
                    status_error = validate_status_field(kwargs[field_name], field_name, valid_statuses)
                    if status_error:
                        return json.dumps({
                            "success": False,
                            "checklist_id": None,
                            "message": status_error
                        })
            
            # Validate date fields if provided
            date_fields = ["background_check_cleared_date", "orientation_date"]
            for field_name in date_fields:
                if field_name in kwargs and kwargs[field_name] is not None:
                    date_error = validate_date_format(kwargs[field_name], field_name)
                    if date_error:
                        return json.dumps({
                            "success": False,
                            "checklist_id": None,
                            "message": date_error
                        })
            
            # Validate boolean field if provided
            if "orientation_completed" in kwargs and kwargs["orientation_completed"] is not None:
                if not isinstance(kwargs["orientation_completed"], bool):
                    return json.dumps({
                        "success": False,
                        "checklist_id": None,
                        "message": "orientation_completed must be a boolean value (True/False)"
                    })
            
            # Update checklist record
            checklist = onboarding_checklists[str(kwargs["checklist_id"])]
            
            # Define allowed update fields
            allowed_update_fields = [
                "pre_onboarding_status", "background_check_status", "background_check_cleared_date",
                "document_verification_status", "it_provisioning_status", "orientation_completed",
                "orientation_date", "benefits_enrollment_status", "overall_status"
            ]
            
            # Update only provided fields
            for field_name in allowed_update_fields:
                if field_name in kwargs and kwargs[field_name] is not None:
                    if field_name in ["background_check_cleared_date", "orientation_date"]:
                        checklist[field_name] = convert_date_format(kwargs[field_name])
                    else:
                        checklist[field_name] = kwargs[field_name]
            
            checklist["updated_at"] = "2025-10-01T12:00:00"
            
            return json.dumps({
                "success": True,
                "checklist_id": str(kwargs["checklist_id"]),
                "message": f"Onboarding checklist {kwargs['checklist_id']} updated successfully"
            })
        
        return json.dumps({
            "success": False,
            "checklist_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_onboarding_operations",
                "description": "Manage employee onboarding operations including checklist creation and updates in the HR talent management system. This tool handles the complete onboarding workflow from initial checklist creation through ongoing progress tracking and completion. For creation, establishes new onboarding checklists with comprehensive validation to ensure employee, hiring manager, and user existence before proceeding. Prevents duplicate checklist creation for the same employee. For updates, modifies existing checklist records while maintaining data integrity and enforcing proper status transitions. Validates status fields against predefined enums, ensures proper date formatting, and handles boolean field validation. Essential for onboarding process management, compliance tracking, and ensuring new employees complete all required steps. Supports the complete onboarding lifecycle from initial checklist creation through final completion tracking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_checklist' to establish new onboarding checklist, 'update_checklist' to modify existing checklist progress",
                            "enum": ["create_checklist", "update_checklist"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee (required for create_checklist only, must exist in system)"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Employee start date in MM-DD-YYYY format (required for create_checklist only)"
                        },
                        "position": {
                            "type": "string",
                            "description": "Employee position/title (required for create_checklist only)"
                        },
                        "hiring_manager_id": {
                            "type": "string",
                            "description": "Unique identifier of the hiring manager (required for create_checklist only, must exist in system)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user creating the checklist (required for create_checklist only, must exist in system)"
                        },
                        "checklist_id": {
                            "type": "string",
                            "description": "Unique identifier of the checklist (required for update_checklist only, must exist in system)"
                        },
                        "pre_onboarding_status": {
                            "type": "string",
                            "description": "Pre-onboarding status (optional for update_checklist)",
                            "enum": ["pending", "in_progress", "completed"]
                        },
                        "background_check_status": {
                            "type": "string",
                            "description": "Background check status (optional for update_checklist)",
                            "enum": ["pending", "in_progress", "passed", "failed"]
                        },
                        "background_check_cleared_date": {
                            "type": "string",
                            "description": "Background check cleared date in MM-DD-YYYY format (optional for update_checklist)"
                        },
                        "document_verification_status": {
                            "type": "string",
                            "description": "Document verification status (optional for update_checklist)",
                            "enum": ["pending", "verified", "failed"]
                        },
                        "it_provisioning_status": {
                            "type": "string",
                            "description": "IT provisioning status (optional for update_checklist)",
                            "enum": ["pending", "in_progress", "completed"]
                        },
                        "orientation_completed": {
                            "type": "boolean",
                            "description": "Whether orientation is completed (optional for update_checklist)"
                        },
                        "orientation_date": {
                            "type": "string",
                            "description": "Orientation completion date in MM-DD-YYYY format (optional for update_checklist)"
                        },
                        "benefits_enrollment_status": {
                            "type": "string",
                            "description": "Benefits enrollment status (optional for update_checklist)",
                            "enum": ["pending", "in_progress", "completed"]
                        },
                        "overall_status": {
                            "type": "string",
                            "description": "Overall onboarding status (optional for update_checklist)",
                            "enum": ["not_started", "in_progress", "completed"]
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
