import json
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool


class ManageApplicationOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage application operations including creation, status updates, and shortlist approval.
        
        Operations:
        - create_application: Create a new job application
        - update_application_status: Update application status
        - approve_shortlist: Approve candidate for shortlist
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        valid_operations = ["create_application", "update_application_status", "approve_shortlist"]
        
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for application operations"
            })
        
        applications = data.get("applications", {})
        candidates = data.get("candidates", {})
        job_postings = data.get("job_postings", {})
        users = data.get("users", {})
        documents = data.get("documents", {})
        
        # CREATE APPLICATION
        if operation_type == "create_application":
            required_fields = ["user_id", "posting_id", "resume_file_id", "application_date"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify user exists and is active
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            # Verify candidate profile exists for user
            candidate = None
            for cand in candidates.values():
                if cand.get("user_id") == kwargs["user_id"] and cand.get("status") == "active":
                    candidate = cand
                    break
            
            if not candidate:
                return json.dumps({"success": False, "error": "Halt: Candidate not found or inactive"})
            
            # Verify job posting exists and is active
            posting = job_postings.get(kwargs["posting_id"])
            if not posting or posting.get("status") != "active":
                return json.dumps({"success": False, "error": "Halt: Posting not found or not in 'active' status"})
            
            # Check for duplicate application
            for app in applications.values():
                if app.get("candidate_id") == candidate["candidate_id"] and app.get("posting_id") == kwargs["posting_id"]:
                    return json.dumps({"success": False, "error": "Halt: Duplicate application (candidate already applied to this posting)"})
            
            # Create application
            app_id = generate_id(applications)
            new_application = {
                "application_id": app_id,
                "candidate_id": candidate["candidate_id"],
                "posting_id": kwargs["posting_id"],
                "resume_file_id": kwargs["resume_file_id"],
                "cover_letter_file_id": kwargs.get("cover_letter_file_id"),
                "application_date": kwargs["application_date"],
                "status": "applied",
                "screened_by": None,
                "screened_date": None,
                "shortlist_approved_by": None,
                "shortlist_approval_date": None,
                "created_at": datetime.now().isoformat()
            }
            applications[app_id] = new_application
            
            return json.dumps({"success": True, "application_id": app_id, "message": f"Application {app_id} created successfully"})
        
        # UPDATE APPLICATION STATUS
        elif operation_type == "update_application_status":
            required_fields = ["application_id", "status", "user_id"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            application = applications.get(kwargs["application_id"])
            if not application:
                return json.dumps({"success": False, "error": "Halt: Application not found"})
            
            # Verify user has appropriate role
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            if user.get("role") not in ["hr_recruiter", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "error": "Halt: User lacks authorization to perform this action"})
            
            # Update status
            application["status"] = kwargs["status"]
            if kwargs.get("screened_date"):
                application["screened_date"] = kwargs["screened_date"]
                application["screened_by"] = kwargs["user_id"]
            
            return json.dumps({"success": True, "application_id": kwargs["application_id"], "message": f"Application {kwargs['application_id']} status updated successfully"})
        
        # APPROVE SHORTLIST
        elif operation_type == "approve_shortlist":
            required_fields = ["application_id", "approved_by", "approval_date"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            application = applications.get(kwargs["application_id"])
            if not application:
                return json.dumps({"success": False, "error": "Halt: Application not found"})
            
            if application.get("status") != "screening_passed":
                return json.dumps({"success": False, "error": "Halt: Application not in 'screening_passed' status"})
            
            # Verify approver is active HR manager
            approver = users.get(kwargs["approved_by"])
            if not approver or approver.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Approver not found or inactive"})
            
            if approver.get("role") != "hr_manager" and approver.get("role") != "hiring_manager":
                return json.dumps({"success": False, "error": "Halt: Approver not authorized (not an active hiring manager)"})
            
            # Approve shortlist
            application["shortlist_approved_by"] = kwargs["approved_by"]
            application["shortlist_approval_date"] = kwargs["approval_date"]
            application["status"] = "shortlisted"
            
            return json.dumps({"success": True, "application_id": kwargs["application_id"], "message": f"Application {kwargs['application_id']} shortlist approved"})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_application_operations",
                "description": "Manage job application operations in the HR talent management system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation",
                            "enum": ["create_application", "update_application_status", "approve_shortlist"]
                        },
                        "user_id": {"type": "string", "description": "User ID (required for create_application and update_application_status)"},
                        "posting_id": {"type": "string", "description": "Job posting ID (required for create_application)"},
                        "resume_file_id": {"type": "string", "description": "Resume file ID (required for create_application)"},
                        "cover_letter_file_id": {"type": "string", "description": "Cover letter file ID (optional for create_application)"},
                        "application_date": {"type": "string", "description": "Application date (required for create_application)"},
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

