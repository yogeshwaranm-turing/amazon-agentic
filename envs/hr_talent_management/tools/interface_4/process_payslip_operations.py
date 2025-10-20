import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ProcessPayslipOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, employee_id: str = None, cycle_id: str = None,
               gross_pay: float = None, base_salary: float = None, total_deductions: float = None,
               net_pay: float = None, user_id: str = None, bonus_earned: float = None,
               incentives_earned: float = None, reimbursements: float = None,
               proration_status: str = None, payslip_id: str = None, released_date: str = None,
               amount: float = None, payment_date: str = None, payment_method: str = None) -> str:
        """
        Manage payslip operations including generation, release, and payment processing.
        
        Operations:
        - create_payslip: Generate payslip for employee (requires employee_id, cycle_id, gross_pay, base_salary, total_deductions, net_pay, user_id)
        - update_payslip_status: Release payslip to employee (requires payslip_id, user_id, released_date)
        - create_payment: Process payment for released payslip (requires employee_id, cycle_id, payslip_id, amount, payment_date, payment_method, user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
            
        def is_valid_amount(amount: float) -> bool:
            """Check if amount is valid (non-negative)"""
            return amount is not None and amount >= 0
            
        def is_future_date(date_str: str) -> bool:
            """Check if date is in the future (simplified for demo)"""
            # For demo purposes, assume current date is 2025-01-15
            current_date = "2025-01-15"
            return date_str > current_date
        
        if operation_type not in ["create_payslip", "update_payslip_status", "create_payment"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_payslip', 'update_payslip_status', or 'create_payment'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payslip operations"
            })
        
        payslips = data.get("payslips", {})
        payments = data.get("payments", {})
        payroll_cycles = data.get("payroll_cycles", {})
        payroll_inputs = data.get("payroll_inputs", {})
        employees = data.get("employees", {})
        users = data.get("users", {})
        audit_trails = data.get("audit_trails", {})
        
        if operation_type == "create_payslip":
            # Validate mandatory fields
            if not all([employee_id, cycle_id, gross_pay, base_salary, total_deductions, net_pay, user_id]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - employee_id, cycle_id, gross_pay, base_salary, total_deductions, net_pay, and user_id are required"
                })
            
            # Verify the user is an active HR Payroll Administrator, HR Manager, or HR Director
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user not found"
                })
            
            user = users[user_id]
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
            
            # Verify cycle exists
            if cycle_id not in payroll_cycles:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Cycle not found or not ready for payslip generation - cycle not found"
                })
            
            # Verify employee has approved payroll input for the cycle
            has_approved_input = False
            for input_record in payroll_inputs.values():
                if (input_record.get("employee_id") == employee_id and 
                    input_record.get("cycle_id") == cycle_id and 
                    input_record.get("input_status") == "submitted"):
                    has_approved_input = True
                    break
            
            if not has_approved_input:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Cycle not found or not ready for payslip generation - no approved payroll input found for employee in this cycle"
                })
            
            # Validate amounts (non-negative)
            if not all([is_valid_amount(gross_pay), is_valid_amount(base_salary), 
                       is_valid_amount(total_deductions), is_valid_amount(net_pay)]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Negative amounts detected - all amounts must be non-negative"
                })
            
            # Validate calculation: net_pay should equal gross_pay minus total_deductions
            calculated_net_pay = gross_pay - total_deductions
            if abs(net_pay - calculated_net_pay) > 0.01:  # Allow for small rounding differences
                return json.dumps({
                    "success": False,
                    "error": "Halt: Calculation validation failed (gross_pay or net_pay mismatch) - net_pay must equal gross_pay minus total_deductions"
                })
            
            # Validate optional amounts if provided
            if bonus_earned is not None and not is_valid_amount(bonus_earned):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Negative amounts detected - bonus_earned must be non-negative"
                })
            
            if incentives_earned is not None and not is_valid_amount(incentives_earned):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Negative amounts detected - incentives_earned must be non-negative"
                })
            
            if reimbursements is not None and not is_valid_amount(reimbursements):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Negative amounts detected - reimbursements must be non-negative"
                })
            
            # Validate proration status if provided
            if proration_status is not None:
                valid_proration_statuses = ["not_applicable", "applied", "none"]
                if proration_status not in valid_proration_statuses:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid proration_status - must be one of: {', '.join(valid_proration_statuses)}"
                    })
            
            # Generate new payslip ID
            new_payslip_id = generate_id(payslips)
            
            # Create payslip
            new_payslip = {
                "payslip_id": new_payslip_id,
                "employee_id": employee_id,
                "cycle_id": cycle_id,
                "gross_pay": gross_pay,
                "base_salary": base_salary,
                "bonus_earned": bonus_earned,
                "incentives_earned": incentives_earned,
                "reimbursements": reimbursements,
                "total_deductions": total_deductions,
                "net_pay": net_pay,
                "proration_status": proration_status or "not_applicable",
                "payslip_status": "generated",
                "released_date": None,
                "created_at": "2025-10-01T12:00:00"
            }
            
            payslips[new_payslip_id] = new_payslip
            
            # Create audit entry for payslip generation
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": new_payslip_id,
                "reference_type": "payroll",
                "action": "create",
                "user_id": user_id,
                "field_name": None,
                "old_value": None,
                "new_value": json.dumps(new_payslip),
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "create_payslip",
                "payslip_id": new_payslip_id,
                "message": f"Payslip {new_payslip_id} generated successfully",
                "payslip_data": new_payslip
            })
        
        elif operation_type == "update_payslip_status":
            # Validate mandatory fields for release
            if not all([payslip_id, user_id, released_date]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - payslip_id, user_id, and released_date are required"
                })
            
            # Verify the user is an active HR Payroll Administrator, HR Manager, or HR Director
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user not found"
                })
            
            user = users[user_id]
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
            
            # Verify payslip exists and is in appropriate status for release
            if payslip_id not in payslips:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payslip not found or not in appropriate status for release - payslip not found"
                })
            
            payslip = payslips[payslip_id]
            if payslip.get("payslip_status") not in ["generated", "verified"]:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payslip not found or not in appropriate status for release - payslip is not in generated or verified status"
                })
            
            # Check if release date is in the future
            if is_future_date(released_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Release date in the future - release date cannot be in the future"
                })
            
            # Update payslip status to released
            updated_payslip = payslip.copy()
            updated_payslip.update({
                "payslip_status": "released",
                "released_date": released_date
            })
            
            payslips[payslip_id] = updated_payslip
            
            # Create audit entry for payslip release
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": payslip_id,
                "reference_type": "payroll",
                "action": "update",
                "user_id": user_id,
                "field_name": "payslip_status",
                "old_value": payslip.get("payslip_status"),
                "new_value": "released",
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "update_payslip_status",
                "payslip_id": payslip_id,
                "message": f"Payslip {payslip_id} released successfully",
                "payslip_data": updated_payslip
            })
        
        elif operation_type == "create_payment":
            # Validate mandatory fields for payment
            if not all([employee_id, cycle_id, payslip_id, amount, payment_date, payment_method, user_id]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - employee_id, cycle_id, payslip_id, amount, payment_date, payment_method, and user_id are required"
                })
            
            # Verify the user is an active finance manager
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user not found"
                })
            
            user = users[user_id]
            if user.get("role") != "finance_manager":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user must be a Finance Manager"
                })
            
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing or invalid inputs - user must be active"
                })
            
            # Verify payslip exists and is released
            if payslip_id not in payslips:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payslip not found or not in 'released' status - payslip not found"
                })
            
            payslip = payslips[payslip_id]
            if payslip.get("payslip_status") != "released":
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payslip not found or not in 'released' status - payslip is not released"
                })
            
            # Verify amount matches payslip net_pay
            if amount != payslip.get("net_pay"):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Amount mismatch with payslip net_pay - payment amount must match payslip net pay"
                })
            
            # Validate payment method
            valid_payment_methods = ["bank_transfer", "check", "cash"]
            if payment_method not in valid_payment_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid payment_method - must be one of: {', '.join(valid_payment_methods)}"
                })
            
            # Check if payment date is in the future
            if is_future_date(payment_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payment date in the future - payment date cannot be in the future"
                })
            
            # Verify employee bank details (simplified check)
            if employee_id not in employees:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Employee bank details invalid - employee not found"
                })
            
            employee = employees[employee_id]
            if not employee.get("bank_account_number") or not employee.get("routing_number"):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Employee bank details invalid - missing bank account or routing number"
                })
            
            # Generate new payment ID
            new_payment_id = generate_id(payments)
            
            # Create payment
            new_payment = {
                "payment_id": new_payment_id,
                "employee_id": employee_id,
                "cycle_id": cycle_id,
                "payslip_id": payslip_id,
                "amount": amount,
                "payment_date": payment_date,
                "payment_method": payment_method,
                "payment_status": "pending",
                "transaction_id": None,
                "bank_confirmation_date": None,
                "created_at": "2025-10-01T12:00:00"
            }
            
            payments[new_payment_id] = new_payment
            
            # Create audit entry for payment processing
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": new_payment_id,
                "reference_type": "payroll",
                "action": "create",
                "user_id": user_id,
                "field_name": None,
                "old_value": None,
                "new_value": json.dumps(new_payment),
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "create_payment",
                "payment_id": new_payment_id,
                "message": f"Payment {new_payment_id} processed successfully",
                "payment_data": new_payment
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_payslip_operations",
                "description": "Manage payslip operations in the HR talent management system. This tool handles payslip generation with comprehensive calculations, payslip release to employees, and payment processing. For generation, validates employee and cycle data, ensures approved payroll inputs exist, and validates all financial calculations. For release, verifies payslip status and release dates. For payment processing, validates finance manager authorization, payslip status, amount matching, and employee bank details. Essential for complete payroll processing workflow with proper validation and audit trails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_payslip' to generate payslip, 'update_payslip_status' to release payslip, 'create_payment' to process payment",
                            "enum": ["create_payslip", "update_payslip_status", "create_payment"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Employee identifier (required for create_payslip and create_payment, must exist and be active)"
                        },
                        "cycle_id": {
                            "type": "string",
                            "description": "Payroll cycle identifier (required for create_payslip and create_payment, must exist)"
                        },
                        "gross_pay": {
                            "type": "number",
                            "description": "Total gross pay amount (required for create_payslip, must be non-negative)"
                        },
                        "base_salary": {
                            "type": "number",
                            "description": "Base salary amount (required for create_payslip, must be non-negative)"
                        },
                        "total_deductions": {
                            "type": "number",
                            "description": "Total deductions amount (required for create_payslip, must be non-negative)"
                        },
                        "net_pay": {
                            "type": "number",
                            "description": "Net pay amount (required for create_payslip, must be non-negative)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User ID (required for all operations, must be active hr_payroll_administrator/hr_manager/hr_admin for create_payslip/update_payslip_status, finance_manager for create_payment)"
                        },
                        "bonus_earned": {
                            "type": "number",
                            "description": "Bonus amount earned (optional for create_payslip, must be non-negative)"
                        },
                        "incentives_earned": {
                            "type": "number",
                            "description": "Incentives amount earned (optional for create_payslip, must be non-negative)"
                        },
                        "reimbursements": {
                            "type": "number",
                            "description": "Reimbursements amount (optional for create_payslip, must be non-negative)"
                        },
                        "proration_status": {
                            "type": "string",
                            "description": "Proration status (optional for create_payslip)",
                            "enum": ["not_applicable", "applied", "none"]
                        },
                        "payslip_id": {
                            "type": "string",
                            "description": "Payslip identifier (required for update_payslip_status and create_payment, must exist)"
                        },
                        "released_date": {
                            "type": "string",
                            "description": "Date payslip was released in YYYY-MM-DD format (required for update_payslip_status, cannot be future date)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Payment amount (required for create_payment, must match payslip net_pay)"
                        },
                        "payment_date": {
                            "type": "string",
                            "description": "Payment date in YYYY-MM-DD format (required for create_payment, cannot be future date)"
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "Payment method (required for create_payment)",
                            "enum": ["bank_transfer", "check", "cash"]
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
