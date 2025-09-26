import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ManagePayrollRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, payroll_data: Dict[str, Any] = None, payroll_id: str = None) -> str:
        """
        Create or update payroll records.
        
        Actions:
        - create: Process payroll run (requires payroll_data with employee_id, pay_period_start, pay_period_end, hourly_rate, finance_officer_approval)
        - update: Payroll correction (requires payroll_id, payroll_data with correction details, and finance_officer_approval)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
            
        def is_valid_date_order(start_date: str, end_date: str) -> bool:
            """Check if start date is before end date - simplified for demo"""
            return start_date <= end_date
            
        def aggregate_approved_timesheet_hours(employee_id: str, pay_period_start: str, pay_period_end: str, timesheets: Dict[str, Any]) -> float:
            """Aggregate approved timesheet hours for the specified pay period"""
            total_hours = 0.0
            for timesheet in timesheets.values():
                if (timesheet.get("employee_id") == employee_id and 
                    timesheet.get("status") == "approved" and
                    pay_period_start <= timesheet.get("work_date", "") <= pay_period_end):
                    total_hours += float(timesheet.get("total_hours", 0))
            return total_hours
        
        if action not in ["create", "update"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action '{action}'. Must be 'create' or 'update'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll records"
            })
        
        payroll_records = data.get("payroll_records", {})
        employees = data.get("employees", {})
        employee_timesheets = data.get("employee_timesheets", {})
        
        if action == "create":
            if not payroll_data:
                return json.dumps({
                    "success": False,
                    "error": "payroll_data is required for create action"
                })
            
            # Validate that all required information is provided: employee, pay period dates
            required_fields = ["employee_id", "pay_period_start", "pay_period_end", "hourly_rate"]
            missing_fields = [field for field in required_fields if field not in payroll_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid payroll run details: {', '.join(missing_fields)}"
                })
            
            # Validate that employee exists in system
            employee_id = str(payroll_data["employee_id"])
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Employee {employee_id} not found"
                })
            
            # Authorization Check - Finance Officer approval required
            finance_officer_approval = payroll_data.get("finance_officer_approval", False)
            if not finance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Finance Officer approval required"
                })
            
            # Validate that pay period dates are logical (start date before end date)
            pay_period_start = payroll_data["pay_period_start"]
            pay_period_end = payroll_data["pay_period_end"]
            if not is_valid_date_order(pay_period_start, pay_period_end):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Pay period start date must be before end date"
                })
            
            # Validate that hourly rate is positive monetary value
            try:
                hourly_rate = float(payroll_data["hourly_rate"])
                if hourly_rate <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Hourly rate must be positive monetary value"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid hourly rate format - must be positive monetary value"
                })
            
            # Aggregate approved timesheet hours for the specified pay period
            hours_worked = aggregate_approved_timesheet_hours(employee_id, pay_period_start, pay_period_end, employee_timesheets)
            
            # Validate only allowed fields are present
            allowed_fields = ["employee_id", "pay_period_start", "pay_period_end", "hourly_rate", 
                            "payment_date", "approved_by", "finance_officer_approval"]
            invalid_fields = [field for field in payroll_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new payroll ID
            new_payroll_id = generate_id(payroll_records)
            
            # Create payroll record with required information: employee, pay period dates, hourly rate
            # Calculate hours worked from approved timesheets
            new_payroll = {
                "payroll_id": str(new_payroll_id),
                "employee_id": employee_id,
                "pay_period_start": pay_period_start,
                "pay_period_end": pay_period_end,
                "hours_worked": hours_worked,  # Calculated from approved timesheets
                "hourly_rate": hourly_rate,
                "payment_date": payroll_data.get("payment_date"),
                "status": payroll_data.get("status", "approved"),  # Default to approved if not specified, use provided status if given
                "approved_by": payroll_data.get("approved_by"),
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            payroll_records[str(new_payroll_id)] = new_payroll
            
            return json.dumps({
                "success": True,
                "action": "create",
                "payroll_id": str(new_payroll_id),
                "message": f"Payroll record {new_payroll_id} created successfully with {hours_worked} hours",
                "payroll_data": new_payroll
            })
        
        elif action == "update":
            if not payroll_id:
                return json.dumps({
                    "success": False,
                    "error": "payroll_id is required for update action"
                })
            
            # Validate that payroll record exists in the system
            if payroll_id not in payroll_records:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record {payroll_id} not found"
                })
            
            if not payroll_data:
                return json.dumps({
                    "success": False,
                    "error": "payroll_data is required for update action"
                })
            
            # Authorization Check - Finance Officer approval required for corrections
            finance_officer_approval = payroll_data.get("finance_officer_approval", False)
            if not finance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Finance Officer approval required"
                })
            
            # Validate only allowed fields for corrections
            allowed_update_fields = ["hours_worked", "hourly_rate", "payment_date", "status", "approved_by", "finance_officer_approval"]
            invalid_fields = [field for field in payroll_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll correction: {', '.join(invalid_fields)}. Cannot update employee_id or pay_period_dates."
                })
            
            # Validate that correction information is valid (hours worked and hourly rate must be positive)
            if "hours_worked" in payroll_data:
                try:
                    hours_worked = float(payroll_data["hours_worked"])
                    if hours_worked <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Hours worked must be positive"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid hours worked format - must be positive"
                    })
            
            if "hourly_rate" in payroll_data:
                try:
                    hourly_rate = float(payroll_data["hourly_rate"])
                    if hourly_rate <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Hourly rate must be positive"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid hourly rate format - must be positive"
                    })
            
            # Validate status enum if provided
            if "status" in payroll_data:
                valid_statuses = ["draft", "approved", "paid", "cancelled"]
                if payroll_data["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            
            # Adjust payroll record with correction details
            current_payroll = payroll_records[payroll_id]
            updated_payroll = current_payroll.copy()
            
            for key, value in payroll_data.items():
                if key != "finance_officer_approval":  # Skip approval from being stored
                    updated_payroll[key] = value
            
            # Update modification timestamp
            updated_payroll["updated_at"] = "2025-10-01T12:00:00"
            payroll_records[payroll_id] = updated_payroll
            
            return json.dumps({
                "success": True,
                "action": "update",
                "payroll_id": payroll_id,
                "message": f"Payroll record {payroll_id} corrected successfully",
                "payroll_data": updated_payroll
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payroll_record",
                "description": "Create or update payroll records in the HR payroll system. This tool manages payroll processing and corrections with comprehensive validation and authorization controls. For creation (payroll run), establishes new payroll records with proper validation of employee existence, pay period logic, and Finance Officer authorization. Automatically aggregates approved timesheet hours for the specified pay period and calculates total hours worked. For updates (payroll correction), modifies existing payroll records while maintaining data integrity and requiring Finance Officer approval for corrections. Validates hours worked and hourly rates are positive, ensures proper date ordering, and enforces field restrictions for corrections. Essential for payroll processing, employee compensation management, and maintaining accurate payroll records.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to process payroll run, 'update' to make payroll correction",
                            "enum": ["create", "update"]
                        },
                        "payroll_data": {
                            "type": "object",
                            "description": "Payroll data object. For create: requires employee_id, pay_period_start, pay_period_end, hourly_rate, finance_officer_approval. Optional: payment_date, approved_by. For update: requires finance_officer_approval plus correction fields. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "employee_id": {
                                    "type": "string",
                                    "description": "Employee identifier (required for create, must exist in system, cannot be updated)"
                                },
                                "pay_period_start": {
                                    "type": "string",
                                    "description": "Pay period start date in YYYY-MM-DD format (required for create, must be before end date, cannot be updated)"
                                },
                                "pay_period_end": {
                                    "type": "string",
                                    "description": "Pay period end date in YYYY-MM-DD format (required for create, must be after start date, cannot be updated)"
                                },
                                "hourly_rate": {
                                    "type": "number",
                                    "description": "Employee hourly rate (required for create, must be positive monetary value)"
                                },
                                "hours_worked": {
                                    "type": "number",
                                    "description": "Total hours worked (auto-calculated from timesheets for create, can be corrected in update, must be positive)"
                                },
                                "payment_date": {
                                    "type": "string",
                                    "description": "Payment date in YYYY-MM-DD format"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Payroll status (auto-set to approved for create if Finance Officer approved)",
                                    "enum": ["draft", "approved", "paid", "cancelled"]
                                },
                                "approved_by": {
                                    "type": "string",
                                    "description": "User who approved the payroll"
                                },
                                "finance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Finance Officer approval status (True/False, required for both create and update operations)"
                                }
                            }
                        },
                        "payroll_id": {
                            "type": "string",
                            "description": "Unique identifier of the payroll record (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }