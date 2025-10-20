import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AdministerPaymentOperations(Tool):
    
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> int:
        """Utility to generate a new sequential ID."""
        if not table:
            return 1001
        return max(int(k) for k in table.keys()) + 1

    @staticmethod
    def _validate_date_format(date_str: str, field_name: str) -> Optional[str]:
        """Validates date format is MM-DD-YYYY."""
        if date_str:
            date_pattern = r'^\d{2}-\d{2}-\d{4}$'
            if not re.match(date_pattern, date_str):
                return f"Invalid {field_name} format. Must be MM-DD-YYYY"
        return None

    @staticmethod
    def _convert_date_format(date_str: str) -> str:
        """Convert MM-DD-YYYY to YYYY-MM-DD for internal storage."""
        if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
            month, day, year = date_str.split('-')
            return f"{year}-{month}-{day}"
        return date_str

    @staticmethod
    def _validate_status_field(status_value: str, field_name: str, valid_statuses: list) -> Optional[str]:
        """Validate status field against allowed values."""
        if status_value and status_value not in valid_statuses:
            return f"Invalid {field_name}. Must be one of: {', '.join(valid_statuses)}"
        return None

    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage employee payment operations including processing new payments and updating their status.
        """
        
        # Validate operation_type
        valid_operations = ["create_payment", "update_payment_status"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "payment_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })

        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "payment_id": None,
                "message": "Invalid data format for payment operations"
            })
        
        payments = data.get("payments", {})
        payslips = data.get("payslips", {})
        
        # --- Create Payment (Payment Processing SOP) ---
        if operation_type == "create_payment":
            required_fields = ["employee_id", "cycle_id", "payslip_id", "amount", "payment_date", "payment_method", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Missing required fields for payment processing: {', '.join(missing_fields)}"
                })

            # Validate date format for payment_date
            date_error = ManagePaymentOperations._validate_date_format(kwargs["payment_date"], "payment_date")
            if date_error:
                return json.dumps({"success": False, "payment_id": None, "message": date_error})
            
            # Basic validation for amount (must be convertible to float)
            try:
                amount_float = float(kwargs["amount"])
                if amount_float <= 0:
                     return json.dumps({"success": False, "payment_id": None, "message": "Amount must be greater than zero"})
            except ValueError:
                 return json.dumps({"success": False, "payment_id": None, "message": "Amount must be a valid number"})

            # Check for amount mismatch against payslip net_pay (SOP requirement)
            payslip_id_str = str(kwargs["payslip_id"])
            payslip = payslips.get(payslip_id_str)
            
            if payslip:
                # IMPORTANT: This check aligns with the SOP halt condition "Amount mismatch with payslip net_pay"
                net_pay_float = payslip.get("net_pay", 0.0) 
                if abs(amount_float - net_pay_float) > 0.001: # Check for floating point equality
                    return json.dumps({
                        "success": False,
                        "payment_id": None,
                        "message": f"Amount mismatch with payslip net_pay. Provided amount: {amount_float}, Payslip net_pay: {net_pay_float}"
                    })

            # Validate payment method against schema (bank_transfer, check, cash)
            valid_methods = ["bank_transfer", "check", "cash"]
            if kwargs["payment_method"] not in valid_methods:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Invalid payment_method. Must be one of: {', '.join(valid_methods)}"
                })
            
            # Check for existing payment for this payslip (prevents duplicates)
            for payment in payments.values():
                if payment.get("payslip_id") == payslip_id_str:
                    return json.dumps({
                        "success": False,
                        "payment_id": None,
                        "message": f"Payment already exists for payslip {kwargs['payslip_id']}"
                    })

            # Process Payment
            new_payment_id = ManagePaymentOperations._generate_id(payments)
            timestamp = "2025-10-01T12:00:00"

            new_payment = {
                "payment_id": str(new_payment_id),
                "employee_id": str(kwargs["employee_id"]),
                "cycle_id": str(kwargs["cycle_id"]),
                "payslip_id": payslip_id_str,
                "amount": amount_float,
                "payment_date": ManagePaymentOperations._convert_date_format(kwargs["payment_date"]),
                "payment_method": kwargs["payment_method"],
                "payment_status": "pending",  # Initial status set to 'pending'
                "transaction_id": None,
                "bank_confirmation_date": None,
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            payments[str(new_payment_id)] = new_payment
            
            return json.dumps({
                "success": True,
                "payment_id": str(new_payment_id),
                "message": f"Payment {new_payment_id} processed successfully and set to 'pending' status for employee {kwargs['employee_id']}"
            })

        # --- Update Payment Status (Payment Status Update SOP) ---
        elif operation_type == "update_payment_status":
            required_fields = ["payment_id", "payment_status", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]

            if missing_fields:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Missing required fields for status update: {', '.join(missing_fields)}"
                })

            # Validate payment exists
            payment_id_str = str(kwargs["payment_id"])
            if payment_id_str not in payments:
                return json.dumps({
                    "success": False,
                    "payment_id": None,
                    "message": f"Payment {payment_id_str} not found"
                })

            # Validate payment status transition against schema (pending, processed, failed, reversed)
            valid_statuses = ["pending", "processed", "failed", "reversed"]
            status_error = ManagePaymentOperations._validate_status_field(kwargs["payment_status"], "payment_status", valid_statuses)
            if status_error:
                return json.dumps({"success": False, "payment_id": None, "message": status_error})

            # Validate bank_confirmation_date format if provided
            if "bank_confirmation_date" in kwargs and kwargs["bank_confirmation_date"] is not None:
                date_error = ManagePaymentOperations._validate_date_format(kwargs["bank_confirmation_date"], "bank_confirmation_date")
                if date_error:
                    return json.dumps({"success": False, "payment_id": None, "message": date_error})
            
            # Execute Update
            payment = payments[payment_id_str]
            
            # Update fields
            payment["payment_status"] = kwargs["payment_status"]
            
            if "transaction_id" in kwargs and kwargs["transaction_id"] is not None:
                payment["transaction_id"] = kwargs["transaction_id"]
                
            if "bank_confirmation_date" in kwargs and kwargs["bank_confirmation_date"] is not None:
                payment["bank_confirmation_date"] = ManagePaymentOperations._convert_date_format(kwargs["bank_confirmation_date"])

            payment["updated_at"] = "2025-10-01T12:00:00"

            return json.dumps({
                "success": True,
                "payment_id": payment_id_str,
                "message": f"Payment {payment_id_str} status updated to '{kwargs['payment_status']}' successfully"
            })
            
        return json.dumps({
            "success": False,
            "payment_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_payment_operations",
                "description": "Manages core employee payment processing, including initiating new payments for released payslips and updating their status based on bank confirmation. The 'create_payment' operation validates payment details, ensures no duplicate payments exist for the payslip, and checks the amount against the payslip's net_pay before setting the initial status to 'pending'. The 'update_payment_status' operation records the final outcome (processed, failed, reversed) and optional transaction/confirmation details.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_payment' to process a new payment, 'update_payment_status' to modify an existing payment's status.",
                            "enum": ["create_payment", "update_payment_status"]
                        },
                        "employee_id": {
                            "type": "string",
                            "description": "Unique identifier of the employee (required for create_payment)."
                        },
                        "cycle_id": {
                            "type": "string",
                            "description": "The payroll cycle identifier (required for create_payment)."
                        },
                        "payslip_id": {
                            "type": "string",
                            "description": "The unique identifier of the payslip being paid (required for create_payment)."
                        },
                        "amount": {
                            "type": "number",
                            "description": "The net pay amount to be transferred (required for create_payment)."
                        },
                        "payment_date": {
                            "type": "string",
                            "description": "The date the payment is scheduled/processed in MM-DD-YYYY format (required for create_payment)."
                        },
                        "payment_method": {
                            "type": "string",
                            "description": "The method of transfer (must align with schema: 'bank_transfer', 'check', or 'cash') (required for create_payment).",
                            "enum": ["bank_transfer", "check", "cash"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the Finance Manager initiating the action (required for both operations)."
                        },
                        "payment_id": {
                            "type": "string",
                            "description": "Unique identifier of the payment record (required for update_payment_status)."
                        },
                        "payment_status": {
                            "type": "string",
                            "description": "The status of the payment (must align with schema: 'pending', 'processed', 'failed', or 'reversed') (required for update_payment_status).",
                            "enum": ["pending", "processed", "failed", "reversed"]
                        },
                        "transaction_id": {
                            "type": "string",
                            "description": "Optional: The bank-generated transaction ID (optional for update_payment_status)."
                        },
                        "bank_confirmation_date": {
                            "type": "string",
                            "description": "Optional: The date the bank confirmed the status, in MM-DD-YYYY format (optional for update_payment_status)."
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
