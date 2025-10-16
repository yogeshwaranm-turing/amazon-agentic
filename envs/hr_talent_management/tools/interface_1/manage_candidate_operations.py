import json
from typing import Any, Dict
from datetime import datetime
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
            required_fields = ["user_id", "country_of_residence"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify user exists and is active
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            # Check for duplicate candidate (same user_id)
            for cand in candidates.values():
                if cand.get("user_id") == kwargs["user_id"]:
                    return json.dumps({"success": False, "error": "Halt: Duplicate candidate (user already has a candidate profile)"})
            
            # Create candidate
            cand_id = generate_id(candidates)
            timestamp = datetime.now().isoformat()
            new_candidate = {
                "candidate_id": cand_id,
                "user_id": kwargs["user_id"],
                "country_of_residence": kwargs["country_of_residence"],
                "linkedin_profile": kwargs.get("linkedin_profile"),
                "current_ctc": kwargs.get("current_ctc"),
                "status": "active",
                "created_at": timestamp,
                "updated_at": timestamp
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
            
            # Allow updates to candidates with any status (active, inactive, suspended)
            
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
            
            candidate["updated_at"] = datetime.now().isoformat()
            
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
                        "user_id": {"type": "string", "description": "User ID (required for create_candidate and update_candidate)"},
                        "country_of_residence": {"type": "string", "description": "Country of residence (required for create_candidate)"},
                        "linkedin_profile": {"type": "string", "description": "LinkedIn profile URL (optional)"},
                        "current_ctc": {"type": "number", "description": "Current CTC (optional)"},
                        "candidate_id": {"type": "string", "description": "Candidate ID (required for update_candidate)"},
                        "status": {"type": "string", "description": "Candidate status (optional for update_candidate)"}
                    },
                    "required": ["operation_type"]
                }
            }
        }

