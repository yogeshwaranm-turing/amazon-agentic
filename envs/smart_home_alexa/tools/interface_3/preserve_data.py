import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class PreserveData(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], archive_type: str, entity_id: str, retention_days: int) -> str:
        """
        Archive historical data in the smart home management system.
        Handles archival of device logs and user logs for long-term retention and compliance.
        """

        # Validate archive_type
        valid_types = ["device_logs", "user_logs"]
        if archive_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid archive_type '{archive_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not entity_id:
            return json.dumps({
                "success": False,
                "error": "Halt: entity_id required for archive operation"
            })

        if not isinstance(retention_days, int) or retention_days <= 0:
            return json.dumps({
                "success": False,
                "error": "Halt: retention_days must be a positive integer"
            })

        # Get access_logs table
        access_logs = data.get("access_logs", {})

        if archive_type == "device_logs":
            # Archive logs for a specific device (SOP 6.2.5)
            devices = data.get("devices", {})

            # Validate device exists
            if entity_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - entity_id '{entity_id}' does not exist"
                })

            device = devices[entity_id]

            # Filter logs related to this device
            device_logs = []
            for log in access_logs.values():
                if (log.get("entity_id") == entity_id and log.get("entity_type") == "device") or \
                   (log.get("operation_details", "{}").find(entity_id) != -1):
                    device_logs.append(log)

            # Simulate archival
            archive_id = f"archive_device_{entity_id}_{retention_days}d"
            archive_location = f"/archives/devices/{entity_id}/{archive_id}.json"
            archive_timestamp = "2025-10-16T14:30:00"
            expiration_date = "2025-10-16T14:30:00"  # Would calculate based on retention_days

            # In real implementation, would:
            # 1. Compress logs
            # 2. Upload to archive storage
            # 3. Remove from active logs
            # 4. Create archive metadata record

            return json.dumps({
                "success": True,
                "archive_type": "device_logs",
                "device_id": entity_id,
                "device_name": device.get("device_name"),
                "logs_archived": len(device_logs),
                "retention_days": retention_days,
                "archive_id": archive_id,
                "archive_location": archive_location,
                "archive_timestamp": archive_timestamp,
                "expiration_date": expiration_date,
                "message": f"Archived {len(device_logs)} logs for device '{device.get('device_name')}' with {retention_days} day retention"
            })

        elif archive_type == "user_logs":
            # Archive logs for a specific user (SOP 6.4.3)
            users = data.get("users", {})

            # Validate user exists or existed
            user_exists = entity_id in users

            # Filter logs related to this user
            user_logs = []
            for log in access_logs.values():
                if log.get("user_id") == entity_id:
                    user_logs.append(log)

            # Simulate archival
            archive_id = f"archive_user_{entity_id}_{retention_days}d"
            archive_location = f"/archives/users/{entity_id}/{archive_id}.json"
            archive_timestamp = "2025-10-16T14:30:00"
            expiration_date = "2025-10-16T14:30:00"  # Would calculate based on retention_days

            return json.dumps({
                "success": True,
                "archive_type": "user_logs",
                "user_id": entity_id,
                "user_exists": user_exists,
                "logs_archived": len(user_logs),
                "retention_days": retention_days,
                "archive_id": archive_id,
                "archive_location": archive_location,
                "archive_timestamp": archive_timestamp,
                "expiration_date": expiration_date,
                "message": f"Archived {len(user_logs)} logs for user '{entity_id}' with {retention_days} day retention"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "preserve_data",
                "description": "Archive historical data in the smart home management system. Archives device_logs for long-term retention when devices are removed or decommissioned, maintaining audit trail for compliance and troubleshooting (SOP 6.2.5). Archives user_logs when users are removed from the system, preserving activity history for security audits and compliance requirements (SOP 6.4.3). Supports configurable retention periods in days for regulatory compliance (typically 90-365 days). Implements compression and secure storage of archived data. Creates archive metadata records with archive ID, location, timestamp, and expiration date. Essential for GDPR compliance, security audits, and regulatory requirements.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "archive_type": {
                            "type": "string",
                            "description": "Type of data to archive",
                            "enum": ["device_logs", "user_logs"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "Device ID or User ID to archive logs for (required)"
                        },
                        "retention_days": {
                            "type": "integer",
                            "description": "Number of days to retain archived data (required, must be positive)"
                        }
                    },
                    "required": ["archive_type", "entity_id", "retention_days"]
                }
            }
        }
