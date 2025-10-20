import json
import re
from typing import Any, Dict, Optional, List
from tau_bench.envs.tool import Tool
from datetime import datetime

class GetSystemEntities(Tool):

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
    def _filter_entity(entity: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Applies all filters to a single entity record."""
        for key, value in filters.items():
            if value is None:
                continue

            # --- Date Range Filtering ---
            if key.endswith("_from") or key.endswith("_to"):
                # Determine the base field name (e.g., 'exit_date' from 'exit_date_from')
                base_field = key[:-5]
                date_str = entity.get(base_field)

                # Skip comparison if the entity record doesn't have the date field
                if not date_str:
                    continue

                converted_date = date_str
                
                if value:
                    filter_date_str = DiscoverSystemEntities._convert_date_format(value)
                    
                    if key.endswith("_from") and converted_date < filter_date_str:
                        return False
                    if key.endswith("_to") and converted_date > filter_date_str:
                        return False
            
            # --- Standard Comparison for all other fields (ID, Status, Text, etc.) ---
            else:
                entity_value = entity.get(key)
                # Convert both to string for consistent comparison (IDs are often stored as strings)
                if str(entity_value) != str(value):
                    return False
            
        return True

    # --- Core Tool Logic ---

    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Locates and retrieves System Entities (Employee Exits, Notifications, and Audit Trails)
        based on entity type and search criteria.
        """
        valid_entity_types = ["employee_exits", "notifications", "audit_trails"]
        
        if not entity_type or entity_type not in valid_entity_types:
            return json.dumps({
                "success": False,
                "message": f"Missing or invalid entity_type '{entity_type}'. Must be one of: {', '.join(valid_entity_types)}."
            }) # Halt Condition: Missing or invalid entity_type

        filters = filters or {}
        
        # 1. Define Valid Keys and Data Source
        valid_keys: List[str]
        
        if entity_type == "employee_exits":
            valid_keys = [
                "exit_id", "employee_id", "exit_date_from", "exit_date_to", "manager_clearance", 
                "it_equipment_return", "finance_settlement_status", "clearance_status", 
                "approved_by", "approval_date_from", "approval_date_to", "paid_date_from", "paid_date_to"
            ]
            data_source = data.get("employee_exits", {})

        elif entity_type == "notifications":
            valid_keys = [
                "notification_id", "recipient_user_id", "recipient_email", "notification_type", 
                "reference_type", "reference_id", "notification_status"
            ]
            data_source = data.get("notifications", {})
        
        elif entity_type == "audit_trails":
            valid_keys = [
                "audit_id", "reference_id", "reference_type", "action", "user_id", "field_name"
            ]
            data_source = data.get("audit_trails", {})
        
        # 2. Validate Filters
        for key, value in filters.items():
            if key not in valid_keys:
                return json.dumps({
                    "success": False,
                    "message": f"Invalid filter key '{key}' provided for entity_type '{entity_type}'."
                })
            
            if key.endswith(("_from", "_to")):
                error = DiscoverSystemEntities._validate_date_format(value, key)
                if error: return json.dumps({"success": False, "message": error})

        # 3. Execute Discovery
        found_entities: List[Dict[str, Any]] = []
        
        for entity_id, entity_record in data_source.items():
            # Quick check for primary ID match if provided (e.g., exit_id)
            id_key = f"{entity_type[:-1]}_id"
            if entity_type == "employee_exits": id_key = "exit_id"
            elif entity_type == "audit_trails": id_key = "audit_id"
            
            if filters.get(id_key) and str(entity_id) != str(filters.get(id_key)):
                continue

            if DiscoverSystemEntities._filter_entity(entity_record, filters):
                found_entities.append(entity_record)

        # 4. Process Results
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
                "name": "get_system_entities",
                "description": "Systematically locates and retrieves System entities (employee_exits, notifications, and audit_trails) from the HR system based on entity type and search criteria (filters).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "The specific type of entity to search for. Mandatory.",
                            "enum": ["employee_exits", "notifications", "audit_trails"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "A dictionary of criteria to filter the entities. Keys must be valid for the specified entity_type.",
                            "properties": {
                                # Employee Exit Keys
                                "exit_id": {"type": "string", "description": "Unique identifier of the exit record."},
                                "employee_id": {"type": "string", "description": "Employee ID related to the exit."},
                                "exit_date_from": {"type": "string", "description": "Start date for the employee's exit date range (MM-DD-YYYY)."},
                                "exit_date_to": {"type": "string", "description": "End date for the employee's exit date range (MM-DD-YYYY)."},
                                "manager_clearance": {"type": "string", "description": "Manager sign-off status."},
                                "it_equipment_return": {"type": "string", "description": "IT equipment return status."},
                                "finance_settlement_status": {"type": "string", "description": "Finance settlement status."},
                                "clearance_status": {"type": "string", "description": "Overall clearance status (e.g., pending, cleared, rejected)."},
                                "approved_by": {"type": "string", "description": "User ID who approved the settlement."},
                                "approval_date_from": {"type": "string", "description": "Start date for settlement approval date range (MM-DD-YYYY)."},
                                "approval_date_to": {"type": "string", "description": "End date for settlement approval date range (MM-DD-YYYY)."},
                                "paid_date_from": {"type": "string", "description": "Start date for settlement paid date range (MM-DD-YYYY)."},
                                "paid_date_to": {"type": "string", "description": "End date for settlement paid date range (MM-DD-YYYY)."},
                                
                                # Notification Keys
                                "notification_id": {"type": "string", "description": "Unique identifier of the notification."},
                                "recipient_user_id": {"type": "string", "description": "User ID who received the notification."},
                                "recipient_email": {"type": "string", "description": "Email address of the notification recipient."},
                                "notification_type": {"type": "string", "description": "Type of notification (e.g., email, system, alert)."},
                                "reference_type": {"type": "string", "description": "Type of entity the notification refers to (e.g., 'application', 'payslip')."},
                                "reference_id": {"type": "string", "description": "ID of the entity the notification refers to."},
                                "notification_status": {"type": "string", "description": "Status of the notification (e.g., sent, delivered, read, failed)."},

                                # Audit Trail Keys
                                "audit_id": {"type": "string", "description": "Unique identifier of the audit record."},
                                "action": {"type": "string", "description": "Type of action logged (e.g., create, update, delete)."},
                                "user_id": {"type": "string", "description": "User ID who performed the action."},
                                "field_name": {"type": "string", "description": "Specific field name that was changed (for update actions)."},
                            },
                            "additionalProperties": False
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
