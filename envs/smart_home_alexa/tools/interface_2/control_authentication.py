import json
import random
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ControlAuthentication(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, user_id: str = None, authentication_method: str = None, verification_code: str = None, operation_data: Dict[str, Any] = None) -> str:
        """
        Manage multi-factor authentication and verification in the smart home management system.
        Handles MFA enablement, verification code generation and validation, backup code creation,
        and verification delivery for SMS and authenticator app methods.
        """
        
        # Validate operation type
        valid_operations = ["enable_mfa", "generate_verification_code", "validate_code", "generate_backup_codes", "send_verification"]
        if operation not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be one of: {', '.join(valid_operations)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # Get users table from schema
        users = data.get("users", {})
        
        # Validate user_id for operations that require it
        if operation in ["enable_mfa", "generate_verification_code", "validate_code", "generate_backup_codes", "send_verification"]:
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: user_id required for {operation} operation"
                })
            
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: User not found - user_id '{user_id}' does not exist"
                })
        
        user = users.get(user_id) if user_id else None
        
        if operation == "generate_verification_code":
            # Generate a verification code for MFA setup
            if not authentication_method:
                return json.dumps({
                    "success": False,
                    "error": "Halt: authentication_method required for generate_verification_code operation"
                })
            
            # Validate authentication method
            valid_methods = ["SMS", "authenticator_app"]
            if authentication_method not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid authentication_method '{authentication_method}'. Must be one of: {', '.join(valid_methods)}"
                })
            
            # Generate 6-digit verification code
            verification_code_generated = str(random.randint(100000, 999999))
            
            # Store verification code temporarily (in real implementation, this would be cached with expiration)
            verification_session = {
                "user_id": user_id,
                "verification_code": verification_code_generated,
                "authentication_method": authentication_method,
                "generated_at": "2025-10-16T14:30:00",
                "expires_at": "2025-10-16T14:40:00",
                "attempts_remaining": 3
            }
            
            return json.dumps({
                "success": True,
                "operation": "generate_verification_code",
                "user_id": user_id,
                "user_name": user.get("name"),
                "authentication_method": authentication_method,
                "verification_code": verification_code_generated,
                "verification_session": verification_session,
                "message": f"Verification code generated for {authentication_method} method"
            })
        
        elif operation == "send_verification":
            # Send verification code to user via specified method
            if not authentication_method:
                return json.dumps({
                    "success": False,
                    "error": "Halt: authentication_method required for send_verification operation"
                })
            
            valid_methods = ["SMS", "authenticator_app"]
            if authentication_method not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid authentication_method '{authentication_method}'. Must be one of: {', '.join(valid_methods)}"
                })
            
            delivery_status = {}
            
            if authentication_method == "SMS":
                phone_number = user.get("phone")
                if not phone_number:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: User phone number not found - cannot send SMS verification"
                    })
                
                # Simulate SMS delivery
                delivery_status = {
                    "method": "SMS",
                    "destination": phone_number,
                    "delivery_status": "sent",
                    "sent_at": "2025-10-16T14:30:00"
                }
            
            elif authentication_method == "authenticator_app":
                email = user.get("email")
                
                # For authenticator app, provide QR code setup instructions
                delivery_status = {
                    "method": "authenticator_app",
                    "setup_method": "QR_code",
                    "email_notification": email,
                    "instructions": "Scan QR code with authenticator app (Google Authenticator, Authy, etc.)",
                    "delivery_status": "ready",
                    "generated_at": "2025-10-16T14:30:00"
                }
            
            return json.dumps({
                "success": True,
                "operation": "send_verification",
                "user_id": user_id,
                "user_name": user.get("name"),
                "authentication_method": authentication_method,
                "delivery_status": delivery_status,
                "message": f"Verification sent via {authentication_method}"
            })
        
        elif operation == "validate_code":
            # Validate user-provided verification code
            if not verification_code:
                return json.dumps({
                    "success": False,
                    "error": "Halt: verification_code required for validate_code operation"
                })
            
            # Simulate verification code validation
            # In real implementation, this would check against stored session
            expected_code = "123456"  # Simulated expected code
            attempts_remaining = 2
            
            if verification_code != expected_code:
                if attempts_remaining > 0:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Verification code incorrect - {attempts_remaining} attempts remaining"
                    })
                else:
                    return json.dumps({
                        "success": False,
                        "error": "Halt: Verification code incorrect after 3 attempts - please generate new code"
                    })
            
            return json.dumps({
                "success": True,
                "operation": "validate_code",
                "user_id": user_id,
                "user_name": user.get("name"),
                "verification_status": "valid",
                "validated_at": "2025-10-16T14:31:00",
                "message": "Verification code validated successfully"
            })
        
        elif operation == "generate_backup_codes":
            # Generate backup codes for MFA recovery
            if not operation_data:
                operation_data = {}
            
            count = operation_data.get("count", 10)
            
            if not isinstance(count, int) or count < 1 or count > 20:
                return json.dumps({
                    "success": False,
                    "error": "Halt: count must be an integer between 1 and 20"
                })
            
            # Generate backup codes (8-character alphanumeric)
            backup_codes = []
            for i in range(count):
                code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
                backup_codes.append(code)
            
            # Store backup codes in user record (as JSON array)
            user["mfa_backup_codes"] = json.dumps(backup_codes)
            
            return json.dumps({
                "success": True,
                "operation": "generate_backup_codes",
                "user_id": user_id,
                "user_name": user.get("name"),
                "backup_codes": backup_codes,
                "codes_generated": count,
                "generated_at": "2025-10-16T14:31:00",
                "message": f"Generated {count} backup codes - store these securely"
            })
        
        elif operation == "enable_mfa":
            # Enable MFA on user account
            if not authentication_method:
                return json.dumps({
                    "success": False,
                    "error": "Halt: authentication_method required for enable_mfa operation"
                })
            
            valid_methods = ["SMS", "authenticator_app"]
            if authentication_method not in valid_methods:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid authentication_method '{authentication_method}'. Must be one of: {', '.join(valid_methods)}"
                })
            
            # Check if MFA already enabled
            if user.get("mfa_enabled"):
                return json.dumps({
                    "success": False,
                    "error": f"Halt: MFA already enabled for user '{user_id}' with method '{user.get('mfa_method')}'"
                })
            
            # Enable MFA on user account
            user["mfa_enabled"] = True
            user["mfa_method"] = authentication_method
            user["updated_date"] = "2025-10-16T14:31:00"
            
            return json.dumps({
                "success": True,
                "operation": "enable_mfa",
                "user_id": user_id,
                "user_name": user.get("name"),
                "email": user.get("email"),
                "mfa_enabled": True,
                "mfa_method": authentication_method,
                "enabled_at": "2025-10-16T14:31:00",
                "message": f"MFA enabled successfully using {authentication_method} method"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "control_authentication",
                "description": "Manage multi-factor authentication and verification in the smart home management system. Handles MFA enablement workflow including verification code generation for SMS or authenticator app methods , code delivery and validation with attempt tracking, backup code generation for account recovery, and MFA activation on user accounts. Supports both SMS-based and authenticator app-based two-factor authentication. Validates phone numbers for SMS delivery and provides QR code setup for authenticator apps.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Authentication operation to perform",
                            "enum": ["enable_mfa", "generate_verification_code", "validate_code", "generate_backup_codes", "send_verification"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user (required for all operations)"
                        },
                        "authentication_method": {
                            "type": "string",
                            "description": "MFA method: SMS or authenticator_app (required for enable_mfa, generate_verification_code, send_verification)",
                            "enum": ["SMS", "authenticator_app"]
                        },
                        "verification_code": {
                            "type": "string",
                            "description": "6-digit verification code to validate (required for validate_code)"
                        },
                        "operation_data": {
                            "type": "object",
                            "description": "Operation-specific parameters. For generate_backup_codes: {count} (default: 10, max: 20)",
                            "properties": {
                                "count": {
                                    "type": "integer",
                                    "description": "Number of backup codes to generate (1-20, default: 10)"
                                }
                            }
                        }
                    },
                    "required": ["operation"]
                }
            }
        }