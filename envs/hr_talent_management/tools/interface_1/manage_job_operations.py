import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ManageJobOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage job operations including requisition and posting management.
        
        Operations:
        - create_requisition: Create a new job requisition
        - update_requisition: Update an existing job requisition
        - approve_requisition: Approve a job requisition
        - create_posting: Create a job posting from approved requisition
        - update_posting: Update an existing job posting
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        valid_operations = ["create_requisition", "update_requisition", "approve_requisition", "create_posting", "update_posting"]
        
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for job operations"
            })
        
        job_requisitions = data.get("job_requisitions", {})
        job_postings = data.get("job_postings", {})
        users = data.get("users", {})
        departments = data.get("departments", {})
        locations = data.get("locations", {})
        
        # CREATE REQUISITION
        if operation_type == "create_requisition":
            required_fields = ["job_title", "department_id", "location_id", "employment_type", "hiring_manager_id", "budgeted_salary_min", "budgeted_salary_max", "created_by"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing required fields: {', '.join(missing)}"})
            
            # Verify user has appropriate role
            user = users.get(kwargs["created_by"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            valid_roles = ["hr_recruiter", "hr_manager", "hr_admin", "hr_director", "hiring_manager"]
            if user.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: User lacks appropriate role authorization"})
            
            # Verify department exists and is active
            dept = departments.get(kwargs["department_id"])
            if not dept or dept.get("status") != "active":
                return json.dumps({"success": False, "error": "Halt: Department not found or is not active"})
            
            # Verify location exists and is active
            loc = locations.get(kwargs["location_id"])
            if not loc or loc.get("status") != "active":
                return json.dumps({"success": False, "error": "Halt: Location not found or is not active"})
            
            # Verify hiring manager exists and is active
            hm = users.get(kwargs["hiring_manager_id"])
            if not hm or hm.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Hiring manager not found or inactive"})
            
            # Validate budget range (skip if values are invalid in data)
            try:
                if float(kwargs["budgeted_salary_min"]) > float(kwargs["budgeted_salary_max"]):
                    return json.dumps({"success": False, "error": "Halt: Invalid budget range (min > max)"})
            except (ValueError, TypeError):
                pass  # Allow invalid budget ranges as they exist in actual data
            
            # Create requisition
            req_id = generate_id(job_requisitions)
            new_req = {
                "requisition_id": req_id,
                "job_title": kwargs["job_title"],
                "department_id": kwargs["department_id"],
                "location_id": kwargs["location_id"],
                "employment_type": kwargs["employment_type"],
                "hiring_manager_id": kwargs["hiring_manager_id"],
                "budgeted_salary_min": float(kwargs["budgeted_salary_min"]),
                "budgeted_salary_max": float(kwargs["budgeted_salary_max"]),
                "job_description": kwargs.get("job_description"),
                "grade": kwargs.get("grade"),
                "shift_type": kwargs.get("shift_type"),
                "remote_indicator": kwargs.get("remote_indicator"),
                "status": "draft",
                "hr_manager_approver": None,
                "dept_head_approver": None,
                "hr_manager_approval_date": None,
                "dept_head_approval_date": None,
                "posted_date": None,
                "created_by": kwargs["created_by"],
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00"
            }
            job_requisitions[req_id] = new_req
            
            return json.dumps({"success": True, "requisition_id": req_id, "message": f"Job requisition {req_id} created successfully"})
        
        # UPDATE REQUISITION
        elif operation_type == "update_requisition":
            if not kwargs.get("requisition_id") or not kwargs.get("user_id"):
                return json.dumps({"success": False, "error": "Halt: Missing requisition_id or user_id"})
            
            req = job_requisitions.get(kwargs["requisition_id"])
            if not req:
                return json.dumps({"success": False, "error": "Halt: Requisition not found"})
            
            if req.get("status") not in ["draft", "pending_approval"]:
                return json.dumps({"success": False, "error": "Halt: Requisition not in updatable status"})
            
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            valid_roles = ["hr_recruiter", "hr_manager", "hr_admin", "hiring_manager"]
            if user.get("role") not in valid_roles:
                return json.dumps({"success": False, "error": "Halt: User lacks authorization to perform this action"})
            
            # Update fields if provided
            updatable_fields = ["job_title", "department_id", "location_id", "employment_type", "hiring_manager_id", 
                              "budgeted_salary_min", "budgeted_salary_max", "job_description", "grade", "shift_type", "remote_indicator"]
            for field in updatable_fields:
                if kwargs.get(field) is not None:
                    req[field] = kwargs[field]
            
            req["updated_at"] = "2025-01-01T12:00:00"
            
            return json.dumps({"success": True, "requisition_id": kwargs["requisition_id"], "message": f"Requisition {kwargs['requisition_id']} updated successfully"})
        
        # APPROVE REQUISITION
        elif operation_type == "approve_requisition":
            if not kwargs.get("requisition_id") or not kwargs.get("user_id"):
                return json.dumps({"success": False, "error": "Halt: Missing requisition_id or user_id"})
            
            req = job_requisitions.get(kwargs["requisition_id"])
            if not req:
                return json.dumps({"success": False, "error": "Halt: Requisition not found"})
            
            if req.get("status") != "pending_approval":
                return json.dumps({"success": False, "error": "Halt: Requisition not in pending approval status"})
            
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            approval_date = kwargs.get("approval_date", "2025-01-01")
            
            # Determine if HR Manager or Department Head
            if user.get("role") == "hr_manager":
                req["hr_manager_approver"] = kwargs["user_id"]
                req["hr_manager_approval_date"] = approval_date
            elif user.get("role") == "hiring_manager" or user.get("user_id") == req.get("hiring_manager_id"):
                req["dept_head_approver"] = kwargs["user_id"]
                req["dept_head_approval_date"] = approval_date
            else:
                return json.dumps({"success": False, "error": "Halt: Unauthorized approver (role mismatch)"})
            
            # Check if both approvals are complete
            if req.get("hr_manager_approver") and req.get("dept_head_approver"):
                req["status"] = "approved"
            
            req["updated_at"] = "2025-01-01T12:00:00"
            
            return json.dumps({"success": True, "requisition_id": kwargs["requisition_id"], "message": f"Requisition {kwargs['requisition_id']} approval recorded"})
        
        # CREATE POSTING
        elif operation_type == "create_posting":
            required_fields = ["requisition_id", "posted_date", "portal_type", "user_id"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing required fields: {', '.join(missing)}"})
            
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            if user.get("role") not in ["hr_recruiter", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "error": "Halt: User lacks appropriate role authorization"})
            
            req = job_requisitions.get(kwargs["requisition_id"])
            if not req or req.get("status") != "approved":
                return json.dumps({"success": False, "error": "Halt: Requisition not found or not in 'approved' status"})
            
            # Create posting
            posting_id = generate_id(job_postings)
            new_posting = {
                "posting_id": posting_id,
                "requisition_id": kwargs["requisition_id"],
                "posted_date": kwargs["posted_date"],
                "portal_type": kwargs["portal_type"],
                "status": "active",
                "closed_date": None,
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00"
            }
            job_postings[posting_id] = new_posting
            
            # Update requisition posted_date
            req["posted_date"] = kwargs["posted_date"]
            
            return json.dumps({"success": True, "posting_id": posting_id, "message": f"Job posting {posting_id} created successfully"})
        
        # UPDATE POSTING
        elif operation_type == "update_posting":
            if not kwargs.get("posting_id") or not kwargs.get("user_id"):
                return json.dumps({"success": False, "error": "Halt: Missing posting_id or user_id"})
            
            posting = job_postings.get(kwargs["posting_id"])
            if not posting:
                return json.dumps({"success": False, "error": "Halt: Posting not found"})
            
            if posting.get("status") != "active":
                return json.dumps({"success": False, "error": "Halt: Posting not in updatable status"})
            
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            if user.get("role") not in ["hr_recruiter", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "error": "Halt: User lacks authorization to perform this action"})
            
            # Update fields
            if kwargs.get("portal_type"):
                posting["portal_type"] = kwargs["portal_type"]
            if kwargs.get("status"):
                posting["status"] = kwargs["status"]
            
            posting["updated_at"] = "2025-01-01T12:00:00"
            
            return json.dumps({"success": True, "posting_id": kwargs["posting_id"], "message": f"Posting {kwargs['posting_id']} updated successfully"})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_job_operations",
                "description": "Manage job requisition and posting operations in the HR talent management system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation",
                            "enum": ["create_requisition", "update_requisition", "approve_requisition", "create_posting", "update_posting"]
                        },
                        "job_title": {"type": "string", "description": "Job title (required for create_requisition)"},
                        "department_id": {"type": "string", "description": "Department ID (required for create_requisition)"},
                        "location_id": {"type": "string", "description": "Location ID (required for create_requisition)"},
                        "employment_type": {"type": "string", "description": "Employment type (required for create_requisition)"},
                        "hiring_manager_id": {"type": "string", "description": "Hiring manager ID (required for create_requisition)"},
                        "budgeted_salary_min": {"type": "number", "description": "Minimum budgeted salary (required for create_requisition)"},
                        "budgeted_salary_max": {"type": "number", "description": "Maximum budgeted salary (required for create_requisition)"},
                        "created_by": {"type": "string", "description": "User ID creating requisition (required for create_requisition)"},
                        "job_description": {"type": "string", "description": "Job description (optional)"},
                        "grade": {"type": "string", "description": "Job grade (optional)"},
                        "shift_type": {"type": "string", "description": "Shift type (optional)"},
                        "remote_indicator": {"type": "string", "description": "Remote work indicator (optional)"},
                        "requisition_id": {"type": "string", "description": "Requisition ID (required for update/approve/create_posting)"},
                        "user_id": {"type": "string", "description": "User ID (required for update/approve/create_posting/update_posting)"},
                        "approval_date": {"type": "string", "description": "Approval date (optional for approve_requisition)"},
                        "posted_date": {"type": "string", "description": "Posted date (required for create_posting)"},
                        "portal_type": {"type": "string", "description": "Portal type (required for create_posting)"},
                        "posting_id": {"type": "string", "description": "Posting ID (required for update_posting)"},
                        "status": {"type": "string", "description": "Status (optional for update_posting)"}
                    },
                    "required": ["operation_type"]
                }
            }
        }

