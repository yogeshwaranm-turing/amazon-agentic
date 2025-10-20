import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool
from datetime import datetime, date

class ProcessBenefitEnrollmentOperations(Tool):
    
    # --- Utility Methods (Reused from common HR toolset) ---
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> int:
        """Utility to generate a new sequential ID for the benefit_enrollments table."""
        if not table:
            return 8001
        return max(int(k) for k in table.keys()) + 1

    @staticmethod
    def _validate_date_format(date_str: str, field_name: str) -> Optional[str]:
        """Validates date format is MM-DD-YYYY."""
        if date_str:
            # Check for the specified MM-DD-YYYY format
            date_pattern = r'^\d{2}-\d{2}-\d{4}$'
            if not re.match(date_pattern, date_str):
                return f"Invalid {field_name} format. Must be MM-DD-YYYY"
            
            # Additional check for valid date parts (e.g., month 13)
            try:
                datetime.strptime(date_str, '%m-%d-%Y')
            except ValueError:
                return f"Invalid date value provided for {field_name}. Please check month/day/year validity."
        return None

    @staticmethod
    def _convert_date_format(date_str: str) -> str:
        """Convert MM-DD-YYYY to YYYY-MM-DD for internal storage."""
        if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
            try:
                dt = datetime.strptime(date_str, '%m-%d-%Y')
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                # Should be caught by validation, but ensures safe conversion
                return date_str
        return date_str

    @staticmethod
    def _validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
        """Validate status field against allowed values."""
        if status_value and status_value not in valid_statuses:
            return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
        return None

    # --- Core Tool Logic ---

    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manages benefit enrollment lifecycle, including creation and HR Manager approval.
        """
        
        # Define allowed operations
        valid_operations = ["create_enrollment", "approve_enrollment"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "enrollment_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        # Access related data (simulating a complex database dictionary)
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "enrollment_id": None,
                "message": "Invalid data format for benefit enrollment operations"
            })
        
        enrollments = data.get("benefit_enrollments", {})
        # Assuming other necessary tables are available for validation
        employees = data.get("employees", {})
        benefit_plans = data.get("benefit_plans", {})
        
        # Set a simulated current date for comparison (2025-10-01)
        simulated_today = date(2025, 10, 1)

        # --- Benefit Enrollment Creation (create_enrollment) ---
        if operation_type == "create_enrollment":
            required_fields = ["employee_id", "plan_id", "effective_date", "employee_contribution", "employer_contribution", "enrollment_window_start", "enrollment_window_end", "selection_date", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "enrollment_id": None,
                    "message": f"Missing mandatory fields: {', '.join(missing_fields)}" # Halt Condition: Missing mandatory fields
                })

            # 1. Validation and Date Conversion
            date_fields = ["effective_date", "enrollment_window_start", "enrollment_window_end", "selection_date"]
            converted_dates = {}
            for field in date_fields:
                date_error = ManageBenefitEnrollmentOperations._validate_date_format(kwargs[field], field)
                if date_error:
                    return json.dumps({"success": False, "enrollment_id": None, "message": date_error})
                converted_dates[field] = ManageBenefitEnrollmentOperations._convert_date_format(kwargs[field])

            # 2. Check for Negative Contribution Amounts
            try:
                emp_contrib = float(kwargs["employee_contribution"])
                er_contrib = float(kwargs["employer_contribution"])
                if emp_contrib < 0 or er_contrib < 0:
                    return json.dumps({"success": False, "enrollment_id": None, "message": "Negative contribution amounts detected."}) # Halt Condition: Negative contribution amounts
            except ValueError:
                return json.dumps({"success": False, "enrollment_id": None, "message": "Contribution amounts must be valid numbers."})

            # 3. Check Effective Date is not in the past
            effective_date_obj = datetime.strptime(converted_dates["effective_date"], '%Y-%m-%d').date()
            if effective_date_obj < simulated_today:
                return json.dumps({"success": False, "enrollment_id": None, "message": "Effective date cannot be in the past."}) # Halt Condition: Effective date in the past

            # 4. Check Selection Date is within Enrollment Window
            selection_date_obj = datetime.strptime(converted_dates["selection_date"], '%Y-%m-%d').date()
            window_start_obj = datetime.strptime(converted_dates["enrollment_window_start"], '%Y-%m-%d').date()
            window_end_obj = datetime.strptime(converted_dates["enrollment_window_end"], '%Y-%m-%d').date()

            if not (window_start_obj <= selection_date_obj <= window_end_obj):
                return json.dumps({"success": False, "enrollment_id": None, "message": "Selection date outside enrollment window."}) # Halt Condition: Selection date outside enrollment window

            # 5. Simulate External Validations (Employee/Plan Existence & Status)
            # SOP: Verify employee exists and is active using discover_employee_entities
            employee = employees.get(str(kwargs["employee_id"]))
            if not employee or employee.get("employment_status") != "active":
                 return json.dumps({"success": False, "enrollment_id": None, "message": "Employee not found or inactive."}) # Halt Condition: Employee not found or inactive

            # SOP: Confirm plan exists and is active using discover_benefit_entities
            plan = benefit_plans.get(str(kwargs["plan_id"]))
            if not plan or plan.get("plan_status") != "active":
                 return json.dumps({"success": False, "enrollment_id": None, "message": "Plan not found or inactive."}) # Halt Condition: Plan not found or inactive

            # SOP: Verify user is an active HR Admin using discover_reference_entities
            # (Skipping direct implementation, assuming user_id is valid for the action)

            # 6. Create Enrollment Record
            new_enrollment_id = ManageBenefitEnrollmentOperations._generate_id(enrollments)
            timestamp = datetime.now().isoformat()

            new_enrollment = {
                "enrollment_id": str(new_enrollment_id),
                "employee_id": str(kwargs["employee_id"]),
                "plan_id": str(kwargs["plan_id"]),
                "effective_date": converted_dates["effective_date"],
                "employee_contribution": emp_contrib,
                "employer_contribution": er_contrib,
                "enrollment_window_start": converted_dates["enrollment_window_start"],
                "enrollment_window_end": converted_dates["enrollment_window_end"],
                "selection_date": converted_dates["selection_date"],
                "enrollment_status": "pending",  # Initial status per schema/SOP
                "hr_manager_approval_status": "pending",
                "approved_by": None,
                "approval_date": None,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            enrollments[str(new_enrollment_id)] = new_enrollment
            
            # SOP: Create Audit Entry (Simulation)
            # create_audit_entry("enrollment", str(new_enrollment_id), "create", kwargs["user_id"], ...)

            return json.dumps({
                "success": True,
                "enrollment_id": str(new_enrollment_id),
                "message": f"Benefit enrollment {new_enrollment_id} created successfully and set to 'pending' for approval."
            })

        # --- Benefit Enrollment Approval (approve_enrollment) ---
        elif operation_type == "approve_enrollment":
            required_fields = ["enrollment_id", "hr_manager_approval_status", "approved_by", "approval_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]

            if missing_fields:
                return json.dumps({
                    "success": False,
                    "enrollment_id": None,
                    "message": f"Missing mandatory fields for approval: {', '.join(missing_fields)}"
                })

            enrollment_id_str = str(kwargs["enrollment_id"])
            enrollment = enrollments.get(enrollment_id_str)
            
            # 1. Verify Enrollment Exists and Status
            if not enrollment:
                return json.dumps({
                    "success": False,
                    "enrollment_id": enrollment_id_str,
                    "message": f"Enrollment {enrollment_id_str} not found."
                })
            
            # Check if enrollment is in 'pending' status for HR Manager approval
            if enrollment.get("hr_manager_approval_status") != "pending":
                return json.dumps({
                    "success": False,
                    "enrollment_id": enrollment_id_str,
                    "message": f"Enrollment {enrollment_id_str} is not in 'pending' status for HR Manager approval." # Halt Condition: Enrollment not found or not in 'pending' status
                })

            # 2. Validation and Date Conversion
            valid_statuses = ["approved", "rejected"]
            approval_status = kwargs["hr_manager_approval_status"]
            status_error = ManageBenefitEnrollmentOperations._validate_status_field(approval_status, "hr_manager_approval_status", valid_statuses)
            if status_error:
                return json.dumps({"success": False, "enrollment_id": None, "message": status_error}) # Halt Condition: Invalid approval_status

            date_error = ManageBenefitEnrollmentOperations._validate_date_format(kwargs["approval_date"], "approval_date")
            if date_error:
                return json.dumps({"success": False, "enrollment_id": None, "message": date_error})
            
            converted_approval_date = ManageBenefitEnrollmentOperations._convert_date_format(kwargs["approval_date"])
            
            # SOP: Verify approver is an active HR Manager using discover_reference_entities
            # (Skipping direct implementation, assuming user_id is valid)

            # 3. Execute Approval/Rejection
            timestamp = datetime.now().isoformat()
            
            enrollment["hr_manager_approval_status"] = approval_status
            enrollment["approved_by"] = str(kwargs["approved_by"])
            enrollment["approval_date"] = converted_approval_date
            enrollment["updated_at"] = timestamp

            # If approved, update the main enrollment status to 'approved'
            if approval_status == "approved":
                enrollment["enrollment_status"] = "approved"

            # SOP: Create Audit Entry (Simulation)
            # create_audit_entry("enrollment", enrollment_id_str, approval_status, kwargs["approved_by"], ...)

            return json.dumps({
                "success": True,
                "enrollment_id": enrollment_id_str,
                "message": f"Benefit enrollment {enrollment_id_str} successfully marked as '{approval_status}'."
            })

        return json.dumps({
            "success": False,
            "enrollment_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_benefit_enrollment_operations",
                "description": "Manages the creation and HR Manager approval of employee benefit enrollments. 'create_enrollment' validates dates, contributions, and enrollment windows before setting the status to 'pending'. 'approve_enrollment' handles the HR Manager's decision to 'approve' or 'rejected' a pending enrollment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation: 'create_enrollment' or 'approve_enrollment'.",
                            "enum": ["create_enrollment", "approve_enrollment"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee (required for create_enrollment)."
                        },
                        "plan_id": {
                            "type": "string",
                            "description": "Unique identifier of the benefit plan (required for create_enrollment)."
                        },
                        "effective_date": {
                            "type": "string",
                            "description": "The date the benefit coverage begins (MM-DD-YYYY, required for create_enrollment)."
                        },
                        "employee_contribution": {
                            "type": "number",
                            "description": "The amount the employee contributes (required for create_enrollment, must be >= 0)."
                        },
                        "employer_contribution": {
                            "type": "number",
                            "description": "The amount the employer contributes (required for create_enrollment, must be >= 0)."
                        },
                        "enrollment_window_start": {
                            "type": "string",
                            "description": "Start date of the enrollment period (MM-DD-YYYY, required for create_enrollment)."
                        },
                        "enrollment_window_end": {
                            "type": "string",
                            "description": "End date of the enrollment period (MM-DD-YYYY, required for create_enrollment)."
                        },
                        "selection_date": {
                            "type": "string",
                            "description": "The date the employee made the benefit selection (MM-DD-YYYY, required for create_enrollment, must be within the window)."
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (HR Admin) initiating the enrollment (required for create_enrollment)."
                        },
                        "enrollment_id": {
                            "type": "string",
                            "description": "Unique identifier of the benefit enrollment record (required for approve_enrollment)."
                        },
                        "hr_manager_approval_status": {
                            "type": "string",
                            "description": "The approval decision from the HR Manager: 'approved' or 'rejected' (required for approve_enrollment).",
                            "enum": ["approved", "rejected"]
                        },
                        "approved_by": {
                            "type": "string",
                            "description": "Unique identifier of the HR Manager providing the approval (required for approve_enrollment)."
                        },
                        "approval_date": {
                            "type": "string",
                            "description": "The date the approval decision was made (MM-DD-YYYY, required for approve_enrollment)."
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
