import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class ArrangeUserOperation(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation_type: str, schedule_data: Dict[str, Any], user_id: str = None) -> str:
        """
        Schedule automatic user operations in the smart home management system.
        Handles scheduled user deactivation for guest access expiration, reminder scheduling
        for privacy reviews and maintenance tasks, and scheduled announcement delivery.
        """
        
        # Validate operation_type
        valid_types = ["user_deactivation", "reminder", "announcement"]
        if operation_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation_type '{operation_type}'. Must be one of: {', '.join(valid_types)}"
            })
        
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })
        
        if not schedule_data or not isinstance(schedule_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: schedule_data required and must be a dictionary"
            })
        
        # Get relevant tables from schema
        users = data.get("users", {})
        devices = data.get("devices", {})
        
        # Current datetime reference
        current_dt = datetime.now()
        current_datetime = current_dt.strftime("%Y-%m-%dT%H:%M:%S")
        
        if operation_type == "user_deactivation":
            # Schedule automatic user deactivation (for guest access expiration)
            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: user_id required for user_deactivation operation"
                })
            
            # Validate user exists
            if user_id not in users:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: User not found - user_id '{user_id}' does not exist"
                })
            
            user = users[user_id]
            
            # Get deactivation datetime
            deactivation_datetime = schedule_data.get("deactivation_datetime")
            if not deactivation_datetime:
                return json.dumps({
                    "success": False,
                    "error": "Halt: deactivation_datetime required in schedule_data"
                })
            
            # Validate datetime format
            if len(deactivation_datetime) == 10:
                deactivation_datetime = deactivation_datetime + "T23:59:59"
            
            # Parse and validate future datetime
            current_dt = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S")
            deactivation_dt = datetime.strptime(deactivation_datetime[:19], "%Y-%m-%dT%H:%M:%S")
            
            if deactivation_dt <= current_dt:
                return json.dumps({
                    "success": False,
                    "error": "Halt: deactivation_datetime must be in the future"
                })
            
            # Calculate days until deactivation
            days_until = (deactivation_dt - current_dt).days
            
            # Create scheduled operation record with timestamp-based ID
            timestamp_id = current_datetime.replace("-", "").replace(":", "").replace("T", "_")
            scheduled_operation_id = f"sched_op_{timestamp_id}"
            scheduled_operation = {
                "operation_id": scheduled_operation_id,
                "operation_type": "user_deactivation",
                "user_id": user_id,
                "user_name": user.get("name"),
                "user_role": user.get("role"),
                "scheduled_datetime": deactivation_datetime,
                "status": "scheduled",
                "created_at": current_datetime
            }
            
            return json.dumps({
                "success": True,
                "operation_type": "user_deactivation",
                "user_id": user_id,
                "user_name": user.get("name"),
                "user_role": user.get("role"),
                "deactivation_datetime": deactivation_datetime,
                "days_until_deactivation": days_until,
                "scheduled_operation_id": scheduled_operation_id,
                "scheduled_operation": scheduled_operation,
                "message": f"User deactivation scheduled for {deactivation_datetime} ({days_until} days from now)"
            })
        
        elif operation_type == "reminder":
            # Schedule reminder (privacy review as per SOP 6.6.3)
            reminder_days = schedule_data.get("reminder_days")
            reminder_type = schedule_data.get("reminder_type")
            
            if not reminder_days:
                return json.dumps({
                    "success": False,
                    "error": "Halt: reminder_days required in schedule_data"
                })
            
            if not isinstance(reminder_days, (int, float)) or reminder_days <= 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: reminder_days must be a positive number"
                })
            
            if not reminder_type:
                return json.dumps({
                    "success": False,
                    "error": "Halt: reminder_type required in schedule_data"
                })
            
            # Only privacy_review is valid as per SOP 6.6.3
            if reminder_type != "privacy_review":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid reminder_type '{reminder_type}'. Must be 'privacy_review'"
                })
            
            # Calculate reminder datetime
            current_dt = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S")
            reminder_dt = current_dt + timedelta(days=reminder_days)
            reminder_datetime = reminder_dt.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Optional: specific users to remind (Admin by default)
            target_user_ids = schedule_data.get("target_user_ids", [])
            if not target_user_ids:
                # Default to all Admins
                admin_users = [uid for uid, u in users.items() if u.get("role") == "Admin"]
                target_user_ids = admin_users
            
            # Validate target users exist
            for target_uid in target_user_ids:
                if target_uid not in users:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Target user not found - user_id '{target_uid}' does not exist"
                    })
            
            # Create scheduled reminder record with timestamp-based ID
            timestamp_id = current_datetime.replace("-", "").replace(":", "").replace("T", "_")
            reminder_id = f"reminder_{timestamp_id}"
            scheduled_reminder = {
                "reminder_id": reminder_id,
                "reminder_type": reminder_type,
                "target_user_ids": target_user_ids,
                "scheduled_datetime": reminder_datetime,
                "reminder_days": reminder_days,
                "status": "scheduled",
                "created_at": current_datetime
            }
            
            reminder_message = "Time to review privacy settings for Echo devices"
            
            return json.dumps({
                "success": True,
                "operation_type": "reminder",
                "reminder_type": reminder_type,
                "reminder_id": reminder_id,
                "reminder_datetime": reminder_datetime,
                "reminder_days": reminder_days,
                "target_user_ids": target_user_ids,
                "target_user_count": len(target_user_ids),
                "reminder_message": reminder_message,
                "scheduled_reminder": scheduled_reminder,
                "message": f"Privacy review reminder scheduled for {reminder_datetime} ({reminder_days} days from now)"
            })
        
        elif operation_type == "announcement":
            # Schedule announcement delivery to Echo devices
            message = schedule_data.get("message")
            target_devices = schedule_data.get("target_devices", [])
            delivery_datetime = schedule_data.get("delivery_datetime")
            volume = schedule_data.get("volume", "device_default")
            
            if not message:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message required in schedule_data for announcement"
                })
            
            # Validate message length
            if len(message) > 280:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message exceeds 280 character limit"
                })
            
            if not target_devices or not isinstance(target_devices, list):
                return json.dumps({
                    "success": False,
                    "error": "Halt: target_devices required and must be a list"
                })
            
            if not delivery_datetime:
                return json.dumps({
                    "success": False,
                    "error": "Halt: delivery_datetime required in schedule_data for scheduled announcement"
                })
            
            # Validate datetime format and future time
            if len(delivery_datetime) == 10:
                delivery_datetime = delivery_datetime + "T09:00:00"
            
            current_dt = datetime.strptime(current_datetime, "%Y-%m-%dT%H:%M:%S")
            delivery_dt = datetime.strptime(delivery_datetime[:19], "%Y-%m-%dT%H:%M:%S")
            
            if delivery_dt <= current_dt:
                return json.dumps({
                    "success": False,
                    "error": "Halt: delivery_datetime must be in the future"
                })
            
            # Validate all target devices exist and are Echo devices
            validated_devices = []
            for device_id in target_devices:
                if device_id not in devices:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                    })
                
                device = devices[device_id]
                device_type = device.get("device_type")
                
                # Check if device is Echo device
                if device_type not in ["speaker", "echo_device"]:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Device '{device_id}' is not an Echo device - type '{device_type}' cannot play announcements"
                    })
                
                validated_devices.append({
                    "device_id": device_id,
                    "device_name": device.get("device_name"),
                    "device_type": device_type
                })
            
            # Validate volume level
            valid_volumes = ["quiet", "medium", "loud", "device_default"]
            if volume not in valid_volumes:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid volume '{volume}'. Must be one of: {', '.join(valid_volumes)}"
                })
            
            # Calculate time until delivery
            hours_until = (delivery_dt - current_dt).total_seconds() / 3600
            
            # Create scheduled announcement record with timestamp-based ID
            timestamp_id = current_datetime.replace("-", "").replace(":", "").replace("T", "_")
            announcement_id = f"sched_announce_{timestamp_id}"
            scheduled_announcement = {
                "announcement_id": announcement_id,
                "message": message,
                "target_devices": target_devices,
                "delivery_datetime": delivery_datetime,
                "volume": volume,
                "status": "scheduled",
                "created_at": current_datetime
            }
            
            return json.dumps({
                "success": True,
                "operation_type": "announcement",
                "announcement_id": announcement_id,
                "message": message,
                "delivery_datetime": delivery_datetime,
                "hours_until_delivery": round(hours_until, 1),
                "target_devices": validated_devices,
                "target_device_count": len(validated_devices),
                "volume": volume,
                "scheduled_announcement": scheduled_announcement,
                "message_text": f"Announcement scheduled for delivery at {delivery_datetime} to {len(validated_devices)} devices"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "arrange_user_operation",
                "description": "Schedule automatic user operations in the smart home management system. Handles scheduled user deactivation for guest access expiration , privacy review reminder scheduling , and scheduled announcement delivery to Echo devices . Validates future datetimes, device capabilities, and message constraints. Only supports 'privacy_review' as reminder type per policy.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation_type": {
                            "type": "string",
                            "description": "Type of scheduled operation",
                            "enum": ["user_deactivation", "reminder", "announcement"]
                        },
                        "user_id": {
                            "type": "string",
                            "description": "User identifier (required for user_deactivation)"
                        },
                        "schedule_data": {
                            "type": "object",
                            "description": "Scheduling parameters based on operation_type. For user_deactivation: {deactivation_datetime}. For reminder: {reminder_days, reminder_type='privacy_review', target_user_ids}. For announcement: {message, target_devices, delivery_datetime, volume}",
                            "properties": {
                                "deactivation_datetime": {
                                    "type": "string",
                                    "description": "Datetime when user should be deactivated (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                                },
                                "reminder_days": {
                                    "type": "number",
                                    "description": "Number of days from now to schedule reminder"
                                },
                                "reminder_type": {
                                    "type": "string",
                                    "description": "Type of reminder: must be 'privacy_review'"
                                },
                                "target_user_ids": {
                                    "type": "array",
                                    "description": "List of user IDs to receive reminder (defaults to all Admins)",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "message": {
                                    "type": "string",
                                    "description": "Announcement message text (max 280 characters)"
                                },
                                "target_devices": {
                                    "type": "array",
                                    "description": "List of Echo device IDs for announcement",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "delivery_datetime": {
                                    "type": "string",
                                    "description": "Datetime when announcement should be delivered (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)"
                                },
                                "volume": {
                                    "type": "string",
                                    "description": "Announcement volume: quiet, medium, loud, device_default",
                                    "enum": ["quiet", "medium", "loud", "device_default"]
                                }
                            }
                        }
                    },
                    "required": ["operation_type", "schedule_data"]
                }
            }
        }