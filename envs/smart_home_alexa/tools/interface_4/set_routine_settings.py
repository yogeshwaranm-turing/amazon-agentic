import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class SetRoutineSettings(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, routine_id: str, backup_data: Dict[str, Any] = None) -> str:
        """
        Backup and restore routine configurations in the smart home management system.
        Handles configuration preservation before modifications and restoration on failures.
        Supports schedule and trigger updates for routine modifications.
        """
        
        # Validate operation type
        valid_operations = ["backup", "restore", "update_schedule", "update_trigger"]
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
        
        # Get routines table from schema
        routines = data.get("routines", {})
        
        # Validate routine exists
        if routine_id not in routines:
            return json.dumps({
                "success": False,
                "error": f"Halt: Routine not found - routine_id '{routine_id}' does not exist"
            })
        
        routine = routines[routine_id]
        
        if operation == "backup":
            # Create complete backup of current routine configuration
            backup_config = {
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "routine_type": routine.get("routine_type"),
                "trigger_type": routine.get("trigger_type"),
                "trigger_value": routine.get("trigger_value"),
                "schedule_recurrence": routine.get("schedule_recurrence"),
                "seasonal_identifier": routine.get("seasonal_identifier"),
                "away_mode": routine.get("away_mode"),
                "security_mode": routine.get("security_mode"),
                "pin_required": routine.get("pin_required"),
                "device_actions": routine.get("device_actions"),
                "status": routine.get("status"),
                "backup_timestamp": "2025-10-16T14:30:00"
            }
            
            return json.dumps({
                "success": True,
                "operation": "backup",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "backup_data": backup_config,
                "message": f"Configuration backup created for routine '{routine.get('routine_name')}'"
            })
        
        elif operation == "restore":
            # Validate backup_data provided
            if not backup_data:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_data required for restore operation"
                })
            
            if not isinstance(backup_data, dict):
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_data must be a dictionary"
                })
            
            # Validate backup_data contains routine_id
            if backup_data.get("routine_id") != routine_id:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: backup_data routine_id mismatch - expected '{routine_id}', got '{backup_data.get('routine_id')}'"
                })
            
            # Store previous values for audit
            previous_config = {
                "trigger_type": routine.get("trigger_type"),
                "trigger_value": routine.get("trigger_value"),
                "schedule_recurrence": routine.get("schedule_recurrence"),
                "device_actions": routine.get("device_actions")
            }
            
            # Restore configuration fields from backup
            restorable_fields = [
                "routine_name", "routine_type", "trigger_type", "trigger_value",
                "schedule_recurrence", "seasonal_identifier", "away_mode",
                "security_mode", "pin_required", "device_actions", "status"
            ]
            
            restored_fields = []
            for field in restorable_fields:
                if field in backup_data:
                    routine[field] = backup_data[field]
                    restored_fields.append(field)
            
            # Update metadata
            routine["updated_date"] = "2025-10-16T14:30:00"
            
            return json.dumps({
                "success": True,
                "operation": "restore",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "restored_fields": restored_fields,
                "previous_config": previous_config,
                "message": f"Configuration restored for routine '{routine.get('routine_name')}' from backup"
            })
        
        elif operation == "update_schedule":
            # Validate backup_data contains new_schedule
            if not backup_data:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_data with new_schedule required for update_schedule operation"
                })
            
            new_schedule = backup_data.get("new_schedule")
            if not new_schedule:
                return json.dumps({
                    "success": False,
                    "error": "Halt: new_schedule field required in backup_data"
                })
            
            # Validate schedule_recurrence value
            valid_recurrences = ["daily", "weekdays", "weekends", "specific_dates", "seasonal", "once"]
            if new_schedule not in valid_recurrences:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid schedule_recurrence '{new_schedule}'. Must be one of: {', '.join(valid_recurrences)}"
                })
            
            # Store previous value
            previous_schedule = routine.get("schedule_recurrence")
            
            # Update schedule
            routine["schedule_recurrence"] = new_schedule
            routine["updated_date"] = "2025-10-16T14:30:00"
            
            return json.dumps({
                "success": True,
                "operation": "update_schedule",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "previous_schedule": previous_schedule,
                "new_schedule": new_schedule,
                "message": f"Schedule updated for routine '{routine.get('routine_name')}' from '{previous_schedule}' to '{new_schedule}'"
            })
        
        elif operation == "update_trigger":
            # Validate backup_data contains trigger configuration
            if not backup_data:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_data with trigger configuration required for update_trigger operation"
                })
            
            new_trigger_type = backup_data.get("new_trigger_type")
            new_trigger_value = backup_data.get("new_trigger_value")
            
            if not new_trigger_type:
                return json.dumps({
                    "success": False,
                    "error": "Halt: new_trigger_type field required in backup_data"
                })
            
            # Validate trigger_type value
            valid_triggers = ["time", "location", "manual", "sensor", "voice"]
            if new_trigger_type not in valid_triggers:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid trigger_type '{new_trigger_type}'. Must be one of: {', '.join(valid_triggers)}"
                })
            
            # Store previous values
            previous_trigger_type = routine.get("trigger_type")
            previous_trigger_value = routine.get("trigger_value")
            
            # Update trigger configuration
            routine["trigger_type"] = new_trigger_type
            if new_trigger_value is not None:
                routine["trigger_value"] = new_trigger_value
            routine["updated_date"] = "2025-10-16T14:30:00"
            
            return json.dumps({
                "success": True,
                "operation": "update_trigger",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "previous_trigger": {
                    "type": previous_trigger_type,
                    "value": previous_trigger_value
                },
                "new_trigger": {
                    "type": new_trigger_type,
                    "value": new_trigger_value
                },
                "message": f"Trigger updated for routine '{routine.get('routine_name')}' from '{previous_trigger_type}' to '{new_trigger_type}'"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_routine_settings",
                "description": "Backup and restore routine configurations in the smart home management system. Creates configuration snapshots before modifications to enable rollback on test failures. Supports schedule and trigger updates for routine modifications. (Modify Comfort Automation),  (Modify Security Automation),  (Modify Awareness Automation), and (Diagnose Routine Execution Failures). Ensures safe configuration changes with rollback capability.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Configuration operation to perform",
                            "enum": ["backup", "restore", "update_schedule", "update_trigger"]
                        },
                        "routine_id": {
                            "type": "string",
                            "description": "Unique identifier of the routine to manage"
                        },
                        "backup_data": {
                            "type": "object",
                            "description": "Configuration data for restore/update operations. For restore: full backup object. For update_schedule: {new_schedule}. For update_trigger: {new_trigger_type, new_trigger_value}",
                            "properties": {
                                "routine_id": {
                                    "type": "string",
                                    "description": "Routine identifier (for restore validation)"
                                },
                                "new_schedule": {
                                    "type": "string",
                                    "description": "New schedule recurrence value (for update_schedule)"
                                },
                                "new_trigger_type": {
                                    "type": "string",
                                    "description": "New trigger type (for update_trigger)"
                                },
                                "new_trigger_value": {
                                    "type": "string",
                                    "description": "New trigger value (for update_trigger)"
                                }
                            }
                        }
                    },
                    "required": ["operation", "routine_id"]
                }
            }
        }