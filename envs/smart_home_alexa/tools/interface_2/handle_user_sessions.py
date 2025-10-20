import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleUserSessions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, user_id: str, session_parameters: Dict[str, Any] = None) -> str:
        """
        Manage user authentication sessions in the smart home management system.
        Handles session invalidation for security operations and voice profile training workflows.
        Supports MFA enablement session cleanup and voice training progress tracking.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate operation type
        valid_operations = ["invalidate", "start_voice_training", "wait_training_completion"]
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
        
        # Get relevant tables from schema
        users = data.get("users", {})
        voice_profiles = data.get("voice_profiles", {})
        
        # Validate user exists
        if user_id not in users:
            return json.dumps({
                "success": False,
                "error": f"Halt: User not found - user_id '{user_id}' does not exist"
            })
        
        user = users[user_id]
        
        if operation == "invalidate":

            # Get session parameters
            if not session_parameters:
                session_parameters = {}
            
            exclude_current = session_parameters.get("exclude_current", False)
            
            # Simulate session invalidation
            # In real implementation, this would clear session tokens/cookies
            invalidated_count = 3  # Simulated: assume user had 3 other sessions
            
            if exclude_current:
                message = f"All sessions invalidated for user '{user.get('name')}' except current session"
            else:
                message = f"All sessions invalidated for user '{user.get('name')}' including current session"
                invalidated_count += 1  # Include current session
            
            return json.dumps({
                "success": True,
                "operation": "invalidate",
                "user_id": user_id,
                "user_name": user.get("name"),
                "exclude_current": exclude_current,
                "sessions_invalidated": invalidated_count,
                "message": message
            })
        
        elif operation == "start_voice_training":
            # Initiate voice profile training session
            if not session_parameters:
                return json.dumps({
                    "success": False,
                    "error": "Halt: session_parameters required for start_voice_training operation"
                })
            
            profile_name = session_parameters.get("profile_name")
            training_phrases_count = session_parameters.get("training_phrases_count", 10)
            
            if not profile_name:
                return json.dumps({
                    "success": False,
                    "error": "Halt: profile_name required in session_parameters for voice training"
                })
            
            if not isinstance(training_phrases_count, int) or training_phrases_count < 1:
                return json.dumps({
                    "success": False,
                    "error": "Halt: training_phrases_count must be a positive integer"
                })
            
            # Check if user already has an active voice profile with same name
            existing_profile = None
            for profile_id, profile in voice_profiles.items():
                if profile.get("user_id") == user_id and profile.get("profile_name") == profile_name:
                    existing_profile = profile_id
                    break
            
            if existing_profile:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Voice profile '{profile_name}' already exists for user '{user_id}'"
                })
            
            # Generate training session ID
            training_session_id = f"train_session_{generate_id(voice_profiles)}"
         
            training_session = {
                "session_id": training_session_id,
                "user_id": user_id,
                "profile_name": profile_name,
                "training_phrases_count": training_phrases_count,
                "phrases_completed": 0,
                "status": "in_progress",
                "start_timestamp": "2025-10-16T14:30:00"
            }
            
            return json.dumps({
                "success": True,
                "operation": "start_voice_training",
                "user_id": user_id,
                "user_name": user.get("name"),
                "training_session_id": training_session_id,
                "profile_name": profile_name,
                "training_phrases_required": training_phrases_count,
                "training_session": training_session,
                "message": f"Voice training session started for profile '{profile_name}' - speak {training_phrases_count} phrases through Echo device"
            })
        
        elif operation == "wait_training_completion":
            # Wait for and verify voice training completion
            if not session_parameters:
                return json.dumps({
                    "success": False,
                    "error": "Halt: session_parameters required for wait_training_completion operation"
                })
            
            session_id = session_parameters.get("session_id")
            timeout_minutes = session_parameters.get("timeout_minutes", 3)
            
            if not session_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: session_id required in session_parameters for training completion check"
                })
            
            if not isinstance(timeout_minutes, (int, float)) or timeout_minutes <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: timeout_minutes must be a positive number"
                })
            
            # Simulate training completion check
            # In real implementation, this would poll for training status from Alexa service
            
            # Simulate successful training completion
            training_completed = True  # Simulated result
            training_quality_score = 0.85  # Simulated quality score (0.0 to 1.0)
            phrases_completed = 10
            
            if not training_completed:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Voice training not completed within {timeout_minutes} minutes timeout"
                })
            
            # Check quality score meets minimum threshold
            minimum_quality = 0.7
            if training_quality_score < minimum_quality:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Voice training quality insufficient - score {training_quality_score} below minimum {minimum_quality}"
                })
            
            return json.dumps({
                "success": True,
                "operation": "wait_training_completion",
                "user_id": user_id,
                "user_name": user.get("name"),
                "training_session_id": session_id,
                "training_completed": training_completed,
                "phrases_completed": phrases_completed,
                "training_quality_score": training_quality_score,
                "completion_timestamp": "2025-10-16T14:33:00",
                "elapsed_minutes": 3,
                "message": f"Voice training completed successfully with quality score {training_quality_score}"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_user_sessions",
                "description": "Handle user authentication sessions in the smart home management system. Handles session invalidation for security operations (e.g., after MFA enablement ), initiates voice profile training workflows for Alexa voice recognition, and waits for training completion with quality validation. Supports exclude_current parameter to preserve active session during invalidation, training phrase count configuration, and timeout handling for training completion.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Session management operation to perform",
                            "enum": ["invalidate", "start_voice_training", "wait_training_completion"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Unique identifier of the user"
                        },
                        "session_parameters": {
                            "type": "object",
                            "description": "Operation-specific parameters. For invalidate: {exclude_current}. For start_voice_training: {profile_name, training_phrases_count}. For wait_training_completion: {session_id, timeout_minutes}",
                            "properties": {
                                "exclude_current": {
                                    "type": "boolean",
                                    "description": "If true, preserves current session during invalidation (for invalidate)"
                                },
                                "profile_name": {
                                    "type": "string",
                                    "description": "Name for the voice profile being trained (for start_voice_training)"
                                },
                                "training_phrases_count": {
                                    "type": "integer",
                                    "description": "Number of training phrases required (default: 10, for start_voice_training)"
                                },
                                "session_id": {
                                    "type": "string",
                                    "description": "Training session identifier (for wait_training_completion)"
                                },
                                "timeout_minutes": {
                                    "type": "integer",
                                    "description": "Maximum wait time in minutes (default: 3, for wait_training_completion)"
                                }
                            }
                        }
                    },
                    "required": ["operation", "user_id"]
                }
            }
        }