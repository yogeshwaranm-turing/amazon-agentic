import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool


class ManageInterviewOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage interview operations including scheduling, panel management, and evaluation.
        
        Operations:
        - schedule_interview: Schedule an interview for a shortlisted candidate
        - add_panel_member: Add a panel member to an interview
        - conduct_evaluation: Record interview evaluation and feedback
        """
        
        def generate_id(table: Dict[str, Any]) -> str:
            if not table:
                return "1"
            return str(max(int(k) for k in table.keys()) + 1)
        
        valid_operations = ["schedule_interview", "add_panel_member", "conduct_evaluation"]
        
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for interview operations"
            })
        
        interviews = data.get("interviews", {})
        interview_panel_members = data.get("interview_panel_members", {})
        applications = data.get("applications", {})
        users = data.get("users", {})
        
        # SCHEDULE INTERVIEW
        if operation_type == "schedule_interview":
            required_fields = ["application_id", "interview_type", "scheduled_date", "user_id"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify user has appropriate role
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            if user.get("role") not in ["hr_recruiter", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "error": "Halt: User lacks appropriate role authorization"})
            
            # Verify application exists and is shortlisted
            application = applications.get(kwargs["application_id"])
            if not application:
                return json.dumps({"success": False, "error": "Halt: Application not found"})
            
            if application.get("status") != "shortlisted":
                return json.dumps({"success": False, "error": "Halt: Application not shortlisted"})
            
            # Create interview
            interview_id = generate_id(interviews)
            new_interview = {
                "interview_id": interview_id,
                "application_id": kwargs["application_id"],
                "interview_type": kwargs["interview_type"],
                "scheduled_date": kwargs["scheduled_date"],
                "interview_status": "scheduled",
                "rating": None,
                "recommendation": None,
                "completed_by": None,
                "completed_date": None,
                "created_at": "2025-01-01T12:00:00",
                "updated_at": "2025-01-01T12:00:00"
            }
            interviews[interview_id] = new_interview
            
            return json.dumps({"success": True, "interview_id": interview_id, "message": f"Interview {interview_id} scheduled successfully"})
        
        # ADD PANEL MEMBER
        elif operation_type == "add_panel_member":
            required_fields = ["interview_id", "panel_member_id", "user_id"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify user has appropriate role
            user = users.get(kwargs["user_id"])
            if not user or user.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: User not found or inactive"})
            
            if user.get("role") not in ["hr_recruiter", "hr_manager", "hr_admin"]:
                return json.dumps({"success": False, "error": "Halt: User not authorized"})
            
            # Verify interview exists and is scheduled
            interview = interviews.get(kwargs["interview_id"])
            if not interview or interview.get("interview_status") != "scheduled":
                return json.dumps({"success": False, "error": "Halt: Interview not found or not in 'scheduled' status"})
            
            # Verify panel member exists and is active
            panel_member = users.get(kwargs["panel_member_id"])
            if not panel_member or panel_member.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Panel member not found or is inactive"})
            
            # Check for duplicate panel member
            for member in interview_panel_members.values():
                if member.get("interview_id") == kwargs["interview_id"] and member.get("user_id") == kwargs["panel_member_id"]:
                    return json.dumps({"success": False, "error": "Halt: Duplicate panel member assignment"})
            
            # Add panel member
            member_id = generate_id(interview_panel_members)
            new_member = {
                "panel_member_id": member_id,
                "interview_id": kwargs["interview_id"],
                "user_id": kwargs["panel_member_id"],
                "created_at": "2025-01-01T12:00:00"
            }
            interview_panel_members[member_id] = new_member
            
            return json.dumps({"success": True, "panel_member_id": member_id, "message": f"Panel member added to interview {kwargs['interview_id']} successfully"})
        
        # CONDUCT EVALUATION
        elif operation_type == "conduct_evaluation":
            required_fields = ["interview_id", "rating", "recommendation", "completed_by", "completed_date"]
            missing = [f for f in required_fields if not kwargs.get(f)]
            if missing:
                return json.dumps({"success": False, "error": f"Halt: Missing mandatory fields: {', '.join(missing)}"})
            
            # Verify interview exists and is scheduled
            interview = interviews.get(kwargs["interview_id"])
            if not interview or interview.get("interview_status") != "scheduled":
                return json.dumps({"success": False, "error": "Halt: Interview not found or not in 'scheduled' status"})
            
            # Verify completed_by user exists and is active
            evaluator = users.get(kwargs["completed_by"])
            if not evaluator or evaluator.get("employment_status") != "active":
                return json.dumps({"success": False, "error": "Halt: Evaluator not found or inactive"})
            
            # Verify evaluator is a panel member
            is_panel_member = False
            for member in interview_panel_members.values():
                if member.get("interview_id") == kwargs["interview_id"] and member.get("user_id") == kwargs["completed_by"]:
                    is_panel_member = True
                    break
            
            if not is_panel_member:
                return json.dumps({"success": False, "error": "Halt: Evaluator not authorized for this interview"})
            
            # Validate rating (1-5 scale)
            rating = int(kwargs["rating"])
            if rating < 1 or rating > 5:
                return json.dumps({"success": False, "error": "Halt: Invalid rating (not 1-5 scale)"})
            
            # Record evaluation
            interview["rating"] = rating
            interview["recommendation"] = kwargs["recommendation"]
            interview["completed_by"] = kwargs["completed_by"]
            interview["completed_date"] = kwargs["completed_date"]
            interview["interview_status"] = "completed"
            interview["updated_at"] = "2025-01-01T12:00:00"
            
            return json.dumps({"success": True, "interview_id": kwargs["interview_id"], "message": f"Interview {kwargs['interview_id']} evaluation recorded successfully"})
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_interview_operations",
                "description": "Manage interview operations in the HR talent management system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation",
                            "enum": ["schedule_interview", "add_panel_member", "conduct_evaluation"]
                        },
                        "application_id": {"type": "string", "description": "Application ID (required for schedule_interview)"},
                        "interview_type": {"type": "string", "description": "Interview type (required for schedule_interview)"},
                        "scheduled_date": {"type": "string", "description": "Scheduled date (required for schedule_interview)"},
                        "user_id": {"type": "string", "description": "User ID (required for schedule_interview and add_panel_member)"},
                        "interview_id": {"type": "string", "description": "Interview ID (required for add_panel_member and conduct_evaluation)"},
                        "panel_member_id": {"type": "string", "description": "Panel member user ID (required for add_panel_member)"},
                        "rating": {"type": "integer", "description": "Interview rating 1-5 (required for conduct_evaluation)"},
                        "recommendation": {"type": "string", "description": "Interview recommendation (required for conduct_evaluation)"},
                        "completed_by": {"type": "string", "description": "Evaluator user ID (required for conduct_evaluation)"},
                        "completed_date": {"type": "string", "description": "Completion date (required for conduct_evaluation)"}
                    },
                    "required": ["operation_type"]
                }
            }
        }

