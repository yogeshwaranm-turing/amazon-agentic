import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageCandidateOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage candidate operations including creation and updates.
        
        Operations:
        - create_candidate: Create new candidate profile
        - update_candidate: Update candidate profile details
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate operation_type
        valid_operations = ["create_candidate", "update_candidate"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "candidate_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "candidate_id": None,
                "message": "Invalid data format for candidate operations"
            })
        
        candidates = data.get("candidates", {})
        users = data.get("users", {})
        
        if operation_type == "create_candidate":
            required_fields = ["first_name", "last_name", "email_address", "contact_number", "country_of_residence", "created_by", "resume_file_name"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, kwargs["email_address"]):
                return json.dumps({"success": False, "error": "Halt: Invalid email format or phone number format"})
            
            # Validate phone number format (basic validation - digits, spaces, hyphens, plus, parentheses)
            phone_pattern = r'^[\d\s\-\+\(\)]+$'
            if not re.match(phone_pattern, kwargs["contact_number"]):
                return json.dumps({"success": False, "error": "Halt: Invalid email format or phone number format"})
            
            # Verify creator exists and has appropriate role
            created_by_str = str(kwargs["created_by"])
            creator = users.get(created_by_str)
            if not creator or creator.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User is not authorized"})
            
            valid_roles = ["hr_recruiter", "hr_manager", "hr_admin", "hr_director"]
            if creator.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: User is not authorized"})
            
            # Check for duplicate email
            for cand in candidates.values():
                if cand.get("email_address") == kwargs["email_address"]:
                    return json.dumps({"success": False, "error": "Halt: Duplicate candidate (same email or contact number already exists)"})
            
            # Check for duplicate contact number
            for cand in candidates.values():
                if cand.get("contact_number") == kwargs["contact_number"]:
                    return json.dumps({"success": False, "error": "Halt: Duplicate candidate (same email or contact number already exists)"})
            
            # Check for duplicate LinkedIn profile if provided
            if kwargs.get("linkedin_profile"):
                for cand in candidates.values():
                    if cand.get("linkedin_profile") == kwargs["linkedin_profile"]:
                        return json.dumps({"success": False, "error": "Halt: Duplicate candidate (same email or contact number already exists)"})
            
            # Generate new candidate ID and create record
            new_candidate_id = generate_id(candidates)
            timestamp = "2025-01-01T12:00:00"
            
            new_candidate = {
                "candidate_id": str(new_candidate_id),
                "first_name": kwargs["first_name"],
                "last_name": kwargs["last_name"],
                "email_address": kwargs["email_address"],
                "contact_number": kwargs["contact_number"],
                "source_of_application": kwargs.get("source_of_application", ""),
                "country_of_residence": kwargs["country_of_residence"],
                "linkedin_profile": kwargs.get("linkedin_profile", ""),
                "current_ctc": float(kwargs.get("current_ctc", 0)),
                "status": "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            candidates[str(new_candidate_id)] = new_candidate
            
            return json.dumps({
                "success": True,
                "candidate_id": str(new_candidate_id),
                "message": f"Candidate {new_candidate_id} created successfully"
            })
        
        elif operation_type == "update_candidate":
            # Validate required fields
            required_fields = ["candidate_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "candidate_id": None,
                    "message": f"Missing required fields for candidate update: {', '.join(missing_fields)}"
                })
            
            # Validate candidate exists
            cand_id = str(kwargs["candidate_id"])
            if cand_id not in candidates:
                return json.dumps({
                    "success": False,
                    "candidate_id": cand_id,
                    "message": f"Candidate {cand_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "candidate_id": cand_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            candidate = candidates[cand_id]
            
            # Validate candidate is active
            if candidate.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "candidate_id": cand_id,
                    "message": f"Cannot update candidate in '{candidate.get('status')}' status"
                })
            
            # Check for duplicate LinkedIn profile if provided
            if "linkedin_profile" in kwargs and kwargs["linkedin_profile"]:
                for check_cand_id, check_cand in candidates.items():
                    if check_cand_id != cand_id and check_cand.get("linkedin_profile") == kwargs["linkedin_profile"]:
                        return json.dumps({
                            "success": False,
                            "candidate_id": cand_id,
                            "message": f"Another candidate with LinkedIn profile {kwargs['linkedin_profile']} already exists"
                        })
            
            # Update fields
            timestamp = "2025-10-10T12:00:00"
            updateable_fields = ["country_of_residence", "linkedin_profile", "current_ctc", "status"]
            
            for field in updateable_fields:
                if field in kwargs and kwargs[field] is not None:
                    if field == "current_ctc":
                        try:
                            candidate[field] = float(kwargs[field])
                        except (ValueError, TypeError):
                            return json.dumps({
                                "success": False,
                                "candidate_id": cand_id,
                                "message": "Invalid current_ctc format"
                            })
                    elif field == "status":
                        valid_statuses = ["active", "inactive", "suspended"]
                        if kwargs[field] not in valid_statuses:
                            return json.dumps({
                                "success": False,
                                "candidate_id": cand_id,
                                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                            })
                        candidate[field] = kwargs[field]
                    else:
                        candidate[field] = kwargs[field]
            
            candidate["updated_at"] = timestamp
            
            return json.dumps({
                "success": True,
                "candidate_id": cand_id,
                "message": f"Candidate {cand_id} updated successfully"
            })
        
        return json.dumps({
            "success": False,
            "candidate_id": None,
            "message": "Operation not implemented"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_candidate_operations",
                "description": """Manage candidate profiles throughout the recruitment process. This tool handles candidate creation and profile updates.

OPERATION 1: create_candidate - Create a new candidate profile in the system
Required: first_name (string), last_name (string), email_address (string, valid email format), contact_number (string, valid phone format), country_of_residence (string), created_by (user ID string), resume_file_name (string)
Optional: source_of_application (string), linkedin_profile (string URL), current_ctc (number in USD)
Note: User must be active HR Recruiter, HR Manager, HR Admin, or HR Director. Email, phone, and LinkedIn profile (if provided) must be unique - no duplicate candidates allowed. Resume file name must not already exist in system. Returns auto-generated candidate_id.

OPERATION 2: update_candidate - Update existing candidate profile information
Required: candidate_id (string), user_id (string)
Optional: country_of_residence (string), linkedin_profile (string URL), current_ctc (number in USD), status (active/inactive/suspended)
Note: Candidate must exist and be active. LinkedIn profile (if updated) must be unique. Only authorized HR roles can update candidate profiles.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation: 'create_candidate', 'update_candidate'"
                        },
                        "first_name": {
                            "type": "string", 
                            "description": "Candidate's first name (for create_candidate)"
                        },
                        "last_name": {
                            "type": "string", 
                            "description": "Candidate's last name (for create_candidate)"
                        },
                        "email_address": {
                            "type": "string", 
                            "description": "Valid email address - must be unique (for create_candidate)"
                        },
                        "contact_number": {
                            "type": "string", 
                            "description": "Phone number with digits, spaces, hyphens, +, parentheses - must be unique (for create_candidate)"
                        },
                        "country_of_residence": {
                            "type": "string", 
                            "description": "Country where candidate resides (for create/update)"
                        },
                        "created_by": {
                            "type": "string", 
                            "description": "User ID of HR person creating candidate record (for create_candidate)"
                        },
                        "resume_file_name": {
                            "type": "string", 
                            "description": "Name of resume file - must not already exist (for create_candidate)"
                        },
                        "source_of_application": {
                            "type": "string", 
                            "description": "Source channel where candidate applied from (optional for create_candidate)"
                        },
                        "linkedin_profile": {
                            "type": "string", 
                            "description": "LinkedIn profile URL - must be unique (optional for create/update)"
                        },
                        "current_ctc": {
                            "type": "number", 
                            "description": "Current compensation in USD (optional for create/update)"
                        },
                        "candidate_id": {
                            "type": "string", 
                            "description": "ID of candidate to update (for update_candidate)"
                        },
                        "user_id": {
                            "type": "string", 
                            "description": "User performing the update (for update_candidate)"
                        },
                        "status": {
                            "type": "string", 
                            "description": "Candidate status: active, inactive, suspended (for update_candidate)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }

