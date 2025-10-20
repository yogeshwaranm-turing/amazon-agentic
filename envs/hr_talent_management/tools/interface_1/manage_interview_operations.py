import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ManageInterviewOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage interview operations including scheduling, panel management, and evaluation.
        
        Operations:
        - schedule_interview: Schedule new interview
        - add_panel_member: Add panel member to interview
        - conduct_evaluation: Record interview evaluation
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
        
        def is_date_in_past(date_str: str, current_date: str = "2025-01-01") -> bool:
            """Check if a date is in the past compared to current_date"""
            # Convert both dates to YYYY-MM-DD format for comparison
            date_normalized = convert_date_format(date_str)
            current_normalized = convert_date_format(current_date)
            return date_normalized < current_normalized
        
        # Validate operation_type
        valid_operations = ["schedule_interview", "add_panel_member", "conduct_evaluation"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "interview_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "interview_id": None,
                "message": "Invalid data format for interview operations"
            })
        
        interviews = data.get("interviews", {})
        interview_panel_members = data.get("interview_panel_members", {})
        applications = data.get("applications", {})
        users = data.get("users", {})
        
        if operation_type == "schedule_interview":
            # Validate required fields
            required_fields = ["application_id", "interview_type", "scheduled_date", "panel_member_ids", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Missing mandatory fields ({', '.join(missing_fields)})"
                })
            
            # Validate user exists, is active, and has appropriate role
            user_id_str = str(kwargs["user_id"])
            if user_id_str not in users:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Operation failed due to system errors"
                })
            
            user = users[user_id_str]
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Operation failed due to system errors"
                })
            
            valid_user_roles = ["hr_recruiter", "hr_manager", "hr_director", "hr_admin"]
            if user.get("role") not in valid_user_roles:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Operation failed due to system errors"
                })
            
            # Validate application exists and is shortlisted
            app_id = str(kwargs["application_id"])
            if app_id not in applications:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Application not found or not shortlisted"
                })
            
            application = applications[app_id]
            if application.get("status") != "shortlisted":
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Application not found or not shortlisted"
                })
            
            # Validate interview type
            valid_interview_types = ["technical", "hr", "panel", "final"]
            if kwargs["interview_type"] not in valid_interview_types:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Halt: Invalid interview_type"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["scheduled_date"], "scheduled_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": date_error
                })
            
            # Validate scheduled date is not in the past
            if is_date_in_past(kwargs["scheduled_date"]):
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": "Halt: Scheduled date in the past"
                })
            
            # Validate panel members exist and are active
            panel_member_ids = kwargs["panel_member_ids"]
            if not isinstance(panel_member_ids, list):
                panel_member_ids = [panel_member_ids]
            
            for panel_member_id in panel_member_ids:
                if str(panel_member_id) not in users:
                    return json.dumps({
                        "success": False,
                        "interview_id": None,
                        "message": f"Panel member {panel_member_id} not found"
                    })
                panel_user = users[str(panel_member_id)]
                if panel_user.get("employment_status") != "active":
                    return json.dumps({
                        "success": False,
                        "interview_id": None,
                        "message": f"Panel member {panel_member_id} is not active"
                    })
            
            # Generate new interview ID and create record
            new_interview_id = generate_id(interviews)
            timestamp = "2025-10-10T12:00:00"
            
            new_interview = {
                "interview_id": str(new_interview_id),
                "application_id": app_id,
                "interview_type": kwargs["interview_type"],
                "scheduled_date": convert_date_format(kwargs["scheduled_date"]),
                "interview_status": "scheduled",
                "created_at": timestamp
            }
            
            interviews[str(new_interview_id)] = new_interview
            
            # Add panel members
            for panel_member_id in panel_member_ids:
                new_panel_member_id = generate_id(interview_panel_members)
                new_panel_member = {
                    "panel_member_id": str(new_panel_member_id),
                    "interview_id": str(new_interview_id),
                    "user_id": str(panel_member_id),
                    "created_at": timestamp
                }
                interview_panel_members[str(new_panel_member_id)] = new_panel_member
            
            return json.dumps({
                "success": True,
                "interview_id": str(new_interview_id),
                "message": f"Interview {new_interview_id} scheduled successfully with {len(panel_member_ids)} panel member(s)"
            })
        
        elif operation_type == "add_panel_member":
            # Validate required fields
            required_fields = ["interview_id", "panel_member_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Missing required fields for adding panel member: {', '.join(missing_fields)}"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate interview exists and is in scheduled status
            interview_id = str(kwargs["interview_id"])
            if interview_id not in interviews:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Interview {interview_id} not found"
                })
            
            interview = interviews[interview_id]
            if interview.get("interview_status") != "scheduled":
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Cannot add panel member to interview in '{interview.get('interview_status')}' status"
                })
            
            # Validate panel member exists and is active
            panel_member_id = str(kwargs["panel_member_id"])
            if panel_member_id not in users:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Panel member {panel_member_id} not found"
                })
            
            panel_user = users[panel_member_id]
            if panel_user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Panel member {panel_member_id} is not active"
                })
            
            # Check if panel member is already assigned
            for pm_id, pm in interview_panel_members.items():
                if pm.get("interview_id") == interview_id and pm.get("user_id") == panel_member_id:
                    return json.dumps({
                        "success": False,
                        "interview_id": interview_id,
                        "message": f"Panel member {panel_member_id} is already assigned to this interview"
                    })
            
            # Add panel member
            new_panel_member_id = generate_id(interview_panel_members)
            timestamp = "2025-10-10T12:00:00"
            
            new_panel_member = {
                "panel_member_id": str(new_panel_member_id),
                "interview_id": interview_id,
                "user_id": panel_member_id,
                "created_at": timestamp
            }
            
            interview_panel_members[str(new_panel_member_id)] = new_panel_member
            
            return json.dumps({
                "success": True,
                "interview_id": interview_id,
                "message": f"Panel member {panel_member_id} added to interview {interview_id}"
            })
        
        elif operation_type == "conduct_evaluation":
            # Validate required fields
            required_fields = ["interview_id", "rating", "recommendation", "completed_by", "completed_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "interview_id": None,
                    "message": f"Missing required fields for interview evaluation: {', '.join(missing_fields)}"
                })
            
            # Validate interview exists
            interview_id = str(kwargs["interview_id"])
            if interview_id not in interviews:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Interview {interview_id} not found"
                })
            
            interview = interviews[interview_id]
            
            # Validate interview is in scheduled status
            if interview.get("interview_status") != "scheduled":
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Cannot evaluate interview in '{interview.get('interview_status')}' status"
                })
            
            # Validate completed_by user exists and is active
            completed_by = str(kwargs["completed_by"])
            if completed_by not in users:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"User {completed_by} not found"
                })
            
            user = users[completed_by]
            if user.get("employment_status") != "active":
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"User {completed_by} is not active"
                })
            
            # Verify completed_by is a panel member for this interview
            is_panel_member = False
            for pm_id, pm in interview_panel_members.items():
                if pm.get("interview_id") == interview_id and pm.get("user_id") == completed_by:
                    is_panel_member = True
                    break
            
            if not is_panel_member:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"User {completed_by} is not a panel member for this interview"
                })
            
            # Validate rating
            try:
                rating = int(kwargs["rating"])
                if rating < 1 or rating > 5:
                    return json.dumps({
                        "success": False,
                        "interview_id": interview_id,
                        "message": "Rating must be between 1 and 5"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": "Invalid rating format"
                })
            
            # Validate recommendation
            valid_recommendations = ["yes", "no", "maybe"]
            if kwargs["recommendation"] not in valid_recommendations:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": f"Invalid recommendation. Must be one of: {', '.join(valid_recommendations)}"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["completed_date"], "completed_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "interview_id": interview_id,
                    "message": date_error
                })
            
            # Update interview with evaluation
            interview["rating"] = rating
            interview["recommendation"] = kwargs["recommendation"]
            interview["completed_by"] = completed_by
            interview["completed_date"] = convert_date_format(kwargs["completed_date"])
            interview["interview_status"] = "completed"
            
            return json.dumps({
                "success": True,
                "interview_id": interview_id,
                "message": f"Interview {interview_id} evaluation recorded successfully"
            })
        
        return json.dumps({
            "success": False,
            "interview_id": None,
            "message": "Operation not implemented"
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_interview_operations",
                "description": """Manage interview scheduling, panel assignments, and evaluation recording throughout the interview process.

OPERATION 1: schedule_interview - Schedule a new interview for a shortlisted candidate application
Required: application_id (string), interview_type (string), scheduled_date (string, format: MM-DD-YYYY or YYYY-MM-DD), panel_member_ids (array of user ID strings), user_id (string)
Valid interview_type values: technical, hr, panel, final
Note: User must be active HR Recruiter, HR Manager, HR Director, or HR Admin. Application must exist and be in 'shortlisted' status. Scheduled date cannot be in the past (must be >= 2025-01-01). All panel members must be active users. System auto-generates unique interview_id and automatically assigns all panel members to the interview. Returns interview_id.

OPERATION 2: add_panel_member - Add additional panel member to an existing scheduled interview
Required: interview_id (string), panel_member_id (user ID string), user_id (string)
Note: User must be active HR role. Interview must exist and be in 'scheduled' status. Panel member must be an active user and not already assigned to this interview. Prevents duplicate panel member assignments.

OPERATION 3: conduct_evaluation - Record interview evaluation and results
Required: interview_id (string), rating (integer 1-5), recommendation (string), completed_by (user ID string), completed_date (string, format: MM-DD-YYYY or YYYY-MM-DD)
Valid recommendation values: yes, no, maybe
Note: Interview must exist and be in 'scheduled' status. User (completed_by) must be an active user and must be assigned as a panel member for this specific interview. Rating must be between 1 and 5. Updates interview status to 'completed'.""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation: 'schedule_interview', 'add_panel_member', 'conduct_evaluation'"
                        },
                        "application_id": {
                            "type": "string",
                            "description": "ID of shortlisted application to schedule interview for (for schedule_interview)"
                        },
                        "interview_type": {
                            "type": "string",
                            "description": "Type of interview: technical, hr, panel, final (for schedule_interview)"
                        },
                        "scheduled_date": {
                            "type": "string",
                            "description": "Interview date MM-DD-YYYY or YYYY-MM-DD - cannot be in past (for schedule_interview)"
                        },
                        "panel_member_ids": {
                            "type": "array",
                            "description": "Array of user IDs for panel members - all will be auto-assigned to interview (for schedule_interview)",
                            "items": {
                                "type": "string"
                            }
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User performing the operation (for schedule_interview, add_panel_member)"
                        },
                        "interview_id": {
                            "type": "string",
                            "description": "ID of interview - NOTE: Auto-generated by schedule_interview, used for add_panel_member and conduct_evaluation"
                        },
                        "panel_member_id": {
                            "type": "string",
                            "description": "User ID of panel member to add - must be active and not already assigned (for add_panel_member)"
                        },
                        "rating": {
                            "type": "integer",
                            "description": "Interview rating 1-5 where 5 is best (for conduct_evaluation)"
                        },
                        "recommendation": {
                            "type": "string",
                            "description": "Hiring recommendation: yes, no, maybe (for conduct_evaluation)"
                        },
                        "completed_by": {
                            "type": "string",
                            "description": "User ID of panel member completing evaluation - must be assigned to this interview (for conduct_evaluation)"
                        },
                        "completed_date": {
                            "type": "string",
                            "description": "Date evaluation completed MM-DD-YYYY or YYYY-MM-DD (for conduct_evaluation)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }

