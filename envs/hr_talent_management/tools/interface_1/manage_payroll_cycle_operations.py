import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManagePayrollCycleOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, cycle_start_date: str = None, cycle_end_date: str = None, frequency: str = None, cutoff_date: str = None, requesting_user_id: str = None) -> str:
        """
        Manage payroll cycle operations including creation, updates, and status changes.
        
        Operations:
        - create_cycle: Create a new payroll cycle (requires cycle_start_date, cycle_end_date, frequency, cutoff_date, requesting_user_id)
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
            
        def is_valid_date_order(start_date: str, end_date: str) -> bool:
            """Check if start date is before end date"""
            return start_date <= end_date
            
        def is_cutoff_within_range(cutoff_date: str, start_date: str, end_date: str) -> bool:
            """Check if cutoff date is within the cycle range"""
            return start_date <= cutoff_date <= end_date
            
        def check_overlapping_cycles(start_date: str, end_date: str, existing_cycles: Dict[str, Any]) -> bool:
            """Check if the new cycle overlaps with existing cycles"""
            for cycle in existing_cycles.values():
                existing_start = cycle.get("cycle_start_date", "")
                existing_end = cycle.get("cycle_end_date", "")
                # Check for overlap: new start <= existing end AND new end >= existing start
                if start_date <= existing_end and end_date >= existing_start:
                    return True
            return False
        
        if operation_type not in ["create_cycle"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be 'create_cycle'"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll cycle operations"
            })
        
        payroll_cycles = data.get("payroll_cycles", {})
        users = data.get("users", {})
        
        if operation_type == "create_cycle":
            if not requesting_user_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Missing mandatory fields - requesting_user_id is required"
                })
            
            # Validate that user is an active HR Payroll Administrator, HR Manager, or HR Director
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
            
            # Validate mandatory fields
            required_fields = {
                "cycle_start_date": cycle_start_date,
                "cycle_end_date": cycle_end_date,
                "frequency": frequency,
                "cutoff_date": cutoff_date
            }
            missing_fields = [field for field, value in required_fields.items() if not value]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Missing mandatory fields - missing fields: {', '.join(missing_fields)}"
                })
            
            # Validate date relationships
            if not is_valid_date_order(cycle_start_date, cycle_end_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid date relationships - start date must be before end date"
                })
            
            if not is_cutoff_within_range(cutoff_date, cycle_start_date, cycle_end_date):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Invalid date relationships - cutoff date must be within cycle range"
                })
            
            # Check for overlapping cycles
            if check_overlapping_cycles(cycle_start_date, cycle_end_date, payroll_cycles):
                return json.dumps({
                    "success": False,
                    "error": "Halt: Overlapping cycles detected - new cycle overlaps with existing cycle"
                })
            
            # Validate frequency
            valid_frequencies = ["weekly", "bi_weekly", "monthly"]
            if frequency not in valid_frequencies:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid frequency - must be one of: {', '.join(valid_frequencies)}"
                })
            
            # Generate new cycle ID
            new_cycle_id = generate_id(payroll_cycles)
            
            # Create payroll cycle
            new_cycle = {
                "cycle_id": new_cycle_id,
                "cycle_start_date": cycle_start_date,
                "cycle_end_date": cycle_end_date,
                "frequency": frequency,
                "cutoff_date": cutoff_date,
                "status": "open",
                "created_at": "2025-10-01T12:00:00",
                "updated_at": "2025-10-01T12:00:00"
            }
            
            payroll_cycles[new_cycle_id] = new_cycle
            
            # Create audit entry for cycle creation
            audit_trails = data.get("audit_trails", {})
            audit_id = generate_id(audit_trails)
            audit_entry = {
                "audit_id": audit_id,
                "reference_id": new_cycle_id,
                "reference_type": "payroll",
                "action": "create",
                "user_id": requesting_user_id,
                "field_name": None,
                "old_value": None,
                "new_value": json.dumps(new_cycle),
                "created_at": "2025-10-01T12:00:00"
            }
            audit_trails[audit_id] = audit_entry
            
            return json.dumps({
                "success": True,
                "operation": "create_cycle",
                "cycle_id": new_cycle_id,
                "message": f"Payroll cycle {new_cycle_id} created successfully",
                "cycle_data": new_cycle
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_payroll_cycle_operations",
                "description": "Manage payroll cycle operations in the HR talent management system. This tool handles the creation of new payroll cycles with comprehensive validation including date relationships, frequency validation, and overlap detection. Essential for establishing payroll processing periods with proper cutoff dates and ensuring no conflicting cycles exist. Validates that only active HR Payroll Administrators can create cycles and enforces all business rules for cycle creation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_cycle' to establish a new payroll cycle",
                            "enum": ["create_cycle"]
                        },
                        "cycle_start_date": {
                            "type": "string",
                            "description": "Cycle start date in YYYY-MM-DD format (required, must be before end date)"
                        },
                        "cycle_end_date": {
                            "type": "string",
                            "description": "Cycle end date in YYYY-MM-DD format (required, must be after start date)"
                        },
                        "frequency": {
                            "type": "string",
                            "description": "Payroll frequency",
                            "enum": ["weekly", "bi_weekly", "monthly"]
                        },
                        "cutoff_date": {
                            "type": "string",
                            "description": "Cutoff date for payroll processing in YYYY-MM-DD format (required, must be within cycle range)"
                        },
                        "requesting_user_id": {
                            "type": "string",
                            "description": "User ID creating the cycle (required, must be active hr_payroll_administrator, hr_manager, or hr_admin)"
                        }
                    },
                    "required": ["operation_type", "cycle_start_date", "cycle_end_date", "frequency", "cutoff_date", "requesting_user_id"]
                }
            }
        }
