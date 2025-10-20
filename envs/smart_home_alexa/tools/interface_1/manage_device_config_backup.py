import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ManageDeviceConfigBackup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, backup_type: str, device_id: str, backup_data: Dict[str, Any] = None) -> str:
        """
        Backup or restore device and network configurations.

        Operations:
        - backup: Capture and store current device or network configuration (requires backup_type, device_id)
        - restore: Retrieve and apply configuration from backup to device (requires backup_type, device_id)
        """
        
        def generate_backup_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate operation
        if operation not in ["backup", "restore"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be 'backup' or 'restore'"
            })
        
        # Validate backup_type
        if backup_type not in ["device_config", "network_config"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid backup_type '{backup_type}'. Must be 'device_config' or 'network_config'"
            })
        
        # Validate device_id
        if not device_id:
            return json.dumps({
                "success": False,
                "error": "device_id is required"
            })
        
        # Access backup_records data
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for backup_records"
            })
        
        backup_records = data.get("backup_records", {})
        
        if operation == "backup":
            # Check for existing backup for the same device and backup_type
            for existing_backup in backup_records.values():
                if (existing_backup.get("device_id") == device_id and
                    existing_backup.get("backup_type") == backup_type):
                    return json.dumps({
                        "success": False,
                        "error": f"Backup already exists for device {device_id} with type {backup_type}. Only one backup per device and type is allowed."
                    })

            # Capture current device configuration
            devices = data.get("devices", {})
            device = devices.get(device_id)

            if not device:
                return json.dumps({
                    "success": False,
                    "error": f"Device {device_id} not found"
                })

            # Capture configuration based on backup_type
            if backup_type == "device_config":
                captured_data = {
                    "name": device.get("name"),
                    "status": device.get("status"),
                    "settings": device.get("settings", {}),
                    "privacy_settings": device.get("privacy_settings", {}),
                    "voice_profile_settings": device.get("voice_profile_settings", {})
                }
            elif backup_type == "network_config":
                captured_data = {
                    "network_name": device.get("network_name"),
                    "network_frequency": device.get("network_frequency"),
                    "ip_address": device.get("ip_address"),
                    "mac_address": device.get("mac_address")
                }
            else:
                captured_data = {}

            # Generate new backup ID
            new_backup_id = generate_backup_id(backup_records)

            # Create new backup record
            new_backup = {
                "backup_id": str(new_backup_id),
                "device_id": device_id,
                "backup_type": backup_type,
                "created_at": "2025-10-01T12:00:00",
                "backup_data": captured_data
            }

            backup_records[str(new_backup_id)] = new_backup

            return json.dumps({
                "success": True,
                "action": "backup",
                "backup_id": str(new_backup_id),
                "message": f"Backup {new_backup_id} created successfully for device {device_id} with type {backup_type}",
                "backup_record": new_backup
            })
        
        elif operation == "restore":
            # Find matching backup record
            backup_id = None
            for bid, record in backup_records.items():
                if (record.get("device_id") == device_id and
                    record.get("backup_type") == backup_type):
                    backup_id = bid
                    break

            if not backup_id:
                return json.dumps({
                    "success": False,
                    "error": f"No backup found for device {device_id} with type {backup_type}"
                })

            # Get backup data from backup record
            backup_record = backup_records[backup_id]
            stored_backup_data = backup_record.get("backup_data", {})

            if not stored_backup_data:
                return json.dumps({
                    "success": False,
                    "error": f"Backup {backup_id} contains no data to restore"
                })

            # Get device to restore to
            devices = data.get("devices", {})
            device = devices.get(device_id)

            if not device:
                return json.dumps({
                    "success": False,
                    "error": f"Device {device_id} not found"
                })

            # Apply backup data to device based on backup_type
            if backup_type == "device_config":
                # Restore device configuration settings
                if "name" in stored_backup_data:
                    device["name"] = stored_backup_data["name"]
                if "status" in stored_backup_data:
                    device["status"] = stored_backup_data["status"]
                if "settings" in stored_backup_data:
                    device["settings"] = stored_backup_data["settings"]
                if "privacy_settings" in stored_backup_data:
                    device["privacy_settings"] = stored_backup_data["privacy_settings"]
                if "voice_profile_settings" in stored_backup_data:
                    device["voice_profile_settings"] = stored_backup_data["voice_profile_settings"]

            elif backup_type == "network_config":
                # Restore network configuration
                if "network_name" in stored_backup_data:
                    device["network_name"] = stored_backup_data["network_name"]
                if "network_frequency" in stored_backup_data:
                    device["network_frequency"] = stored_backup_data["network_frequency"]
                if "ip_address" in stored_backup_data:
                    device["ip_address"] = stored_backup_data["ip_address"]
                if "mac_address" in stored_backup_data:
                    device["mac_address"] = stored_backup_data["mac_address"]

            # Record restoration timestamp
            device["last_restored_at"] = "2025-10-01T12:00:00"
            device["last_restored_from_backup_id"] = str(backup_id)

            return json.dumps({
                "success": True,
                "action": "restore",
                "backup_id": str(backup_id),
                "device_id": device_id,
                "backup_type": backup_type,
                "message": f"Configuration restored successfully to device {device_id} from backup {backup_id}",
                "restored_data": stored_backup_data
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "manage_device_config_backup",
                "description": "Backup and restore device and network configurations in the device management system. This tool manages configuration backups to ensure system reliability and recovery capabilities. For backup, captures and stores the current configuration for a specified device and backup type, preventing duplicate backups for the same device and type combination. For restore, retrieves a previously saved configuration from backup records and applies it to the device, ensuring data integrity and compatibility. Essential for disaster recovery, system maintenance, and configuration management. Supports both device-specific and network-wide configurations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Operation to perform: 'backup' to capture and store current device configuration, 'restore' to retrieve and apply a saved configuration to the device",
                            "enum": ["backup", "restore"]
                        },
                        "backup_type": {
                            "type": "string",
                            "description": "Type of configuration to manage: 'device_config' for individual device settings (name, status, privacy_settings, voice_profile_settings), 'network_config' for network settings (network_name, network_frequency, ip_address, mac_address)",
                            "enum": ["device_config", "network_config"]
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Unique identifier of the device to backup or restore"
                        },
                        "backup_data": {
                            "type": "object",
                            "description": "DEPRECATED: No longer used. Configuration data is automatically retrieved from backup records during restore operation."
                        }
                    },
                    "required": ["operation", "backup_type", "device_id"]
                }
            }
        }