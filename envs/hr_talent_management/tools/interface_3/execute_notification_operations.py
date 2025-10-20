# Auto-generated — DO NOT EDIT BY HAND
import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ExecuteNotificationOperations(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], mode: str, recipient_user_id: str = None, sender_user_id: str = None, recipient_email: str = None, notification_type: str = None, reference_type: str = None, reference_id: str = None, subject: str = None, notification_id: str = None, failed_reason: str = None) -> str:
        notifications = data.setdefault("notifications", {})
        mode = (mode or "").strip().lower()
        if mode not in {"notifications.queue","notifications.mark_sent","notifications.mark_failed"}:
            raise ValueError("mode must be one of notifications.queue|notifications.mark_sent|notifications.mark_failed")

        valid_types = ['application_acknowledgment', 'interview_scheduled', 'offer_issued', 'onboarding_welcome', 'payslip_released', 'payment_processed', 'benefits_enrollment', 'payroll_query_update', 'exit_confirmation', 'document_request', 'other']
        valid_refs = ['application', 'interview', 'offer', 'employee', 'payroll', 'benefit', 'document', 'exit']

        if mode == "notifications.queue":
            # required fields
            required = [recipient_user_id, sender_user_id, notification_type, reference_type, reference_id, subject]
            if any(v in (None, "") for v in required):
                raise ValueError("Missing required args for notifications.queue")

            if notification_type not in valid_types:
                raise ValueError(f"notification_type must be one of {valid_types}")
            if reference_type not in valid_refs:
                raise ValueError(f"reference_type must be one of {valid_refs}")

            new_id = str(max([int(k) for k in notifications.keys()] + [0]) + 1)
            rec = {
                "notification_id": new_id,
                "recipient_user_id": recipient_user_id,
                "sender_user_id": sender_user_id,
                "recipient_email": recipient_email,
                "notification_type": notification_type,
                "reference_type": reference_type,
                "reference_id": reference_id,
                "subject": subject,
                "notification_status": "pending",
                "created_at": data.get("_now_utc", "2025-01-01T00:00:00Z"),
                "sent_at": None,
                "failed_reason": None
            }
            notifications[new_id] = rec
            return json.dumps(rec)

        if not notification_id:
            raise ValueError("notification_id is required for status updates")
        if notification_id not in notifications:
            raise ValueError(f"Notification {notification_id} not found")

        rec = notifications[notification_id]
        if mode == "notifications.mark_sent":
            rec["notification_status"] = "sent"
            rec["sent_at"] = data.get("_now_utc", "2025-01-01T00:00:00Z")
            return json.dumps(rec)

        rec["notification_status"] = "failed"
        rec["failed_reason"] = failed_reason or "unspecified"
        return json.dumps(rec)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "execute_notification_operations",
                "description": 'Create or update notifications (queue, mark_sent, mark_failed) per notifications table.',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {"type": "str"},
                        "recipient_user_id": {"type": "str"},
                        "sender_user_id": {"type": "str"},
                        "recipient_email": {"type": "str"},
                        "notification_type": {"type": "str"},
                        "reference_type": {"type": "str"},
                        "reference_id": {"type": "str"},
                        "subject": {"type": "str"},
                        "notification_id": {"type": "str"},
                        "failed_reason": {"type": "str"}
                    },
                    "required": ["mode"]
                }
            }
        }

def manage_notification_operations(data: Dict[str, Any], **kwargs) -> str:
    return ManageNotificationOperations.invoke(data, **kwargs)
