import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool
from datetime import datetime

class FetchPaymentEntities(Tool):

    # --- Utility Methods ---

    @staticmethod
    def _validate_date_format(date_str: str, field_name: str) -> Optional[str]:
        """Validates date format is MM-DD-YYYY."""
        if date_str:
            date_pattern = r'^\d{2}-\d{2}-\d{4}$'
            if not re.match(date_pattern, date_str):
                return f"Invalid {field_name} format. Must be MM-DD-YYYY."
            try:
                datetime.strptime(date_str, '%m-%d-%Y')
            except ValueError:
                return f"Invalid date value provided for {field_name}. Please check month/day/year validity."
        return None

    @staticmethod
    def _convert_date_format(date_str: str) -> str:
        """Converts MM-DD-YYYY to YYYY-MM-DD for internal comparison."""
        if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
            try:
                dt = datetime.strptime(date_str, '%m-%d-%Y')
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                return date_str
        return date_str

    @staticmethod
    def _validate_numeric_range(value: Any, field_name: str) -> Optional[str]:
        """Validates that a filter value is a non-negative number."""
        if value is not None:
            try:
                if float(value) < 0:
                    return f"{field_name} cannot be negative."
            except ValueError:
                return f"{field_name} must be a valid number."
        return None

    @staticmethod
    def _filter_entity(entity: Dict[str, Any], entity_type: str, filters: Dict[str, Any]) -> bool:
        """Applies all filters to a single entity record."""
        for key, value in filters.items():
            if value is None:
                continue

            # Standard comparison for direct match fields
            if key in ["payslip_id", "payment_id", "employee_id", "cycle_id", "payment_method", "transaction_id"]:
                if str(entity.get(key)) != str(value):
                    return False
            
            # Status and Proration Fields (requires exact match)
            elif key in ["proration_status", "payslip_status", "payment_status"]:
                if entity.get(key) != value:
                    return False

            # --- Date Range Filtering ---
            elif key.endswith("_from") or key.endswith("_to"):
                # Get the base field name (e.g., 'released_date' from 'released_date_from')
                base_field = key[:-5]
                date_str = entity.get(base_field)
                if not date_str:
                    continue

                converted_date = date_str
                # Only compare if the filter is provided
                if value:
                    filter_date_str = DiscoverPaymentEntities._convert_date_format(value)
                    
                    if key.endswith("_from") and converted_date < filter_date_str:
                        return False
                    if key.endswith("_to") and converted_date > filter_date_str:
                        return False

            # --- Numeric Range Filtering (Min/Max) ---
            elif key.endswith("_min") or key.endswith("_max"):
                # Get the base field name (e.g., 'gross_pay' from 'gross_pay_min')
                base_field = key[:-4]
                entity_value = entity.get(base_field)

                # Ensure entity value is numeric for comparison
                if entity_value is None:
                    continue
                try:
                    entity_value = float(entity_value)
                except (ValueError, TypeError):
                    continue
                
                if value is not None:
                    filter_value = float(value)
                    if key.endswith("_min") and entity_value < filter_value:
                        return False
                    if key.endswith("_max") and entity_value > filter_value:
                        return False
            
        return True

    # --- Core Tool Logic ---

    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Locates and retrieves Payslip and Payment entities based on search criteria.
        """
        if not entity_type or entity_type not in ["payslips", "payments"]:
            return json.dumps({
                "success": False,
                "message": f"Missing or invalid entity_type '{entity_type}'. Must be 'payslips' or 'payments'."
            }) # Halt Condition: Missing or invalid entity_type

        filters = filters or {}
        
        # Define valid keys and perform preliminary validation
        if entity_type == "payslips":
            valid_keys = [
                "payslip_id", "employee_id", "cycle_id", "gross_pay_min", "gross_pay_max", 
                "base_salary_min", "base_salary_max", "total_deductions_min", "total_deductions_max", 
                "net_pay_min", "net_pay_max", "proration_status", "payslip_status", 
                "released_date_from", "released_date_to"
            ]
            data_source = data.get("payslips", {})

        elif entity_type == "payments":
            valid_keys = [
                "payment_id", "employee_id", "cycle_id", "payslip_id", "amount_min", "amount_max", 
                "payment_date_from", "payment_date_to", "payment_method", "payment_status", "transaction_id"
            ]
            data_source = data.get("payments", {})
        
        # 1. Validate Filters
        for key, value in filters.items():
            if key not in valid_keys:
                return json.dumps({
                    "success": False,
                    "message": f"Invalid filter key '{key}' provided for entity_type '{entity_type}'."
                })
            
            if key.endswith(("_min", "_max", "_pay", "_amount", "_salary", "_deductions")):
                error = DiscoverPaymentEntities._validate_numeric_range(value, key)
                if error: return json.dumps({"success": False, "message": error})

            if key.endswith(("_from", "_to")):
                error = DiscoverPaymentEntities._validate_date_format(value, key)
                if error: return json.dumps({"success": False, "message": error})

        # 2. Execute Discovery
        found_entities: List[Dict[str, Any]] = []
        
        for entity_id, entity_record in data_source.items():
            # If the entity ID is provided as a filter, short-circuit
            id_key = f"{entity_type[:-1]}_id" # payslip_id or payment_id
            if filters.get(id_key) and str(entity_id) != str(filters.get(id_key)):
                continue

            if DiscoverPaymentEntities._filter_entity(entity_record, entity_type, filters):
                found_entities.append(entity_record)

        # 3. Process Results
        if not found_entities:
            return json.dumps({
                "success": True,
                "entity_type": entity_type,
                "count": 0,
                "message": f"No {entity_type} entities found matching the criteria.",
                "entities": []
            })
        
        return json.dumps({
            "success": True,
            "entity_type": entity_type,
            "count": len(found_entities),
            "message": f"Successfully retrieved {len(found_entities)} {entity_type} entities.",
            "entities": found_entities
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_payment_entities",
                "description": "Systematically locates and retrieves Payment-related entities (payslips and payments) from the HR system based on entity type and search criteria (filters).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "The specific type of entity to search for. Mandatory.",
                            "enum": ["payslips", "payments"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "A dictionary of criteria to filter the entities. Keys must be valid for the specified entity_type.",
                            "properties": {
                                # Payslip Keys
                                "payslip_id": {"type": "string", "description": "Unique identifier of the payslip."},
                                "gross_pay_min": {"type": "number", "description": "Minimum gross pay amount."},
                                "gross_pay_max": {"type": "number", "description": "Maximum gross pay amount."},
                                "base_salary_min": {"type": "number", "description": "Minimum base salary amount."},
                                "base_salary_max": {"type": "number", "description": "Maximum base salary amount."},
                                "total_deductions_min": {"type": "number", "description": "Minimum total deductions amount."},
                                "total_deductions_max": {"type": "number", "description": "Maximum total deductions amount."},
                                "net_pay_min": {"type": "number", "description": "Minimum net pay amount."},
                                "net_pay_max": {"type": "number", "description": "Maximum net pay amount."},
                                "proration_status": {"type": "string", "description": "Proration status of the payslip."},
                                "payslip_status": {"type": "string", "description": "Status of the payslip (e.g., released, draft, calculated)."},
                                "released_date_from": {"type": "string", "description": "Start date for payslip release date range (MM-DD-YYYY)."},
                                "released_date_to": {"type": "string", "description": "End date for payslip release date range (MM-DD-YYYY)."},
                                
                                # Payment Keys
                                "payment_id": {"type": "string", "description": "Unique identifier of the payment record."},
                                "amount_min": {"type": "number", "description": "Minimum payment amount."},
                                "amount_max": {"type": "number", "description": "Maximum payment amount."},
                                "payment_date_from": {"type": "string", "description": "Start date for payment date range (MM-DD-YYYY)."},
                                "payment_date_to": {"type": "string", "description": "End date for payment date range (MM-DD-YYYY)."},
                                "payment_method": {"type": "string", "description": "Method of payment (e.g., ACH, check)."},
                                "payment_status": {"type": "string", "description": "Status of the payment (e.g., successful, failed, pending)."},
                                "transaction_id": {"type": "string", "description": "External transaction ID for the payment."},
                                
                                # Common Keys
                                "employee_id": {"type": "string", "description": "Employee ID related to the payment/payslip."},
                                "cycle_id": {"type": "string", "description": "Payroll cycle ID related to the payment/payslip."},
                            },
                            "additionalProperties": False # Enforce use of defined keys
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
