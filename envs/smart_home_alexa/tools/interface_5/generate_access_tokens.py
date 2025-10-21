import json
import random
import string
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GenerateAccessTokens(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], code_type: str, generation_parameters: Dict[str, Any] = None) -> str:
        """
        Generate access codes and identifiers in the smart home management system.
        Handles guest access code generation for temporary user access and backup identifier
        generation for system configuration backups.
        """
        
        # Validate code_type
        valid_types = ["guest_access", "backup_identifier"]
        if code_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid code_type '{code_type}'. Must be one of: {', '.join(valid_types)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        # Get generation parameters
        if not generation_parameters:
            generation_parameters = {}
        
        if code_type == "guest_access":
            # Generate guest access code (10-character alphanumeric as per schema)
            code_length = 10
            
            # Generate alphanumeric code (excluding ambiguous characters like 0, O, I, l)
            safe_chars = ''.join(set(string.ascii_uppercase + string.digits) - set('0OIL'))
            guest_access_code = ''.join(random.choices(safe_chars, k=code_length))
            
            # Get users table to check for duplicates
            users = data.get("users", {})
            
            # Check if generated code already exists (very unlikely but important)
            max_attempts = 10
            attempts = 0
            while attempts < max_attempts:
                code_exists = False
                for user_id, user in users.items():
                    if user.get("guest_access_code") == guest_access_code:
                        code_exists = True
                        break
                
                if not code_exists:
                    break
                
                # Regenerate if duplicate found
                guest_access_code = ''.join(random.choices(safe_chars, k=code_length))
                attempts += 1
            
            if attempts >= max_attempts:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Failed to generate unique guest access code after 10 attempts"
                })
            
            return json.dumps({
                "success": True,
                "code_type": "guest_access",
                "guest_access_code": guest_access_code,
                "code_length": code_length,
                "generated_at": "2025-10-16T14:30:00",
                "message": f"Guest access code generated: {guest_access_code}"
            })
        
        elif code_type == "backup_identifier":
            # Generate unique backup identifier
            timestamp = generation_parameters.get("timestamp")
            
            if not timestamp:
                # Use current timestamp if not provided
                timestamp = "2025-10-16T14:30:00"
            
            # Parse timestamp to create identifier components
            # Format: backup_YYYYMMDD_HHMMSS_XXXX (random suffix)
            timestamp_clean = timestamp.replace("-", "").replace(":", "").replace("T", "_")[:15]
            
            # Generate 4-character random suffix for uniqueness
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            
            backup_id = f"backup_{timestamp_clean}_{random_suffix}"
            
            # Get backups table to check for duplicates
            backups = data.get("backups", {})
            
            # Check if generated backup_id already exists
            max_attempts = 10
            attempts = 0
            while backup_id in backups and attempts < max_attempts:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                backup_id = f"backup_{timestamp_clean}_{random_suffix}"
                attempts += 1
            
            if attempts >= max_attempts:
                return json.dumps({
                    "success": False,
                    "error": "Halt: Failed to generate unique backup identifier after 10 attempts"
                })
            
            return json.dumps({
                "success": True,
                "code_type": "backup_identifier",
                "backup_id": backup_id,
                "timestamp": timestamp,
                "generated_at": "2025-10-16T14:30:00",
                "message": f"Backup identifier generated: {backup_id}"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "generate_access_tokens",
                "description": "Generate access codes and identifiers in the smart home management system. Handles guest access code generation for temporary user access  using fixed 10-character alphanumeric codes and backup identifier generation for system configuration backups , using timestamp-based identifiers with random suffixes. Excludes ambiguous characters (0, O, I, L) from guest codes for clarity.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code_type": {
                            "type": "string",
                            "description": "Type of code or identifier to generate",
                            "enum": ["guest_access", "backup_identifier"]
                        },
                        "generation_parameters": {
                            "type": "object",
                            "description": "Code generation parameters. For backup_identifier: {timestamp} (optional, defaults to current time). Not used for guest_access.",
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "description": "Timestamp for backup identifier (YYYY-MM-DDTHH:MM:SS format, defaults to current time)"
                                }
                            }
                        }
                    },
                    "required": ["code_type"]
                }
            }
        }