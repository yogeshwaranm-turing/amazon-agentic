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
            # Validate required fields
            required_fields = ["first_name", "last_name", "email_address", "contact_number", 
                             "country_of_residence", "created_by", "resume_file_name"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "candidate_id": None,
                    "message": f"Missing required fields for candidate creation: {', '.join(missing_fields)}"
                })
            
            # Validate creator exists
            if str(kwargs["created_by"]) not in users:
                return json.dumps({
                    "success": False,
                    "candidate_id": None,
                    "message": f"User {kwargs['created_by']} not found"
                })
            
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, kwargs["email_address"]):
                return json.dumps({
                    "success": False,
                    "candidate_id": None,
                    "message": "Invalid email format"
                })
            
            # Check for duplicate email in existing candidates
            for cand_id, cand in candidates.items():
                user_id = cand.get("user_id")
                if user_id and str(user_id) in users:
                    existing_user = users[str(user_id)]
                    if existing_user.get("email") == kwargs["email_address"]:
                        return json.dumps({
                            "success": False,
                            "candidate_id": None,
                            "message": f"Candidate with email {kwargs['email_address']} already exists"
                        })
            
            # Check for duplicate contact number
            for cand_id, cand in candidates.items():
                user_id = cand.get("user_id")
                if user_id and str(user_id) in users:
                    existing_user = users[str(user_id)]
                    if existing_user.get("phone_number") == kwargs["contact_number"]:
                        return json.dumps({
                            "success": False,
                            "candidate_id": None,
                            "message": f"Candidate with contact number {kwargs['contact_number']} already exists"
                        })
            
            # Check for duplicate LinkedIn profile if provided
            if "linkedin_profile" in kwargs and kwargs["linkedin_profile"]:
                for cand_id, cand in candidates.items():
                    if cand.get("linkedin_profile") == kwargs["linkedin_profile"]:
                        return json.dumps({
                            "success": False,
                            "candidate_id": None,
                            "message": f"Candidate with LinkedIn profile {kwargs['linkedin_profile']} already exists"
                        })
            
            # Create user record first
            new_user_id = generate_id(users)
            timestamp = "2025-10-10T12:00:00"
            
            new_user = {
                "user_id": str(new_user_id),
                "first_name": kwargs["first_name"],
                "last_name": kwargs["last_name"],
                "email": kwargs["email_address"],
                "phone_number": kwargs["contact_number"],
                "role": "candidate",
                "employment_status": "active",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            users[str(new_user_id)] = new_user
            
            # Generate new candidate ID and create record
            new_candidate_id = generate_id(candidates)
            
            new_candidate = {
                "candidate_id": str(new_candidate_id),
                "user_id": str(new_user_id),
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
                "user_id": str(new_user_id),
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
                "description": "Manage candidate operations including creation and updates. Operations: create_candidate, update_candidate.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_candidate', 'update_candidate'"
                        },
                        "candidate_id": {
                            "type": "string",
                            "description": "Required for update_candidate"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Required for update_candidate"
                        },
                        "first_name": {
                            "type": "string",
                            "description": "Required for create_candidate"
                        },
                        "last_name": {
                            "type": "string",
                            "description": "Required for create_candidate"
                        },
                        "email_address": {
                            "type": "string",
                            "description": "Required for create_candidate"
                        },
                        "contact_number": {
                            "type": "string",
                            "description": "Required for create_candidate"
                        },
                        "country_of_residence": {
                            "type": "string",
                            "description": "Required for create_candidate. Optional for update_candidate"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Required for create_candidate"
                        },
                        "resume_file_name": {
                            "type": "string",
                            "description": "Required for create_candidate"
                        },
                        "linkedin_profile": {
                            "type": "string",
                            "description": "Optional for both operations"
                        },
                        "current_ctc": {
                            "type": "number",
                            "description": "Optional for both operations"
                        },
                        "status": {
                            "type": "string",
                            "description": "Optional for update_candidate. Values: active, inactive, suspended"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }

