import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ControlAlerts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], notification_type: str, notification_data: Dict[str, Any]) -> str:
        """
        Create and send alerts and notifications in the smart home management system.
        Handles security alerts, system alerts, admin notifications, email notifications,
        announcements to Echo devices, and delivery confirmation.
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        # Validate notification_type
        valid_types = ["security_alert", "system_alert", "admin_notification", "email_notification", "announcement", "wait_delivery"]
        if notification_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid notification_type '{notification_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not notification_data or not isinstance(notification_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: notification_data required and must be a dictionary"
            })

        # Get relevant tables
        system_alerts = data.get("system_alerts", {})
        devices = data.get("devices", {})

        if notification_type == "security_alert":
            # Create security alert
            priority = notification_data.get("priority", "high")
            message = notification_data.get("message")
            affected_device_id = notification_data.get("affected_device_id")
            alert_type = notification_data.get("alert_type", "security_alert")

            if not message:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message required in notification_data for security_alert"
                })

            # Validate priority
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}"
                })

            # Validate device exists if provided
            if affected_device_id and affected_device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - affected_device_id '{affected_device_id}' does not exist"
                })

            # Create alert record
            alert_id = f"alert_{generate_id(system_alerts)}"
            timestamp = "2025-10-16T14:30:00"

            alert_record = {
                "alert_id": alert_id,
                "alert_type": alert_type,
                "priority": priority,
                "message": message,
                "affected_device_id": affected_device_id,
                "affected_entity_type": "device" if affected_device_id else None,
                "affected_entity_id": affected_device_id,
                "acknowledged": False,
                "acknowledged_by_user_id": None,
                "acknowledged_at": None,
                "resolved": False,
                "resolved_at": None,
                "created_date": timestamp,
                "updated_date": timestamp
            }

            system_alerts[alert_id] = alert_record

            return json.dumps({
                "success": True,
                "notification_type": "security_alert",
                "alert_id": alert_id,
                "priority": priority,
                "message": message,
                "affected_device_id": affected_device_id,
                "timestamp": timestamp,
                "alert_record": alert_record,
                "message_sent": f"Security alert created with priority '{priority}'"
            })

        elif notification_type == "system_alert":
            # Create system alert
            priority = notification_data.get("priority", "medium")
            message = notification_data.get("message")
            alert_type = notification_data.get("alert_type", "system_alert")

            if not message:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message required in notification_data for system_alert"
                })

            # Validate priority
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}"
                })

            # Create alert record
            alert_id = f"alert_{generate_id(system_alerts)}"
            timestamp = "2025-10-16T14:30:00"

            alert_record = {
                "alert_id": alert_id,
                "alert_type": alert_type,
                "priority": priority,
                "message": message,
                "affected_device_id": None,
                "affected_entity_type": None,
                "affected_entity_id": None,
                "acknowledged": False,
                "acknowledged_by_user_id": None,
                "acknowledged_at": None,
                "resolved": False,
                "resolved_at": None,
                "created_date": timestamp,
                "updated_date": timestamp
            }

            system_alerts[alert_id] = alert_record

            return json.dumps({
                "success": True,
                "notification_type": "system_alert",
                "alert_id": alert_id,
                "priority": priority,
                "message": message,
                "timestamp": timestamp,
                "alert_record": alert_record,
                "message_sent": f"System alert created with priority '{priority}'"
            })

        elif notification_type == "admin_notification":
            # Send notification to admin users
            message = notification_data.get("message")
            subject = notification_data.get("subject", "Smart Home System Notification")

            if not message:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message required in notification_data for admin_notification"
                })

            # Get all admin users
            users = data.get("users", {})
            admin_users = [uid for uid, u in users.items() if u.get("role") == "Admin"]

            if not admin_users:
                return json.dumps({
                    "success": False,
                    "error": "Halt: No admin users found in system"
                })

            # Simulate sending notifications
            notifications_sent = []
            for admin_id in admin_users:
                admin = users[admin_id]
                notifications_sent.append({
                    "user_id": admin_id,
                    "user_name": admin.get("name"),
                    "email": admin.get("email"),
                    "sent_at": "2025-10-16T14:30:00"
                })

            return json.dumps({
                "success": True,
                "notification_type": "admin_notification",
                "subject": subject,
                "message": message,
                "admins_notified": len(notifications_sent),
                "notifications": notifications_sent,
                "timestamp": "2025-10-16T14:30:00",
                "message_sent": f"Notification sent to {len(notifications_sent)} admin users"
            })

        elif notification_type == "email_notification":
            # Send email notification to specific users
            recipient_emails = notification_data.get("recipient_emails", [])
            subject = notification_data.get("subject")
            message = notification_data.get("message")

            if not recipient_emails:
                return json.dumps({
                    "success": False,
                    "error": "Halt: recipient_emails required in notification_data for email_notification"
                })

            if not subject or not message:
                return json.dumps({
                    "success": False,
                    "error": "Halt: subject and message required in notification_data for email_notification"
                })

            # Simulate sending emails
            emails_sent = []
            for email in recipient_emails:
                emails_sent.append({
                    "recipient": email,
                    "subject": subject,
                    "sent_at": "2025-10-16T14:30:00",
                    "status": "sent"
                })

            return json.dumps({
                "success": True,
                "notification_type": "email_notification",
                "subject": subject,
                "recipients_count": len(emails_sent),
                "emails_sent": emails_sent,
                "timestamp": "2025-10-16T14:30:00",
                "message_sent": f"Email notification sent to {len(emails_sent)} recipients"
            })

        elif notification_type == "announcement":
            # Send announcement to Echo devices (SOP 6.10.2)
            message = notification_data.get("message")
            target_devices = notification_data.get("target_devices", [])
            volume = notification_data.get("volume", "device_default")

            if not message:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message required in notification_data for announcement"
                })

            if not target_devices:
                return json.dumps({
                    "success": False,
                    "error": "Halt: target_devices required in notification_data for announcement"
                })

            # Validate message length
            if len(message) > 280:
                return json.dumps({
                    "success": False,
                    "error": "Halt: message exceeds 280 character limit"
                })

            # Validate volume level
            valid_volumes = ["quiet", "medium", "loud", "device_default"]
            if volume not in valid_volumes:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid volume '{volume}'. Must be one of: {', '.join(valid_volumes)}"
                })

            # Validate target devices are Echo devices
            validated_devices = []
            for device_id in target_devices:
                if device_id not in devices:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                    })

                device = devices[device_id]
                device_type = device.get("device_type")

                if device_type not in ["speaker", "echo_device"]:
                    return json.dumps({
                        "success": False,
                        "error": f"Halt: Device '{device_id}' is not an Echo device - type '{device_type}' cannot play announcements"
                    })

                validated_devices.append({
                    "device_id": device_id,
                    "device_name": device.get("device_name"),
                    "device_type": device_type,
                    "connection_status": device.get("connection_status"),
                    "announced": device.get("connection_status") == "online"
                })

            online_devices = sum(1 for d in validated_devices if d["announced"])

            return json.dumps({
                "success": True,
                "notification_type": "announcement",
                "message": message,
                "volume": volume,
                "target_devices_count": len(validated_devices),
                "online_devices": online_devices,
                "offline_devices": len(validated_devices) - online_devices,
                "devices": validated_devices,
                "timestamp": "2025-10-16T14:30:00",
                "message_sent": f"Announcement delivered to {online_devices} of {len(validated_devices)} devices"
            })

        elif notification_type == "wait_delivery":
            # Wait for announcement delivery confirmation
            announcement_id = notification_data.get("announcement_id")
            timeout_seconds = notification_data.get("timeout_seconds", 10)

            if not announcement_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: announcement_id required in notification_data for wait_delivery"
                })

            # Simulate waiting for delivery
            delivery_completed = True  # Simulated result
            delivered_count = notification_data.get("expected_count", 1)

            return json.dumps({
                "success": True,
                "notification_type": "wait_delivery",
                "announcement_id": announcement_id,
                "delivery_completed": delivery_completed,
                "delivered_count": delivered_count,
                "elapsed_seconds": timeout_seconds,
                "timestamp": "2025-10-16T14:30:00",
                "message_sent": f"Announcement delivery confirmed: {delivered_count} devices"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "control_alerts",
                "description": "Create and send alerts and notifications in the smart home management system. Creates security alerts for critical events like device failures, unauthorized access, or system breaches with priority levels (low/medium/high/critical) and affected device tracking. Generates system alerts for non-security events like firmware updates available, battery warnings, or configuration changes. Sends admin notifications to all users with Admin role for system-wide announcements and important updates. Delivers email notifications to specific recipients with custom subject and message content. Plays announcements on Echo devices with volume control and device targeting (SOP 6.10.2), validating Echo device capability and online status. Waits for announcement delivery confirmation with timeout handling.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_type": {
                            "type": "string",
                            "description": "Type of notification to send",
                            "enum": ["security_alert", "system_alert", "admin_notification", "email_notification", "announcement", "wait_delivery"]
                        },
                        "notification_data": {
                            "type": "object",
                            "description": "Notification-specific data. For security_alert/system_alert: {priority, message, alert_type, affected_device_id}. For admin_notification: {subject, message}. For email_notification: {recipient_emails, subject, message}. For announcement: {message, target_devices, volume}. For wait_delivery: {announcement_id, timeout_seconds, expected_count}",
                            "properties": {
                                "priority": {
                                    "type": "string",
                                    "description": "Alert priority level",
                                    "enum": ["low", "medium", "high", "critical"]
                                },
                                "message": {
                                    "type": "string",
                                    "description": "Notification message text"
                                },
                                "alert_type": {
                                    "type": "string",
                                    "description": "Type of alert being created"
                                },
                                "affected_device_id": {
                                    "type": "string",
                                    "description": "Device ID affected by the alert"
                                },
                                "subject": {
                                    "type": "string",
                                    "description": "Email subject line"
                                },
                                "recipient_emails": {
                                    "type": "array",
                                    "description": "List of recipient email addresses"
                                },
                                "target_devices": {
                                    "type": "array",
                                    "description": "List of Echo device IDs for announcement"
                                },
                                "volume": {
                                    "type": "string",
                                    "description": "Announcement volume level",
                                    "enum": ["quiet", "medium", "loud", "device_default"]
                                },
                                "announcement_id": {
                                    "type": "string",
                                    "description": "ID of announcement to track delivery"
                                },
                                "timeout_seconds": {
                                    "type": "number",
                                    "description": "Maximum wait time for delivery confirmation"
                                }
                            }
                        }
                    },
                    "required": ["notification_type", "notification_data"]
                }
            }
        }
