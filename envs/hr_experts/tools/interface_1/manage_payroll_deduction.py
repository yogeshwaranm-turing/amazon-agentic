import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePayrollDeduction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], action: str, deduction_data: Dict[str, Any] = None, deduction_id: str = None) -> str:
        """
        Create or update payroll deduction records.
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
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll deductions"
            })
        
        payroll_deductions = data.get("payroll_deductions", {})
        payroll_records = data.get("payroll_records", {})
        users = data.get("users", {})
        
        if action == "create":
            if not deduction_data:
                return json.dumps({
                    "success": False,
                    "error": "deduction_data is required for create action"
                })
            
            # Validate required fields
            required_fields = ["payroll_id", "deduction_type", "amount", "created_by"]
            missing_fields = [field for field in required_fields if field not in deduction_data]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid payroll deduction details: {', '.join(missing_fields)}"
                })
            
            # Authorization Check - Payroll Administrator or Finance Officer approval required
            payroll_admin_approval = deduction_data.get("payroll_administrator_approval", False)
            finance_officer_approval = deduction_data.get("finance_officer_approval", False)
            
            if not payroll_admin_approval and not finance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payroll Administrator or Finance Officer approval required"
                })
            
            # Validate that payroll record exists in the system
            payroll_id = str(deduction_data["payroll_id"])
            if payroll_id not in payroll_records:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll record {payroll_id} not found"
                })
            
            # Validate that creator exists in the user system
            created_by = str(deduction_data["created_by"])
            if created_by not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Creator {created_by} not found in user system"
                })
            
            # Validate deduction_type enum
            valid_types = ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
            if deduction_data["deduction_type"] not in valid_types:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid deduction_type. Must be one of: {', '.join(valid_types)}"
                })
            
            # Validate amount is positive monetary value
            try:
                amount = float(deduction_data["amount"])
                if amount <= 0:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Deduction amount must be positive monetary value"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid amount format - must be positive monetary value"
                })
            
            # Validate only allowed fields are present
            allowed_fields = ["payroll_id", "deduction_type", "amount", "created_by", 
                            "payroll_administrator_approval", "finance_officer_approval"]
            invalid_fields = [field for field in deduction_data.keys() if field not in allowed_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll deduction creation: {', '.join(invalid_fields)}"
                })
            
            # Generate new deduction ID
            new_deduction_id = generate_id(payroll_deductions)
            
            # Create new deduction record
            new_deduction = {
                "deduction_id": str(new_deduction_id),
                "payroll_id": payroll_id,
                "deduction_type": deduction_data["deduction_type"],
                "amount": deduction_data["amount"],
                "created_by": created_by,
                "created_at": "2025-10-01T12:00:00"
            }
            
            payroll_deductions[str(new_deduction_id)] = new_deduction
            
            return json.dumps({
                "success": True,
                "action": "create",
                "deduction_id": str(new_deduction_id),
                "message": f"Payroll deduction {new_deduction_id} created successfully",
                "deduction_data": new_deduction
            })
        
        elif action == "update":
            if not deduction_id:
                return json.dumps({
                    "success": False,
                    "error": "deduction_id is required for update action"
                })
            
            # Validate that payroll deduction record exists in the system
            if deduction_id not in payroll_deductions:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Payroll deduction {deduction_id} not found"
                })
            
            if not deduction_data:
                return json.dumps({
                    "success": False,
                    "error": "deduction_data is required for update action"
                })
            
            # Authorization Check - Payroll Administrator or Finance Officer approval required for corrections
            payroll_admin_approval = deduction_data.get("payroll_administrator_approval", False)
            finance_officer_approval = deduction_data.get("finance_officer_approval", False)
            
            if not payroll_admin_approval and not finance_officer_approval:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Payroll Administrator or Finance Officer approval required for deduction correction"
                })
            
            # Validate that only modifiable fields are being updated (deduction_type, amount)
            # Check that core fields are not being modified (payroll_id, created_by, deduction_id)
            allowed_update_fields = ["deduction_type", "amount", "payroll_administrator_approval", "finance_officer_approval"]
            invalid_fields = [field for field in deduction_data.keys() if field not in allowed_update_fields]
            if invalid_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Invalid fields for payroll deduction update: {', '.join(invalid_fields)}. Cannot update payroll_id, created_by, or deduction_id."
                })
            
            # Validate deduction_type enum if provided
            if "deduction_type" in deduction_data:
                valid_types = ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
                if deduction_data["deduction_type"] not in valid_types:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Invalid deduction_type. Must be one of: {', '.join(valid_types)}"
                    })
            
            # Validate amount if provided
            if "amount" in deduction_data:
                try:
                    amount = float(deduction_data["amount"])
                    if amount <= 0:
                        return json.dumps({
                            "success": False,
                            "error": "Halt: Deduction amount must be positive monetary value"
                        })
                except (ValueError, TypeError):
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Invalid amount format - must be positive monetary value"
                    })
            
            # Update deduction record - Adjust payroll deduction record with correction details
            # Maintain original creation information (payroll_id, created_by, created_at)
            current_deduction = payroll_deductions[deduction_id]
            updated_deduction = current_deduction.copy()
            
            for key, value in deduction_data.items():
                if key not in ["payroll_administrator_approval", "finance_officer_approval"]:  # Skip approval from being stored
                    updated_deduction[key] = value
            
            # Update modification timestamp
            updated_deduction["updated_at"] = "2025-10-01T12:00:00"
            payroll_deductions[deduction_id] = updated_deduction
            
            return json.dumps({
                "success": True,
                "action": "update",
                "deduction_id": deduction_id,
                "message": f"Payroll deduction {deduction_id} updated successfully",
                "deduction_data": updated_deduction
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payroll_deduction",
                "description": "Create or update payroll deduction records in the HR payroll system. This tool manages payroll deductions with comprehensive validation, authorization controls, and data integrity checks. For creation, establishes new deductions with proper validation of payroll record existence, creator verification, deduction type compliance, and required Payroll Administrator or Finance Officer approval authorization. For updates (corrections), modifies existing deductions while maintaining data integrity and requiring proper authorization for corrections. Validates deduction amounts are positive monetary values, ensures payroll record exists, verifies creator exists in user system, and enforces approval requirements for all operations. Essential for payroll processing, deduction management, and maintaining accurate payroll records with proper authorization controls.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Action to perform: 'create' to establish new payroll deduction, 'update' to make deduction correction",
                            "enum": ["create", "update"]
                        },
                        "deduction_data": {
                            "type": "object",
                            "description": "Deduction data object. For create: requires payroll_id (must exist), deduction_type, amount (positive), created_by (must exist in users), and payroll_administrator_approval or finance_officer_approval. For update: fields to change with required approval authorization. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                "payroll_id": {
                                    "type": "string",
                                    "description": "Payroll record identifier (required for create, must exist in system, cannot be updated)"
                                },
                                "deduction_type": {
                                    "type": "string",
                                    "description": "Type of payroll deduction",
                                    "enum": ["tax", "insurance", "retirement", "garnishment", "equipment", "other"]
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Deduction amount (must be positive monetary value)"
                                },
                                "created_by": {
                                    "type": "string",
                                    "description": "User who created the deduction (required for create, must exist in user system, cannot be updated)"
                                },
                                "payroll_administrator_approval": {
                                    "type": "boolean",
                                    "description": "Payroll Administrator approval status (True/False, required for create and update operations)"
                                },
                                "finance_officer_approval": {
                                    "type": "boolean",
                                    "description": "Finance Officer approval status (True/False, required for create and update operations)"
                                }
                            }
                        },
                        "deduction_id": {
                            "type": "string",
                            "description": "Unique identifier of the payroll deduction (required for update action only)"
                        }
                    },
                    "required": ["action"]
                }
            }
        }