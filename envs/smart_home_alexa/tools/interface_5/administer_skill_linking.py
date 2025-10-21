import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class AdministerSkillLinking(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, skill_id: str, operation_parameters: Dict[str, Any] = None) -> str:
        """
        Manage skill account linking and authorization in the smart home management system.
        Handles initiation of account linking workflow, waiting for user authorization completion,
        and unlinking accounts from skills.
        """

        # Validate operation type
        valid_operations = ["initiate_linking", "wait_authorization", "unlink_account"]
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

        # Validate skill exists
        if skill_id not in skills:
            return json.dumps({
                "success": False,
                "error": f"Halt: Skill not found - skill_id '{skill_id}' does not exist"
            })

        skill = skills[skill_id]

        if not operation_parameters:
            operation_parameters = {}

        if operation == "initiate_linking":
            # Initiate account linking process for skill

            # Check if skill requires account linking
            permissions_required = skill.get("permissions_required")
            if not permissions_required:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill '{skill.get('skill_name')}' does not require account linking"
                })

            # Check if already linked
            if skill.get("account_linking_status") == "linked":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill '{skill.get('skill_name')}' is already linked"
                })

            # Generate linking URL (simulated)
            linking_url = f"https://alexa.amazon.com/api/skill-account-linking/{skill_id}/authorize"
            linking_code = f"LINK_{skill_id[:8].upper()}"

            # Update skill linking status to pending
            skill["account_linking_status"] = "pending_authorization"
            skill["account_linking_data"] = json.dumps({
                "linking_initiated_at": "2025-10-16T14:30:00",
                "linking_code": linking_code,
                "linking_url": linking_url,
                "status": "awaiting_user_authorization"
            })
            skill["updated_date"] = "2025-10-16T14:30:00"

            return json.dumps({
                "success": True,
                "operation": "initiate_linking",
                "skill_id": skill_id,
                "skill_name": skill.get("skill_name"),
                "publisher": skill.get("publisher"),
                "linking_url": linking_url,
                "linking_code": linking_code,
                "instructions": "Visit the linking URL and authorize the skill to access your account",
                "message": f"Account linking initiated for skill '{skill.get('skill_name')}' - user authorization required"
            })

        elif operation == "wait_authorization":
            # Wait for user to complete authorization and verify linking
            timeout_minutes = operation_parameters.get("timeout_minutes", 5)

            if not isinstance(timeout_minutes, (int, float)) or timeout_minutes <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: timeout_minutes must be a positive number"
                })

            # Check if linking was initiated
            if skill.get("account_linking_status") not in ["pending_authorization", "linked"]:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Account linking not initiated for skill '{skill.get('skill_name')}'"
                })

            # Check if already linked
            if skill.get("account_linking_status") == "linked":
                return json.dumps({
                    "success": True,
                    "operation": "wait_authorization",
                    "skill_id": skill_id,
                    "skill_name": skill.get("skill_name"),
                    "linking_status": "already_linked",
                    "message": f"Skill '{skill.get('skill_name')}' is already linked"
                })

            # Simulate waiting for authorization
            # In real implementation, this would poll the Alexa API
            authorization_completed = True  # Simulated result

            if not authorization_completed:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: User authorization not completed within {timeout_minutes} minutes timeout"
                })

            # Update skill to linked status
            linking_data = json.loads(skill.get("account_linking_data", "{}"))
            linking_data["status"] = "authorized"
            linking_data["linked_at"] = "2025-10-16T14:35:00"
            linking_data["linked_account_identifier"] = f"user_account_{skill_id[:6]}"

            skill["account_linking_status"] = "linked"
            skill["account_linking_data"] = json.dumps(linking_data)
            skill["updated_date"] = "2025-10-16T14:35:00"

            return json.dumps({
                "success": True,
                "operation": "wait_authorization",
                "skill_id": skill_id,
                "skill_name": skill.get("skill_name"),
                "linking_status": "linked",
                "linked_account": linking_data["linked_account_identifier"],
                "linked_at": "2025-10-16T14:35:00",
                "elapsed_minutes": timeout_minutes,
                "message": f"Account linking completed successfully for skill '{skill.get('skill_name')}'"
            })

        elif operation == "unlink_account":
            # Unlink account from skill

            # Check if skill is linked
            if skill.get("account_linking_status") != "linked":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Skill '{skill.get('skill_name')}' is not currently linked"
                })

            # Store previous linking data for audit
            previous_linking_data = skill.get("account_linking_data")

            # Update skill to unlinked status
            skill["account_linking_status"] = "not_linked"
            skill["account_linking_data"] = json.dumps({
                "unlinked_at": "2025-10-16T14:30:00",
                "previous_link_removed": True
            })
            skill["updated_date"] = "2025-10-16T14:30:00"

            return json.dumps({
                "success": True,
                "operation": "unlink_account",
                "skill_id": skill_id,
                "skill_name": skill.get("skill_name"),
                "linking_status": "not_linked",
                "unlinked_at": "2025-10-16T14:30:00",
                "message": f"Account unlinked successfully from skill '{skill.get('skill_name')}'"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_skill_linking",
                "description": "Manage skill account linking and authorization in the smart home management system. Initiates account linking workflow by generating authorization URLs and codes for skills that require third-party account access (SOP 6.8.2), waits for user authorization completion with timeout handling and validates linking status, and unlinks accounts from skills when access revocation is needed. Supports OAuth-based linking workflows common in smart home integrations. Updates skill linking status and maintains linking metadata for audit trails.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Linking operation to perform",
                            "enum": ["initiate_linking", "wait_authorization", "unlink_account"]
                        },
                        "skill_id": {
                            "type": "string",
                            "description": "Unique identifier of the skill (required for all operations)"
                        },
                        "operation_parameters": {
                            "type": "object",
                            "description": "Operation-specific parameters. For wait_authorization: {timeout_minutes} (default: 5)",
                            "properties": {
                                "timeout_minutes": {
                                    "type": "number",
                                    "description": "Maximum wait time in minutes for user authorization (default: 5)"
                                }
                            }
                        }
                    },
                    "required": ["operation", "skill_id"]
                }
            }
        }
