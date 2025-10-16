import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class DiscoverPayrollEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, filters: Optional[Dict[str, Any]] = None) -> str:
        """
        Discover payroll entities including cycles, inputs, and earnings with optional filtering.
        
        Entity Types:
        - payroll_cycles: Discover payroll cycles with date, frequency, and status filters
        - payroll_inputs: Discover payroll inputs with employee, cycle, and approval filters
        - payroll_earnings: Discover payroll earnings with type, amount, and approval filters
        """
        
        def is_date_in_range(date_str: str, start_date: Optional[str], end_date: Optional[str]) -> bool:
            """Check if date is within the specified range"""
            if start_date and date_str < start_date:
                return False
            if end_date and date_str > end_date:
                return False
            return True
        
        def is_amount_in_range(amount: float, min_amount: Optional[float], max_amount: Optional[float]) -> bool:
            """Check if amount is within the specified range"""
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True
        
        def matches_filter(entity: Dict[str, Any], filter_key: str, filter_value: Any) -> bool:
            """Check if entity matches a specific filter"""
            entity_value = entity.get(filter_key)
            
            if entity_value is None:
                return False
            
            # Handle different filter types
            if filter_key.endswith('_from') or filter_key.endswith('_to'):
                # Date range filters
                base_key = filter_key.replace('_from', '').replace('_to', '')
                if base_key in entity:
                    if filter_key.endswith('_from'):
                        return entity[base_key] >= filter_value
                    else:  # _to
                        return entity[base_key] <= filter_value
            elif filter_key.endswith('_min') or filter_key.endswith('_max'):
                # Numeric range filters
                base_key = filter_key.replace('_min', '').replace('_max', '')
                if base_key in entity:
                    if filter_key.endswith('_min'):
                        return entity[base_key] >= filter_value
                    else:  # _max
                        return entity[base_key] <= filter_value
            else:
                # Exact match filters
                return str(entity_value).lower() == str(filter_value).lower()
            
            return False
        
        def apply_filters(entities: Dict[str, Any], valid_filters: List[str], filters: Dict[str, Any]) -> Dict[str, Any]:
            """Apply filters to entities and return matching results"""
            if not filters:
                return entities
            
            # Validate filter keys
            invalid_filters = [key for key in filters.keys() if key not in valid_filters]
            if invalid_filters:
                return {
                    "error": f"Invalid filter keys: {', '.join(invalid_filters)}. Valid filters are: {', '.join(valid_filters)}"
                }
            
            filtered_entities = {}
            for entity_id, entity in entities.items():
                matches = True
                for filter_key, filter_value in filters.items():
                    if not matches_filter(entity, filter_key, filter_value):
                        matches = False
                        break
                
                if matches:
                    filtered_entities[entity_id] = entity
            
            return filtered_entities
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll entity discovery"
            })
        
        if entity_type not in ["payroll_cycles", "payroll_inputs", "payroll_earnings"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: payroll_cycles, payroll_inputs, payroll_earnings"
            })
        
        if entity_type == "payroll_cycles":
            entities = data.get("payroll_cycles", {})
            valid_filters = [
                "cycle_id", "cycle_start_date_from", "cycle_start_date_to", 
                "cycle_end_date_from", "cycle_end_date_to", "frequency", 
                "cutoff_date_from", "cutoff_date_to", "status"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "payroll_cycles",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
        
        elif entity_type == "payroll_inputs":
            entities = data.get("payroll_inputs", {})
            valid_filters = [
                "input_id", "employee_id", "cycle_id", "hours_worked_min", 
                "hours_worked_max", "overtime_hours_min", "overtime_hours_max", 
                "manager_approval_status", "manager_approved_by", "input_status"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "payroll_inputs",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
        
        elif entity_type == "payroll_earnings":
            entities = data.get("payroll_earnings", {})
            valid_filters = [
                "earning_id", "payroll_input_id", "employee_id", "earning_type", 
                "amount_min", "amount_max", "approval_status", "approved_by", 
                "approval_date_from", "approval_date_to"
            ]
            
            if filters:
                filtered_entities = apply_filters(entities, valid_filters, filters)
                if "error" in filtered_entities:
                    return json.dumps({
                        "success": False,
                        "error": filtered_entities["error"]
                    })
                entities = filtered_entities
            
            return json.dumps({
                "success": True,
                "entity_type": "payroll_earnings",
                "count": len(entities),
                "entities": entities,
                "filters_applied": filters or {}
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_payroll_entities",
                "description": "Discover and filter payroll entities in the HR talent management system. This tool allows comprehensive discovery of payroll cycles, payroll inputs, and payroll earnings with flexible filtering options. Supports date range filtering, numeric range filtering, and exact match filtering. Essential for payroll reporting, data analysis, and operational oversight of payroll processes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of payroll entity to discover",
                            "enum": ["payroll_cycles", "payroll_inputs", "payroll_earnings"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply. For payroll_cycles: cycle_id, cycle_start_date_from, cycle_start_date_to, cycle_end_date_from, cycle_end_date_to, frequency, cutoff_date_from, cutoff_date_to, status. For payroll_inputs: input_id, employee_id, cycle_id, hours_worked_min, hours_worked_max, overtime_hours_min, overtime_hours_max, manager_approval_status, manager_approved_by, input_status. For payroll_earnings: earning_id, payroll_input_id, employee_id, earning_type, amount_min, amount_max, approval_status, approved_by, approval_date_from, approval_date_to. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                # Payroll Cycles filters
                                "cycle_id": {"type": "string", "description": "Exact cycle ID match"},
                                "cycle_start_date_from": {"type": "string", "description": "Cycle start date from (YYYY-MM-DD)"},
                                "cycle_start_date_to": {"type": "string", "description": "Cycle start date to (YYYY-MM-DD)"},
                                "cycle_end_date_from": {"type": "string", "description": "Cycle end date from (YYYY-MM-DD)"},
                                "cycle_end_date_to": {"type": "string", "description": "Cycle end date to (YYYY-MM-DD)"},
                                "frequency": {"type": "string", "description": "Payroll frequency", "enum": ["weekly", "bi_weekly", "monthly"]},
                                "cutoff_date_from": {"type": "string", "description": "Cutoff date from (YYYY-MM-DD)"},
                                "cutoff_date_to": {"type": "string", "description": "Cutoff date to (YYYY-MM-DD)"},
                                "status": {"type": "string", "description": "Cycle status", "enum": ["open", "active", "locked", "closed", "archived"]},
                                
                                # Payroll Inputs filters
                                "input_id": {"type": "string", "description": "Exact input ID match"},
                                "employee_id": {"type": "string", "description": "Employee ID match"},
                                "cycle_id": {"type": "string", "description": "Cycle ID match"},
                                "hours_worked_min": {"type": "number", "description": "Minimum hours worked"},
                                "hours_worked_max": {"type": "number", "description": "Maximum hours worked"},
                                "overtime_hours_min": {"type": "number", "description": "Minimum overtime hours"},
                                "overtime_hours_max": {"type": "number", "description": "Maximum overtime hours"},
                                "manager_approval_status": {"type": "string", "description": "Manager approval status", "enum": ["pending", "approved", "rejected"]},
                                "manager_approved_by": {"type": "string", "description": "Manager who approved"},
                                "input_status": {"type": "string", "description": "Input status", "enum": ["draft", "submitted", "exception", "ready_for_payroll", "locked"]},
                                
                                # Payroll Earnings filters
                                "earning_id": {"type": "string", "description": "Exact earning ID match"},
                                "payroll_input_id": {"type": "string", "description": "Payroll input ID match"},
                                "employee_id": {"type": "string", "description": "Employee ID match"},
                                "earning_type": {"type": "string", "description": "Earning type", "enum": ["bonus", "incentive", "reimbursement", "commission", "other"]},
                                "amount_min": {"type": "number", "description": "Minimum earning amount"},
                                "amount_max": {"type": "number", "description": "Maximum earning amount"},
                                "approval_status": {"type": "string", "description": "Approval status", "enum": ["pending", "approved", "rejected"]},
                                "approved_by": {"type": "string", "description": "User who approved"},
                                "approval_date_from": {"type": "string", "description": "Approval date from (YYYY-MM-DD)"},
                                "approval_date_to": {"type": "string", "description": "Approval date to (YYYY-MM-DD)"}
                            }
                        }
                    },
                    "required": ["entity_type"]
                }
            }
        }
