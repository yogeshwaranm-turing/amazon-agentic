import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageJobOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage job operations including requisitions and postings.
        
        Operations:
        - create_requisition: Create new job requisition
        - update_requisition: Update job requisition details
        - approve_requisition: Approve job requisition
        - create_posting: Create job posting from requisition
        - update_posting: Update job posting details
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
        valid_operations = ["create_requisition", "update_requisition", "approve_requisition", 
                          "create_posting", "update_posting"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "requisition_id": None,
                "posting_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "requisition_id": None,
                "posting_id": None,
                "message": "Invalid data format for job operations"
            })
        
        job_requisitions = data.get("job_requisitions", {})
        job_postings = data.get("job_postings", {})
        users = data.get("users", {})
        departments = data.get("departments", {})
        locations = data.get("locations", {})
        
        if operation_type == "create_requisition":
            # Validate required fields
            required_fields = ["job_title", "department_id", "location_id", "employment_type", 
                             "hiring_manager_id", "budgeted_salary_min", "budgeted_salary_max", "created_by"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Missing required fields for requisition creation: {', '.join(missing_fields)}"
                })
            
            # Validate user exists
            if str(kwargs["created_by"]) not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"User {kwargs['created_by']} not found"
                })
            
            # Validate department exists
            if str(kwargs["department_id"]) not in departments:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Department {kwargs['department_id']} not found"
                })
            
            # Validate location exists
            if str(kwargs["location_id"]) not in locations:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Location {kwargs['location_id']} not found"
                })
            
            # Validate hiring manager exists
            if str(kwargs["hiring_manager_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Hiring manager {kwargs['hiring_manager_id']} not found"
                })
            
            # Validate salary range
            try:
                min_salary = float(kwargs["budgeted_salary_min"])
                max_salary = float(kwargs["budgeted_salary_max"])
                if min_salary < 0 or max_salary < 0:
                    return json.dumps({
                        "success": False,
                        "requisition_id": None,
                        "message": "Salary values must be non-negative"
                    })
                if min_salary > max_salary:
                    return json.dumps({
                        "success": False,
                        "requisition_id": None,
                        "message": "Minimum salary cannot exceed maximum salary"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": "Invalid salary format"
                })
            
            # Validate employment type
            valid_employment_types = ["full_time", "part_time", "contract", "intern"]
            if kwargs["employment_type"] not in valid_employment_types:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Invalid employment_type. Must be one of: {', '.join(valid_employment_types)}"
                })
            
            # Generate new requisition ID and create record
            new_requisition_id = generate_id(job_requisitions)
            timestamp = "2025-10-10T12:00:00"
            
            new_requisition = {
                "requisition_id": str(new_requisition_id),
                "job_title": kwargs["job_title"],
                "department_id": str(kwargs["department_id"]),
                "location_id": str(kwargs["location_id"]),
                "employment_type": kwargs["employment_type"],
                "hiring_manager_id": str(kwargs["hiring_manager_id"]),
                "budgeted_salary_min": float(kwargs["budgeted_salary_min"]),
                "budgeted_salary_max": float(kwargs["budgeted_salary_max"]),
                "job_description": kwargs.get("job_description", ""),
                "grade": kwargs.get("grade", ""),
                "shift_type": kwargs.get("shift_type", ""),
                "remote_indicator": kwargs.get("remote_indicator", ""),
                "status": "draft",
                "created_by": str(kwargs["created_by"]),
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            job_requisitions[str(new_requisition_id)] = new_requisition
            
            return json.dumps({
                "success": True,
                "requisition_id": str(new_requisition_id),
                "message": f"Job requisition {new_requisition_id} created successfully"
            })
        
        elif operation_type == "update_requisition":
            # Validate required fields
            required_fields = ["requisition_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Missing required fields for requisition update: {', '.join(missing_fields)}"
                })
            
            # Validate requisition exists
            req_id = str(kwargs["requisition_id"])
            if req_id not in job_requisitions:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"Job requisition {req_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            requisition = job_requisitions[req_id]
            
            # If updating status, validate current status
            if "status" in kwargs and kwargs["status"] is not None:
                valid_statuses = ["draft", "pending_approval", "approved", "closed"]
                if kwargs["status"] not in valid_statuses:
                    return json.dumps({
                        "success": False,
                        "requisition_id": req_id,
                        "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                    })
            else:
                # For non-status updates, check if requisition is in editable state
                if requisition.get("status") not in ["draft", "pending_approval"]:
                    return json.dumps({
                        "success": False,
                        "requisition_id": req_id,
                        "message": f"Cannot update requisition in '{requisition.get('status')}' status"
                    })
            
            # Update fields
            timestamp = "2025-10-10T12:00:00"
            updateable_fields = ["job_title", "department_id", "location_id", "employment_type", 
                               "hiring_manager_id", "budgeted_salary_min", "budgeted_salary_max",
                               "job_description", "grade", "shift_type", "remote_indicator", "status"]
            
            for field in updateable_fields:
                if field in kwargs and kwargs[field] is not None:
                    if field in ["department_id", "location_id", "hiring_manager_id"]:
                        requisition[field] = str(kwargs[field])
                    elif field in ["budgeted_salary_min", "budgeted_salary_max"]:
                        requisition[field] = float(kwargs[field])
                    else:
                        requisition[field] = kwargs[field]
            
            requisition["updated_at"] = timestamp
            
            return json.dumps({
                "success": True,
                "requisition_id": req_id,
                "message": f"Job requisition {req_id} updated successfully"
            })
        
        elif operation_type == "approve_requisition":
            # Validate required fields
            required_fields = ["requisition_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "requisition_id": None,
                    "message": f"Missing required fields for requisition approval: {', '.join(missing_fields)}"
                })
            
            # Validate requisition exists
            req_id = str(kwargs["requisition_id"])
            if req_id not in job_requisitions:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"Job requisition {req_id} not found"
                })
            
            # Validate user exists
            user_id = str(kwargs["user_id"])
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"User {user_id} not found"
                })
            
            requisition = job_requisitions[req_id]
            user = users[user_id]
            user_role = user.get("role", "")
            
            # Validate requisition status
            if requisition.get("status") != "pending_approval":
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"Cannot approve requisition in '{requisition.get('status')}' status"
                })
            
            # Determine approval type based on user role
            approval_date = kwargs.get("approval_date", "2025-10-10")
            approval_date_converted = convert_date_format(approval_date)
            
            if user_role == "hr_manager":
                requisition["hr_manager_approver"] = user_id
                requisition["hr_manager_approval_date"] = approval_date_converted
            elif user_role == "finance_manager":
                requisition["finance_manager_approver"] = user_id
                requisition["finance_manager_approval_date"] = approval_date_converted
            elif user_role == "department_manager" or user_role == "hiring_manager":
                requisition["dept_head_approver"] = user_id
                requisition["dept_head_approval_date"] = approval_date_converted
            else:
                return json.dumps({
                    "success": False,
                    "requisition_id": req_id,
                    "message": f"User with role '{user_role}' is not authorized to approve requisitions"
                })
            
            requisition["updated_at"] = "2025-10-10T12:00:00"
            
            return json.dumps({
                "success": True,
                "requisition_id": req_id,
                "message": f"Job requisition {req_id} approved by {user_role}"
            })
        
        elif operation_type == "create_posting":
            # Validate required fields
            required_fields = ["requisition_id", "posted_date", "portal_type", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Missing required fields for posting creation: {', '.join(missing_fields)}"
                })
            
            # Validate requisition exists
            req_id = str(kwargs["requisition_id"])
            if req_id not in job_requisitions:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Job requisition {req_id} not found"
                })
            
            requisition = job_requisitions[req_id]
            
            # Validate requisition is approved
            if requisition.get("status") != "approved":
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Cannot create posting for requisition in '{requisition.get('status')}' status"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate portal type
            valid_portal_types = ["internal", "external", "both"]
            if kwargs["portal_type"] not in valid_portal_types:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Invalid portal_type. Must be one of: {', '.join(valid_portal_types)}"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["posted_date"], "posted_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": date_error
                })
            
            # Generate new posting ID and create record
            new_posting_id = generate_id(job_postings)
            timestamp = "2025-10-10T12:00:00"
            
            new_posting = {
                "posting_id": str(new_posting_id),
                "requisition_id": req_id,
                "posted_date": convert_date_format(kwargs["posted_date"]),
                "portal_type": kwargs["portal_type"],
                "status": "active",
                "created_at": timestamp
            }
            
            job_postings[str(new_posting_id)] = new_posting
            
            return json.dumps({
                "success": True,
                "posting_id": str(new_posting_id),
                "message": f"Job posting {new_posting_id} created successfully"
            })
        
        elif operation_type == "update_posting":
            # Validate required fields
            required_fields = ["posting_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "posting_id": None,
                    "message": f"Missing required fields for posting update: {', '.join(missing_fields)}"
                })
            
            # Validate posting exists
            posting_id = str(kwargs["posting_id"])
            if posting_id not in job_postings:
                return json.dumps({
                    "success": False,
                    "posting_id": posting_id,
                    "message": f"Job posting {posting_id} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "posting_id": posting_id,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            posting = job_postings[posting_id]
            
            # Validate posting is in updatable status
            if posting.get("status") != "active":
                return json.dumps({
                    "success": False,
                    "posting_id": posting_id,
                    "message": f"Cannot update posting in '{posting.get('status')}' status"
                })
            
            # Update fields
            updateable_fields = ["portal_type", "status"]
            
            for field in updateable_fields:
                if field in kwargs and kwargs[field] is not None:
                    if field == "portal_type":
                        valid_portal_types = ["internal", "external", "both"]
                        if kwargs[field] not in valid_portal_types:
                            return json.dumps({
                                "success": False,
                                "posting_id": posting_id,
                                "message": f"Invalid portal_type. Must be one of: {', '.join(valid_portal_types)}"
                            })
                    elif field == "status":
                        valid_statuses = ["active", "closed", "archived"]
                        if kwargs[field] not in valid_statuses:
                            return json.dumps({
                                "success": False,
                                "posting_id": posting_id,
                                "message": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                            })
                    posting[field] = kwargs[field]
            
            return json.dumps({
                "success": True,
                "posting_id": posting_id,
                "message": f"Job posting {posting_id} updated successfully"
            })
        
        return json.dumps({
            "success": False,
            "requisition_id": None,
            "posting_id": None,
            "message": "Operation not implemented"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_job_operations",
                "description": "Manage job operations including requisitions and postings. Operations: create_requisition, update_requisition, approve_requisition, create_posting, update_posting.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_requisition', 'update_requisition', 'approve_requisition', 'create_posting', 'update_posting'"
                        },
                        "requisition_id": {
                            "type": "string",
                            "description": "Required for update_requisition, approve_requisition. Optional for create_posting"
                        },
                        "posting_id": {
                            "type": "string",
                            "description": "Required for update_posting"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Required for all operations except create_requisition where created_by is used"
                        },
                        "job_title": {
                            "type": "string",
                            "description": "Required for create_requisition"
                        },
                        "department_id": {
                            "type": "string",
                            "description": "Required for create_requisition"
                        },
                        "location_id": {
                            "type": "string",
                            "description": "Required for create_requisition"
                        },
                        "employment_type": {
                            "type": "string",
                            "description": "Required for create_requisition. Values: full_time, part_time, contract, intern"
                        },
                        "hiring_manager_id": {
                            "type": "string",
                            "description": "Required for create_requisition"
                        },
                        "budgeted_salary_min": {
                            "type": "number",
                            "description": "Required for create_requisition"
                        },
                        "budgeted_salary_max": {
                            "type": "number",
                            "description": "Required for create_requisition"
                        },
                        "created_by": {
                            "type": "string",
                            "description": "Required for create_requisition"
                        },
                        "posted_date": {
                            "type": "string",
                            "description": "Required for create_posting. Format: MM-DD-YYYY or YYYY-MM-DD"
                        },
                        "portal_type": {
                            "type": "string",
                            "description": "Required for create_posting. Values: internal, external, both"
                        },
                        "status": {
                            "type": "string",
                            "description": "Optional for update operations"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }

