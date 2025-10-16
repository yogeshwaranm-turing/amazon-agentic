import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class DiscoverBenefitEntities(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], entity_type: str, plan_id: str = None, benefit_type: str = None, 
               plan_name: str = None, provider_name: str = None, plan_status: str = None,
               effective_from_from: str = None, effective_from_to: str = None,
               effective_until_from: str = None, effective_until_to: str = None,
               enrollment_id: str = None, employee_id: str = None, cycle_id: str = None,
               effective_date_from: str = None, effective_date_to: str = None,
               enrollment_window_start_from: str = None, enrollment_window_start_to: str = None,
               enrollment_window_end_from: str = None, enrollment_window_end_to: str = None,
               enrollment_status: str = None, hr_manager_approval_status: str = None,
               approved_by: str = None, approval_date_from: str = None, approval_date_to: str = None) -> str:
        """
        Discover benefit entities including plans and enrollments with optional filtering.
        
        Entity Types:
        - benefit_plans: Discover benefit plans with type, status, and date filters
        - benefit_enrollments: Discover benefit enrollments with employee, plan, and approval filters
        """
        
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
            else:
                # Exact match filters (case-insensitive for text fields)
                if isinstance(entity_value, str) and isinstance(filter_value, str):
                    return entity_value.lower() == filter_value.lower()
                else:
                    return str(entity_value).lower() == str(filter_value).lower()
            
            return False
        
        def apply_filters(entities: Dict[str, Any], filter_params: Dict[str, Any]) -> Dict[str, Any]:
            """Apply filters to entities and return matching results"""
            # Remove None values from filter parameters
            active_filters = {k: v for k, v in filter_params.items() if v is not None}
            
            if not active_filters:
                return entities
            
            filtered_entities = {}
            for entity_id, entity in entities.items():
                matches = True
                for filter_key, filter_value in active_filters.items():
                    if not matches_filter(entity, filter_key, filter_value):
                        matches = False
                        break
                
                if matches:
                    filtered_entities[entity_id] = entity
            
            return filtered_entities
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for benefit entity discovery"
            })
        
        if entity_type not in ["benefit_plans", "benefit_enrollments"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid entity_type '{entity_type}'. Must be one of: benefit_plans, benefit_enrollments"
            })
        
        if entity_type == "benefit_plans":
            entities = data.get("benefit_plans", {})
            filter_params = {
                "plan_id": plan_id,
                "benefit_type": benefit_type,
                "plan_name": plan_name,
                "provider_name": provider_name,
                "plan_status": plan_status,
                "effective_from_from": effective_from_from,
                "effective_from_to": effective_from_to,
                "effective_until_from": effective_until_from,
                "effective_until_to": effective_until_to
            }
            
            entities = apply_filters(entities, filter_params)
            
            return json.dumps({
                "success": True,
                "entity_type": "benefit_plans",
                "count": len(entities),
                "entities": entities,
                "filters_applied": {k: v for k, v in filter_params.items() if v is not None}
            })
        
        elif entity_type == "benefit_enrollments":
            entities = data.get("benefit_enrollments", {})
            filter_params = {
                "enrollment_id": enrollment_id,
                "employee_id": employee_id,
                "plan_id": plan_id,
                "effective_date_from": effective_date_from,
                "effective_date_to": effective_date_to,
                "enrollment_window_start_from": enrollment_window_start_from,
                "enrollment_window_start_to": enrollment_window_start_to,
                "enrollment_window_end_from": enrollment_window_end_from,
                "enrollment_window_end_to": enrollment_window_end_to,
                "enrollment_status": enrollment_status,
                "hr_manager_approval_status": hr_manager_approval_status,
                "approved_by": approved_by,
                "approval_date_from": approval_date_from,
                "approval_date_to": approval_date_to
            }
            
            entities = apply_filters(entities, filter_params)
            
            return json.dumps({
                "success": True,
                "entity_type": "benefit_enrollments",
                "count": len(entities),
                "entities": entities,
                "filters_applied": {k: v for k, v in filter_params.items() if v is not None}
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_benefit_entities",
                "description": "Discover and filter benefit entities in the HR talent management system. This tool allows comprehensive discovery of benefit plans and benefit enrollments with flexible filtering options. Supports date range filtering and exact match filtering for plan details, enrollment status, and approval information. Essential for benefits administration, enrollment tracking, and benefits reporting.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entity_type": {
                            "type": "string",
                            "description": "Type of benefit entity to discover",
                            "enum": ["benefit_plans", "benefit_enrollments"]
                        },
                        "filters": {
                            "type": "object",
                            "description": "Optional filters to apply. For benefit_plans: plan_id, benefit_type, plan_name, provider_name, plan_status, effective_from_from, effective_from_to, effective_until_from, effective_until_to. For benefit_enrollments: enrollment_id, employee_id, plan_id, effective_date_from, effective_date_to, enrollment_window_start_from, enrollment_window_start_to, enrollment_window_end_from, enrollment_window_end_to, enrollment_status, hr_manager_approval_status, approved_by, approval_date_from, approval_date_to. SYNTAX: {\"key\": \"value\"}",
                            "properties": {
                                # Benefit Plans filters
                                "plan_id": {"type": "string", "description": "Exact plan ID match"},
                                "benefit_type": {"type": "string", "description": "Benefit type", "enum": ["medical", "dental", "vision", "401k", "life_insurance", "disability"]},
                                "plan_name": {"type": "string", "description": "Plan name match (case-insensitive)"},
                                "provider_name": {"type": "string", "description": "Provider name match (case-insensitive)"},
                                "plan_status": {"type": "string", "description": "Plan status", "enum": ["active", "inactive", "discontinued"]},
                                "effective_from_from": {"type": "string", "description": "Effective from date from (YYYY-MM-DD)"},
                                "effective_from_to": {"type": "string", "description": "Effective from date to (YYYY-MM-DD)"},
                                "effective_until_from": {"type": "string", "description": "Effective until date from (YYYY-MM-DD)"},
                                "effective_until_to": {"type": "string", "description": "Effective until date to (YYYY-MM-DD)"},
                                
                                # Benefit Enrollments filters
                                "enrollment_id": {"type": "string", "description": "Exact enrollment ID match"},
                                "employee_id": {"type": "string", "description": "Employee ID match"},
                                "plan_id": {"type": "string", "description": "Plan ID match"},
                                "effective_date_from": {"type": "string", "description": "Effective date from (YYYY-MM-DD)"},
                                "effective_date_to": {"type": "string", "description": "Effective date to (YYYY-MM-DD)"},
                                "enrollment_window_start_from": {"type": "string", "description": "Enrollment window start from (YYYY-MM-DD)"},
                                "enrollment_window_start_to": {"type": "string", "description": "Enrollment window start to (YYYY-MM-DD)"},
                                "enrollment_window_end_from": {"type": "string", "description": "Enrollment window end from (YYYY-MM-DD)"},
                                "enrollment_window_end_to": {"type": "string", "description": "Enrollment window end to (YYYY-MM-DD)"},
                                "enrollment_status": {"type": "string", "description": "Enrollment status", "enum": ["pending", "valid", "outside_window", "approved", "active"]},
                                "hr_manager_approval_status": {"type": "string", "description": "HR manager approval status", "enum": ["pending", "approved", "rejected"]},
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
