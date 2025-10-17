import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePayrollInputOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, employee_id: str = None, cycle_id: str = None, 
               hours_worked: float = None, overtime_hours: float = None, requesting_user_id: str = None,
               input_id: str = None, manager_approval_status: str = None, manager_approved_by: str = None,
               manager_approval_date: str = None) -> str:
        """
        Manage payroll input operations including creation and approval.
        
        Operations:
        - create_input: Create payroll input data for an employee (requires employee_id, cycle_id, requesting_user_id)
        - approve_input: Approve payroll input data (requires input_id, manager_approval_status, manager_approved_by, manager_approval_date)
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
            
        def is_valid_hours(hours: float) -> bool:
            """Check if hours are valid (positive and <= 24 per day)"""
            return hours is not None and hours >= 0 and hours <= 24
            
        def is_after_cutoff_date(cycle_id: str, payroll_cycles: Dict[str, Any]) -> bool:
            """Check if current date is after cutoff date"""
            if cycle_id not in payroll_cycles:
                return False
            cycle = payroll_cycles[cycle_id]
            cutoff_date = cycle.get("cutoff_date", "")
            # For demo purposes, assume current date is 2025-01-10
            current_date = "2025-01-10"
            return current_date > cutoff_date
        
        if operation_type not in ["create_input", "approve_input"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_input' or 'approve_input'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll input operations"
            })
        
        payroll_inputs = data.get("payroll_inputs", {})
        payroll_cycles = data.get("payroll_cycles", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        if operation_type == "create_input":
            # Validate mandatory fields
            if not all([employee_id, cycle_id, requesting_user_id]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - employee_id, cycle_id, and requesting_user_id are required"
                })
            
            # Verify the user is an active HR Payroll Administrator, HR Manager, or HR Director
            if requesting_user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user not found"
                })
            
            user = users[requesting_user_id]
            user_role = user.get("role")
            valid_roles = ["hr_payroll_administrator", "hr_manager", "hr_admin"]
            
            if user_role not in valid_roles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user must be an HR Payroll Administrator, HR Manager, or HR Admin"
                })
            
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user must be active"
                })
            
            # Verify employee exists and is active
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Employee not found or inactive - employee not found"
                })
            
            employee = employees[employee_id]
            if employee.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Employee not found or inactive - employee is not active"
                })
            
            # Verify cycle exists and is open for input collection
            if cycle_id not in payroll_cycles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Cycle not found or not in 'open' status - cycle not found"
                })
            
            cycle = payroll_cycles[cycle_id]
            if cycle.get("status") != "open":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Cycle not found or not in 'open' status - cycle is not open"
                })
            
            # Check if input submitted after cutoff date
            if is_after_cutoff_date(cycle_id, payroll_cycles):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Input submitted after cutoff date"
                })
            
            # Validate hours if provided
            if hours_worked is not None and not is_valid_hours(hours_worked):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid hours (negative or > 24 per day) - hours_worked is invalid"
                })
            
            if overtime_hours is not None and not is_valid_hours(overtime_hours):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid hours (negative or > 24 per day) - overtime_hours is invalid"
                })
            
            # Generate new input ID
            new_input_id = generate_id(payroll_inputs)
            
            # Create payroll input
            new_input = {
                "input_id": new_input_id,
                "employee_id": employee_id,
                "cycle_id": cycle_id,
                "hours_worked": hours_worked,
                "overtime_hours": overtime_hours,
                "manager_approval_status": "pending",
                "manager_approved_by": None,
                "manager_approval_date": None,
                "input_status": "draft",
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            payroll_inputs[new_input_id] = new_input
            
            # Create audit entry for input creation
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": new_input_id,
                "reference_type": "payroll",
                "action": "create",
                "user_id": requesting_user_id,
                "field_name": None,
                "old_value": None,
                "new_value": json.dumps(new_input),
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "create_input",
                "input_id": new_input_id,
                "message": f"Payroll input {new_input_id} created successfully",
                "input_data": new_input
            })
        
        elif operation_type == "approve_input":
            # Validate mandatory fields for approval
            if not all([input_id, manager_approval_status, manager_approved_by, manager_approval_date]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - input_id, manager_approval_status, manager_approved_by, and manager_approval_date are required"
                })
            
            # Verify input exists and is in 'draft' status
            if input_id not in payroll_inputs:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Input not found or not in 'draft' status - input not found"
                })
            
            input_record = payroll_inputs[input_id]
            if input_record.get("input_status") != "draft":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Input not found or not in 'draft' status - input is not in draft status"
                })
            
            # Verify approver exists and is active
            if manager_approved_by not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized (not employee's manager) - approver not found"
                })
            
            approver = users[manager_approved_by]
            if approver.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized (not employee's manager) - approver is not active"
                })
            
            # Verify approver is the employee's manager
            employee_id = input_record.get("employee_id")
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized (not employee's manager) - employee not found"
                })
            
            employee = employees[employee_id]
            if employee.get("manager_id") != manager_approved_by:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Approver not authorized (not employee's manager) - approver is not the employee's manager"
                })
            
            # Validate approval status
            valid_approval_statuses = ["approved", "rejected"]
            if manager_approval_status not in valid_approval_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid approval_status - must be one of: {', '.join(valid_approval_statuses)}"
                })
            
            # Update payroll input with approval details
            updated_input = input_record.copy()
            updated_input.update({
                "manager_approval_status": manager_approval_status,
                "manager_approved_by": manager_approved_by,
                "manager_approval_date": manager_approval_date,
                "input_status": "submitted" if manager_approval_status == "approved" else "rejected",
                "updated_at": "2025-10-01T12:00:00"
            })
            
            payroll_inputs[input_id] = updated_input
            
            # Create audit entry for approval
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": input_id,
                "reference_type": "payroll",
                "action": "approve" if manager_approval_status == "approved" else "reject",
                "user_id": manager_approved_by,
                "field_name": "manager_approval_status",
                "old_value": "pending",
                "new_value": manager_approval_status,
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "approve_input",
                "input_id": input_id,
                "message": f"Payroll input {input_id} {manager_approval_status} successfully",
                "input_data": updated_input
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payroll_input_operations",
                "description": "Manage payroll input operations in the HR talent management system. This tool handles the creation of payroll input data for employees and manager approval of payroll inputs. For creation, validates employee and cycle status, ensures proper authorization, and validates hours worked. For approval, verifies manager authorization and updates input status. Essential for accurate payroll processing and maintaining proper approval workflows.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_input' to create payroll input data, 'approve_input' to approve/reject payroll input",
                            "enum": ["create_input", "approve_input"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Employee identifier (required for create_input, must exist and be active)"
                        },
                        "cycle_id": {
                            "type": "string",
                            "description": "Payroll cycle identifier (required for create_input, must exist and be open)"
                        },
                        "hours_worked": {
                            "type": "number",
                            "description": "Hours worked by employee (optional for create_input, must be >= 0 and <= 24)"
                        },
                        "overtime_hours": {
                            "type": "number",
                            "description": "Overtime hours worked by employee (optional for create_input, must be >= 0 and <= 24)"
                        },
                        "requesting_user_id": {
                            "type": "string",
                            "description": "User ID creating the input (required for create_input, must be active hr_payroll_administrator, hr_manager, or hr_admin)"
                        },
                        "input_id": {
                            "type": "string",
                            "description": "Payroll input identifier (required for approve_input, must exist and be in draft status)"
                        },
                        "manager_approval_status": {
                            "type": "string",
                            "description": "Manager approval status (required for approve_input)",
                            "enum": ["approved", "rejected"]
                        },
                        "manager_approved_by": {
                            "type": "string",
                            "description": "User ID of the manager approving the input (required for approve_input, must be employee's manager)"
                        },
                        "manager_approval_date": {
                            "type": "string",
                            "description": "Date of manager approval in YYYY-MM-DD format (required for approve_input)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
