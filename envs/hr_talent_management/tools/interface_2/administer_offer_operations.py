import json
import re
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class AdministerOfferOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, **kwargs) -> str:
        """
        Manage job offer operations including creation, benefits, compliance, approval, issuance, and acceptance.
        
        Operations:
        - create_offer: Create new offer (requires candidate_id, requisition_id, position, start_date, base_salary, reporting_manager_id, user_id)
        - add_benefit: Add benefit to offer (requires offer_id, benefit_type, benefit_description)
        - verify_compliance: Verify compliance approval (requires offer_id, compliance_approved_by, compliance_approval_date)
        - approve_offer: Approve offer (requires offer_id, hr_manager_approved_by, hr_manager_approval_date)
        - issue_offer: Issue offer (requires offer_id, user_id, issue_date)
        - record_acceptance: Record offer acceptance (requires offer_id, acceptance_date, offer_accepted_date)
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        def validate_date_format(date_str: str, field_name: str) -> Optional[str]:
            if date_str:
                # Convert MM-DD-YYYY to YYYY-MM-DD for internal storage
                date_pattern = r'^\d{2}-\d{2}-\d{4}$'
                if not re.match(date_pattern, date_str):
                    return f"Invalid {field_name} format. Must be MM-DD-YYYY"
            return None
        
        def convert_date_format(date_str: str) -> str:
            """Convert MM-DD-YYYY to YYYY-MM-DD"""
            if date_str and re.match(r'^\d{2}-\d{2}-\d{4}$', date_str):
                month, day, year = date_str.split('-')
                return f"{year}-{month}-{day}"
            return date_str
        
        # Validate operation_type
        valid_operations = ["create_offer", "add_benefit", "verify_compliance", "approve_offer", "issue_offer", "record_acceptance"]
        if operation_type not in valid_operations:
            return json.dumps({
                "success": False,
                "offer_id": None,
                "message": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        # Access related data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "offer_id": None,
                "message": "Invalid data format for offer operations"
            })
        
        offers = data.get("offers", {})
        offer_benefits = data.get("offer_benefits", {})
        candidates = data.get("candidates", {})
        users = data.get("users", {})
        
        if operation_type == "create_offer":
            # Validate required fields for offer creation
            required_fields = ["candidate_id", "requisition_id", "position", "start_date", "base_salary", "reporting_manager_id", "user_id"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Missing required fields for offer creation: {', '.join(missing_fields)}"
                })
            
            # Validate candidate exists
            if str(kwargs["candidate_id"]) not in candidates:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Candidate {kwargs['candidate_id']} not found"
                })
            
            # Validate user exists
            if str(kwargs["user_id"]) not in users:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"User {kwargs['user_id']} not found"
                })
            
            # Validate base_salary is positive
            try:
                base_salary = float(kwargs["base_salary"])
                if base_salary <= 0:
                    return json.dumps({
                        "success": False,
                        "offer_id": None,
                        "message": "Base salary must be positive"
                    })
            except (ValueError, TypeError):
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": "Invalid base_salary format"
                })
            
            # Validate optional numeric fields
            optional_numeric_fields = ["stock_options_amount", "signing_bonus_amount", "relocation_allowance_amount"]
            for field in optional_numeric_fields:
                if field in kwargs and kwargs[field] is not None:
                    try:
                        value = float(kwargs[field])
                        if value < 0:
                            return json.dumps({
                                "success": False,
                                "offer_id": None,
                                "message": f"{field} must be non-negative"
                            })
                    except (ValueError, TypeError):
                        return json.dumps({
                            "success": False,
                            "offer_id": None,
                            "message": f"Invalid {field} format"
                        })
            
            # Validate date format
            date_error = validate_date_format(kwargs["start_date"], "start_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": date_error
                })
            
            # Generate new offer ID and create record
            new_offer_id = generate_id(offers)
            timestamp = "2025-10-01T12:00:00"
            
            new_offer = {
                "offer_id": str(new_offer_id),
                "candidate_id": str(kwargs["candidate_id"]),
                "requisition_id": str(kwargs["requisition_id"]),
                "position": kwargs["position"],
                "start_date": convert_date_format(kwargs["start_date"]),
                "base_salary": float(kwargs["base_salary"]),
                "stock_options_amount": float(kwargs.get("stock_options_amount", 0)),
                "signing_bonus_amount": float(kwargs.get("signing_bonus_amount", 0)),
                "relocation_allowance_amount": float(kwargs.get("relocation_allowance_amount", 0)),
                "reporting_manager_id": str(kwargs["reporting_manager_id"]),
                "offer_status": "draft",
                "created_at": timestamp,
                "updated_at": timestamp
            }
            
            offers[str(new_offer_id)] = new_offer
            
            return json.dumps({
                "success": True,
                "offer_id": str(new_offer_id),
                "message": f"Offer {new_offer_id} created successfully"
            })
        
        elif operation_type == "add_benefit":
            # Validate required fields for adding benefit
            required_fields = ["offer_id", "benefit_type", "benefit_description"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Missing required fields for adding benefit: {', '.join(missing_fields)}"
                })
            
            # Validate offer exists
            if str(kwargs["offer_id"]) not in offers:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Offer {kwargs['offer_id']} not found"
                })
            
            # Generate new benefit ID and create record
            new_benefit_id = generate_id(offer_benefits)
            timestamp = "2025-10-01T12:00:00"
            
            new_benefit = {
                "benefit_id": str(new_benefit_id),
                "offer_id": str(kwargs["offer_id"]),
                "benefit_type": kwargs["benefit_type"],
                "benefit_description": kwargs["benefit_description"],
                "created_at": timestamp
            }
            
            offer_benefits[str(new_benefit_id)] = new_benefit
            
            return json.dumps({
                "success": True,
                "offer_id": str(kwargs["offer_id"]),
                "message": f"Benefit {new_benefit_id} added to offer {kwargs['offer_id']} successfully"
            })
        
        elif operation_type == "verify_compliance":
            # Validate required fields for compliance verification
            required_fields = ["offer_id", "compliance_approved_by", "compliance_approval_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Missing required fields for compliance verification: {', '.join(missing_fields)}"
                })
            
            # Validate offer exists
            if str(kwargs["offer_id"]) not in offers:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Offer {kwargs['offer_id']} not found"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["compliance_approval_date"], "compliance_approval_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": date_error
                })
            
            # Update offer with compliance approval
            offer = offers[str(kwargs["offer_id"])]
            offer["compliance_approved_by"] = str(kwargs["compliance_approved_by"])
            offer["compliance_approval_date"] = convert_date_format(kwargs["compliance_approval_date"])
            offer["updated_at"] = "2025-10-01T12:00:00"
            
            return json.dumps({
                "success": True,
                "offer_id": str(kwargs["offer_id"]),
                "message": f"Compliance verification completed for offer {kwargs['offer_id']}"
            })
        
        elif operation_type == "approve_offer":
            # Validate required fields for offer approval
            required_fields = ["offer_id", "hr_manager_approved_by", "hr_manager_approval_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Missing required fields for offer approval: {', '.join(missing_fields)}"
                })
            
            # Validate offer exists
            if str(kwargs["offer_id"]) not in offers:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Offer {kwargs['offer_id']} not found"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["hr_manager_approval_date"], "hr_manager_approval_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": date_error
                })
            
            # Update offer with HR manager approval
            offer = offers[str(kwargs["offer_id"])]
            offer["hr_manager_approved_by"] = str(kwargs["hr_manager_approved_by"])
            offer["hr_manager_approval_date"] = convert_date_format(kwargs["hr_manager_approval_date"])
            offer["offer_status"] = "approved_for_issue"
            offer["updated_at"] = "2025-10-01T12:00:00"
            
            return json.dumps({
                "success": True,
                "offer_id": str(kwargs["offer_id"]),
                "message": f"Offer {kwargs['offer_id']} approved successfully"
            })
        
        elif operation_type == "issue_offer":
            # Validate required fields for offer issuance
            required_fields = ["offer_id", "user_id", "issue_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Missing required fields for offer issuance: {', '.join(missing_fields)}"
                })
            
            # Validate offer exists
            if str(kwargs["offer_id"]) not in offers:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Offer {kwargs['offer_id']} not found"
                })
            
            # Validate date format
            date_error = validate_date_format(kwargs["issue_date"], "issue_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": date_error
                })
            
            # Update offer with issuance details
            offer = offers[str(kwargs["offer_id"])]
            offer["issue_date"] = convert_date_format(kwargs["issue_date"])
            offer["offer_status"] = "issued"
            offer["updated_at"] = "2025-10-01T12:00:00"
            
            return json.dumps({
                "success": True,
                "offer_id": str(kwargs["offer_id"]),
                "message": f"Offer {kwargs['offer_id']} issued successfully"
            })
        
        elif operation_type == "record_acceptance":
            # Validate required fields for recording acceptance
            required_fields = ["offer_id", "acceptance_date", "offer_accepted_date"]
            missing_fields = [field for field in required_fields if field not in kwargs or kwargs[field] is None]
            if missing_fields:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Missing required fields for recording acceptance: {', '.join(missing_fields)}"
                })
            
            # Validate offer exists
            if str(kwargs["offer_id"]) not in offers:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": f"Offer {kwargs['offer_id']} not found"
                })
            
            # Validate date formats
            date_error = validate_date_format(kwargs["acceptance_date"], "acceptance_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": date_error
                })
            
            date_error = validate_date_format(kwargs["offer_accepted_date"], "offer_accepted_date")
            if date_error:
                return json.dumps({
                    "success": False,
                    "offer_id": None,
                    "message": date_error
                })
            
            # Update offer with acceptance details
            offer = offers[str(kwargs["offer_id"])]
            offer["acceptance_date"] = convert_date_format(kwargs["acceptance_date"])
            offer["offer_accepted_date"] = convert_date_format(kwargs["offer_accepted_date"])
            offer["offer_status"] = "accepted"
            offer["updated_at"] = "2025-10-01T12:00:00"
            
            return json.dumps({
                "success": True,
                "offer_id": str(kwargs["offer_id"]),
                "message": f"Offer acceptance recorded for offer {kwargs['offer_id']}"
            })
        
        return json.dumps({
            "success": False,
            "offer_id": None,
            "message": "Unhandled operation type"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_offer_operations",
                "description": "Manage job offer operations including creation, benefits, compliance, approval, issuance, and acceptance. This tool handles the complete offer lifecycle from initial creation through final acceptance. For creation, establishes new offer records with comprehensive validation of candidate and user existence, positive salary requirements, and proper date formatting. For benefits, adds additional compensation and benefit details to existing offers. For compliance and approval, records necessary authorization steps with proper date tracking. For issuance, marks offers as officially sent to candidates. For acceptance, records candidate acceptance with complete audit trail. Essential for talent acquisition workflow management, compliance tracking, and offer administration.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of operation to perform: 'create_offer' to establish new offer record, 'add_benefit' to add benefit to offer, 'verify_compliance' to record compliance approval, 'approve_offer' to record HR manager approval, 'issue_offer' to mark offer as issued, 'record_acceptance' to record candidate acceptance",
                            "enum": ["create_offer", "add_benefit", "verify_compliance", "approve_offer", "issue_offer", "record_acceptance"]
                        },
                        "candidate_id": {
                            "type": "string",
                            "description": "Unique identifier of the candidate (required for create_offer only, must exist in system)"
                        },
                        "requisition_id": {
                            "type": "string",
                            "description": "Unique identifier of the job requisition (required for create_offer only)"
                        },
                        "position": {
                            "type": "string",
                            "description": "Job position title (required for create_offer only)"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Proposed start date in MM-DD-YYYY format (required for create_offer only)"
                        },
                        "base_salary": {
                            "type": "number",
                            "description": "Base salary amount (required for create_offer only, must be positive)"
                        },
                        "reporting_manager_id": {
                            "type": "string",
                            "description": "Unique identifier of the reporting manager (required for create_offer only)"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user performing the operation (required for create_offer and issue_offer, must exist in system)"
                        },
                        "stock_options_amount": {
                            "type": "number",
                            "description": "Stock options amount (optional for create_offer, must be non-negative)"
                        },
                        "signing_bonus_amount": {
                            "type": "number",
                            "description": "Signing bonus amount (optional for create_offer, must be non-negative)"
                        },
                        "relocation_allowance_amount": {
                            "type": "number",
                            "description": "Relocation allowance amount (optional for create_offer, must be non-negative)"
                        },
                        "offer_id": {
                            "type": "string",
                            "description": "Unique identifier of the offer (required for add_benefit, verify_compliance, approve_offer, issue_offer, and record_acceptance, must exist in system)"
                        },
                        "benefit_type": {
                            "type": "string",
                            "description": "Type of benefit being added (required for add_benefit only)"
                        },
                        "benefit_description": {
                            "type": "string",
                            "description": "Description of the benefit being added (required for add_benefit only)"
                        },
                        "compliance_approved_by": {
                            "type": "string",
                            "description": "User ID of compliance approver (required for verify_compliance only)"
                        },
                        "compliance_approval_date": {
                            "type": "string",
                            "description": "Date of compliance approval in MM-DD-YYYY format (required for verify_compliance only)"
                        },
                        "hr_manager_approved_by": {
                            "type": "string",
                            "description": "User ID of HR manager approver (required for approve_offer only)"
                        },
                        "hr_manager_approval_date": {
                            "type": "string",
                            "description": "Date of HR manager approval in MM-DD-YYYY format (required for approve_offer only)"
                        },
                        "issue_date": {
                            "type": "string",
                            "description": "Date offer was issued in MM-DD-YYYY format (required for issue_offer only)"
                        },
                        "acceptance_date": {
                            "type": "string",
                            "description": "Date candidate accepted offer in MM-DD-YYYY format (required for record_acceptance only)"
                        },
                        "offer_accepted_date": {
                            "type": "string",
                            "description": "Date offer acceptance was recorded in MM-DD-YYYY format (required for record_acceptance only)"
                        }
                    },
                    "required": ["operation_type"]
                }
            }
        }
