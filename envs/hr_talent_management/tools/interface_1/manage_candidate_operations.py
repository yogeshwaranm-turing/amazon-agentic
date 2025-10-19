import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ManageCandidateOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage candidate operations including creation and updates.
        
        Operations:
        - create_candidate: Create a new candidate profile
        - update_candidate: Update existing candidate information
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        valid_operations = ["create_candidate", "update_candidate"]
        
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for candidate operations"
            })
        
        candidates = data.get("candidates", {})
        users = data.get("users", {})
        
        # CREATE CANDIDATE
        if operation_type == "create_candidate":
            required_fields = ["first_name", "last_name", "email_address", "contact_number", "country_of_residence", "created_by", "resume_file_name"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify creator exists and has appropriate role
            creator = users.get(kwargs["created_by"])
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
            
            # Create candidate
            cand_id = generate_id(candidates)
            new_candidate = {
                "candidate_id": cand_id,
                "first_name": kwargs["first_name"],
                "last_name": kwargs["last_name"],
                "email_address": kwargs["email_address"],
                "contact_number": kwargs["contact_number"],
                "source_of_application": kwargs.get("source_of_application"),
                "country_of_residence": kwargs["country_of_residence"],
                "linkedin_profile": kwargs.get("linkedin_profile"),
                "current_ctc": kwargs.get("current_ctc"),
                "status": "active",
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00"
            }
            candidates[cand_id] = new_candidate
            
            return json.dumps({"success": True, "candidate_id": cand_id, "message": f"Candidate {cand_id} created successfully"})
        
        # UPDATE CANDIDATE
        elif operation_type == "update_candidate":
            if not kwargs.get("candidate_id") or not kwargs.get("user_id"):
                return json.dumps({"success": False, "error": "Halt: Missing candidate_id or user_id"})
            
            candidate = candidates.get(kwargs["candidate_id"])
            if not candidate:
                return json.dumps({"success": False, "error": "Halt: Candidate not found"})

            if candidate.get("status") == "inactive":
                return json.dumps({"success": False, "error": "Halt: Candidate is inactive"})
            
            # Verify user has appropriate role
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            if user.get("role") not in ["hr_recruiter", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "error": "Halt: User lacks authorization to perform this action"})
            
            # Update fields if provided
            updatable_fields = ["country_of_residence", "linkedin_profile", "current_ctc", "status"]
            for field in updatable_fields:
                if kwargs.get(field) is not None:
                    candidate[field] = kwargs[field]
            
            candidate["updated_at"] = "2025-01-01T12:00:00"
            
            return json.dumps({"success": True, "candidate_id": kwargs["candidate_id"], "message": f"Candidate {kwargs['candidate_id']} updated successfully"})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_candidate_operations",
                "description": "Manage candidate profile operations in the HR talent management system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation",
                            "enum": ["create_candidate", "update_candidate"]
                        },
                        "first_name": {"type": "string", "description": "First name (required for create_candidate)"},
                        "last_name": {"type": "string", "description": "Last name (required for create_candidate)"},
                        "email_address": {"type": "string", "description": "Email address (required for create_candidate)"},
                        "contact_number": {"type": "string", "description": "Contact number (required for create_candidate)"},
                        "country_of_residence": {"type": "string", "description": "Country of residence (required for create_candidate)"},
                        "created_by": {"type": "string", "description": "User ID who created candidate (required for create_candidate)"},
                        "resume_file_name": {"type": "string", "description": "Resume file name (required for create_candidate)"},
                        "source_of_application": {"type": "string", "description": "Source of application (optional for create_candidate)"},
                        "linkedin_profile": {"type": "string", "description": "LinkedIn profile URL (optional)"},
                        "current_ctc": {"type": "number", "description": "Current CTC (optional)"},
                        "candidate_id": {"type": "string", "description": "Candidate ID (required for update_candidate)"},
                        "user_id": {"type": "string", "description": "User ID (required for update_candidate)"},
                        "status": {"type": "string", "description": "Candidate status (optional for update_candidate)"}
                    },
                    "required": ["operation_type"]
                }
            }
        }

