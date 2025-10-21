import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ControlSkill(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, skill_id: str = None, skill_name: str = None) -> str:
        """
        Enable, disable, and configure Alexa Skills in the smart home management system.
        Handles skill enablement, disablement, search, and detail retrieval operations.
        """
        
        # Validate operation type
        valid_operations = ["enable", "disable", "search", "get_details"]
        if operation not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # Get skills table from schema
        skills = data.get("skills", {})
        
        if operation == "enable":
            # Enable an Alexa Skill
            if not skill_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: skill_id required for enable operation"
                })
            
            # Validate skill exists
            if skill_id not in skills:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill not found - skill_id '{skill_id}' does not exist"
                })
            
            skill = skills[skill_id]
            
            # Check if skill already enabled
            if skill.get("enablement_status") == "enabled":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill '{skill.get('skill_name')}' is already enabled"
                })
            
            # Enable the skill
            skill["enablement_status"] = "enabled"
            skill["enabled_date"] = "2025-10-16T14:30:00"
            skill["updated_date"] = "2025-10-16T14:30:00"
            
            return json.dumps({
                "success": True,
                "operation": "enable",
                "skill_id": skill_id,
                "skill_name": skill.get("skill_name"),
                "publisher": skill.get("publisher"),
                "enablement_status": "enabled",
                "enabled_date": "2025-10-16T14:30:00",
                "message": f"Skill '{skill.get('skill_name')}' enabled successfully"
            })
        
        elif operation == "disable":
            # Disable an Alexa Skill
            if not skill_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: skill_id required for disable operation"
                })
            
            # Validate skill exists
            if skill_id not in skills:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill not found - skill_id '{skill_id}' does not exist"
                })
            
            skill = skills[skill_id]
            
            # Check if skill already disabled
            if skill.get("enablement_status") == "disabled":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill '{skill.get('skill_name')}' is already disabled"
                })
            
            # Disable the skill
            skill["enablement_status"] = "disabled"
            skill["updated_date"] = "2025-10-16T14:30:00"
            
            return json.dumps({
                "success": True,
                "operation": "disable",
                "skill_id": skill_id,
                "skill_name": skill.get("skill_name"),
                "publisher": skill.get("publisher"),
                "enablement_status": "disabled",
                "disabled_date": "2025-10-16T14:30:00",
                "message": f"Skill '{skill.get('skill_name')}' disabled successfully"
            })
        
        elif operation == "search":
            # Search for skills by name
            if not skill_name:
                return json.dumps({
                    "success": False,
                    "error": "Halt: skill_name required for search operation"
                })
            
            # Search for skills matching the name
            matching_skills = []
            for sid, skill in skills.items():
                if skill_name.lower() in skill.get("skill_name", "").lower():
                    matching_skills.append({
                        "skill_id": sid,
                        "skill_name": skill.get("skill_name"),
                        "publisher": skill.get("publisher"),
                        "description": skill.get("description"),
                        "enablement_status": skill.get("enablement_status"),
                        "ratings": skill.get("ratings")
                    })
            
            return json.dumps({
                "success": True,
                "operation": "search",
                "search_query": skill_name,
                "results_count": len(matching_skills),
                "matching_skills": matching_skills,
                "message": f"Found {len(matching_skills)} skills matching '{skill_name}'"
            })
        
        elif operation == "get_details":
            # Get detailed information about a skill
            if not skill_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: skill_id required for get_details operation"
                })
            
            # Validate skill exists
            if skill_id not in skills:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill not found - skill_id '{skill_id}' does not exist"
                })
            
            skill = skills[skill_id]
            
            # Return complete skill details
            skill_details = {
                "skill_id": skill_id,
                "skill_name": skill.get("skill_name"),
                "publisher": skill.get("publisher"),
                "description": skill.get("description"),
                "permissions_required": skill.get("permissions_required"),
                "account_linking_status": skill.get("account_linking_status"),
                "account_linking_data": skill.get("account_linking_data"),
                "enablement_status": skill.get("enablement_status"),
                "ratings": skill.get("ratings"),
                "enabled_date": skill.get("enabled_date"),
                "created_date": skill.get("created_date"),
                "updated_date": skill.get("updated_date")
            }
            
            return json.dumps({
                "success": True,
                "operation": "get_details",
                "skill_id": skill_id,
                "skill_details": skill_details,
                "message": f"Retrieved details for skill '{skill.get('skill_name')}'"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "control_skill",
                "description": "Enable, disable, and configure Alexa Skills in the smart home management system. Handles skill enablement by updating enablement_status to 'enabled', skill disablement by updating enablement_status to 'disabled', skill search by name for discovery, and detailed skill information retrieval. Updates enabled_date timestamp on enablement.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Skill management operation to perform",
                            "enum": ["enable", "disable", "search", "get_details"]
                        },
                        "skill_id": {
                            "type": "string",
                            "description": "Unique identifier of the skill (required for enable, disable, get_details)"
                        },
                        "skill_name": {
                            "type": "string",
                            "description": "Skill name for search (required for search operation)"
                        }
                    },
                    "required": ["operation"]
                }
            }
        }