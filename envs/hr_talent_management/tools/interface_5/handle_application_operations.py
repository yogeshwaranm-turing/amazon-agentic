import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class HandleApplicationOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage application operations including creation and status updates.
        
        Operations:
        - create_application: Create new job application
        - update_application_status: Update application status
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Accept both MM-DD-YYYY and YYYY-MM-DD formats
                date_pattern_1 = r'^\d{2}-\d{2}-\d{4}$'
                date_pattern_2 = r'^\d{4}-\d{2}-\d{2}$'
                if not (re.match(date_pattern_1, date_str) or re.match(date_pattern_2, date_str)):
                    return f"Invalid {field_name} format. Must be MM-DD-YYYY or YYYY-MM-DD"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert MM-DD-YYYY to YYYY-MM-DD"""
            if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                month, day, year = date_str.split('-')
                return f"{year}-{month}-{day}"
            return date_str
        
        # Validate operation_type
        valid_operations = ["create_application", "update_application_status"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "application_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "application_id": None,
                "message": "Invalid data format for application operations"
            })
        
        applications = data.get("applications", {})
        candidates = data.get("candidates", {})
        job_postings = data.get("job_postings", {})
        documents = data.get("documents", {})
        users = data.get("users", {})
        
        if operation_type == "create_application":
            # Validate required fields
            required_fields = ["created_by", "candidate_id", "posting_id", "resume_file_id", "application_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Missing required fields for application creation: {', '.join(missing_fields)}"
                })
            
            # Validate creator exists
            if str(kwargs["created_by"]) not in users:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"User {kwargs['created_by']} not found"
                })
            
            # Validate candidate exists and is active
            cand_id = str(kwargs["candidate_id"])
            if cand_id not in candidates:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Candidate {cand_id} not found"
                })
            
            candidate = candidates[cand_id]
            if candidate.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Candidate {cand_id} is not active"
                })
            
            # Validate posting exists and is active
            posting_id = str(kwargs["posting_id"])
            if posting_id not in job_postings:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Job posting {posting_id} not found"
                })
            
            posting = job_postings[posting_id]
            if posting.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Job posting {posting_id} is not active"
                })
            
            # Validate resume file exists
            resume_file_id = str(kwargs["resume_file_id"])
            if resume_file_id not in documents:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Resume file {resume_file_id} not found"
                })
            
            # Validate cover letter file if provided
            if "cover_letter_file_id" in kwargs and kwargs["cover_letter_file_id"]:
                cover_letter_id = str(kwargs["cover_letter_file_id"])
                if cover_letter_id not in documents:
                    return json.dumps({
                        "success": False,
                        "application_id": None,
                        "message": f"Cover letter file {cover_letter_id} not found"
                    })
            
            # Check for duplicate application (candidate already applied to this posting)
            for app_id, app in applications.items():
                if app.get("candidate_id") == cand_id and app.get("posting_id") == posting_id:
                    return json.dumps({
                        "success": False,
                        "application_id": None,
                        "message": f"Candidate {cand_id} has already applied to posting {posting_id}"
                    })
            
            # Validate date format
            date_error = validate_date_format(kwargs["application_date"], "application_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": date_error
                })
            
            # Generate new application ID and create record
            new_application_id = generate_id(applications)
            timestamp = "2025-10-10T12:00:00"
            
            new_application = {
                "application_id": app_id,
                "candidate_id": kwargs["candidate_id"],
                "posting_id": kwargs["posting_id"],
                "resume_file_id": kwargs["resume_file_id"],
                "cover_letter_file_id": kwargs.get("cover_letter_file_id"),
                "application_date": kwargs["application_date"],
                "status": "applied",
                "screened_by": None,
                "screened_date": None,
                "shortlist_approved_by": None,
                "shortlist_approval_date": None,
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00"
            }
            
            applications[str(new_application_id)] = new_application
            
            return json.dumps({
                "success": True,
                "application_id": str(new_application_id),
                "message": f"Application {new_application_id} created successfully"
            })
        
        elif operation_type == "update_application_status":
            # Validate required fields
            required_fields = ["application_id", "status", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "application_id": None,
                    "message": f"Missing required fields for application status update: {', '.join(missing_fields)}"
                })
            
            # Validate application exists
            app_id = str(kwargs["application_id"])
            if app_id not in applications:
                return json.dumps({
                    "success": False,
                    "application_id": app_id,
                    "message": f"Application {app_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "application_id": app_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            application = applications[app_id]
            
            # Validate status
            valid_statuses = ["pending_review", "incomplete", "screening_passed", "shortlisted", 
                            "interview_scheduled", "interview_completed", "selected", "rejected", 
                            "offer_issued", "offer_accepted", "onboarding"]
            if kwargs["status"] not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "application_id": app_id,
                    "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                })
            
            # Update status
            application["status"] = kwargs["status"]
            
            # Update optional fields if provided
            if "screened_date" in kwargs and kwargs["screened_date"]:
                date_error = validate_date_format(kwargs["screened_date"], "screened_date")
                if date_error:
                    return json.dumps({
                        "success": False,
                        "application_id": app_id,
                        "message": date_error
                    })
                application["screened_date"] = convert_date_format(kwargs["screened_date"])
                application["screened_by"] = str(kwargs["user_id"])
            
            if "shortlist_approval_date" in kwargs and kwargs["shortlist_approval_date"]:
                date_error = validate_date_format(kwargs["shortlist_approval_date"], "shortlist_approval_date")
                if date_error:
                    return json.dumps({
                        "success": False,
                        "application_id": app_id,
                        "message": date_error
                    })
                application["shortlist_approval_date"] = convert_date_format(kwargs["shortlist_approval_date"])
                application["shortlist_approved_by"] = str(kwargs["user_id"])
            
            return json.dumps({
                "success": True,
                "application_id": app_id,
                "message": f"Application {app_id} status updated to {kwargs['status']}"
            })
        
        return json.dumps({
            "success": False,
            "application_id": None,
            "message": "Operation not implemented"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_application_operations",
                "description": "Manage application operations including creation and status updates. Operations: create_application, update_application_status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_application', 'update_application_status'"
                        },
                        "created_by": {"type": "string", "description": "User ID who created application (required for create_application)"},
                        "candidate_id": {"type": "string", "description": "Candidate ID (required for create_application)"},
                        "posting_id": {"type": "string", "description": "Job posting ID (required for create_application)"},
                        "resume_file_id": {"type": "string", "description": "Resume file ID (required for create_application)"},
                        "cover_letter_file_id": {"type": "string", "description": "Cover letter file ID (optional for create_application)"},
                        "application_date": {"type": "string", "description": "Application date (required for create_application)"},
                        "user_id": {"type": "string", "description": "User ID (required for update_application_status)"},
                        "application_id": {"type": "string", "description": "Application ID (required for update_application_status and approve_shortlist)"},
                        "status": {"type": "string", "description": "Application status (required for update_application_status)"},
                        "screened_date": {"type": "string", "description": "Screened date (optional for update_application_status)"},
                        "approved_by": {"type": "string", "description": "Approver user ID (required for approve_shortlist)"},
                        "approval_date": {"type": "string", "description": "Approval date (required for approve_shortlist)"}
                    },
                    "required": ["operation_type"]
                }
            }
        }

