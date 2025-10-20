import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class FirmwareController(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        operation: str,
        device_id: Optional[str] = None,
        update_scope: Optional[str] = None,
        operation_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Manage device firmware updates and rollbacks.

        Operations:
        - discover_updates: Scan devices for available firmware updates (security or general)
        - initiate_update: Start firmware update for a specific device
        - monitor_progress: Monitor update progress
        - wait_reconnection: Wait for devices to reconnect after update
        - restore_previous: Rollback firmware to previous version
        - initialize_tracking: Initialize update tracking metadata
        - update_tracking: Update tracking status during or after firmware update
        """

        # Validate operation
        valid_operations = [
            "discover_updates", "initiate_update", "monitor_progress",
            "wait_reconnection", "restore_previous", "initialize_tracking",
            "update_tracking"
        ]
        if operation not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be one of {valid_operations}"
            })

        # Initialize device data
        devices = data.get("devices", {})

        # Handle operation-specific logic
        if operation == "discover_updates":
            scope = update_scope or "all_devices"
            available_updates = []

            for dev_id, dev_info in devices.items():
                # Example simulated logic
                if scope in ["all_devices", "security_updates_only"] and dev_info.get("firmware_outdated"):
                    available_updates.append({
                        "device_id": dev_id,
                        "current_version": dev_info.get("firmware_version"),
                        "available_version": dev_info.get("available_firmware"),
                        "update_type": "security" if dev_info.get("security_patch_pending") else "general"
                    })

            return json.dumps({
                "success": True,
                "operation": "discover_updates",
                "update_scope": scope,
                "available_updates": available_updates,
                "message": f"Discovered {len(available_updates)} updates in scope '{scope}'"
            })

        elif operation == "initiate_update":
            if not device_id or device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Device '{device_id}' not found or missing"
                })

            # Check prerequisites before initiating update
            device = devices[device_id]
            connection_status = device.get("connection_status")
            battery_level = device.get("battery_level")
            signal_strength = device.get("signal_strength")
            power_source = device.get("power_source", "battery")

            # Prerequisites: online, battery >20% (or plugged in), signal >-70 dBm
            prerequisites_met = True
            failure_reasons = []

            if connection_status != "online":
                prerequisites_met = False
                failure_reasons.append(f"Device is not online (status: {connection_status})")

            if power_source != "plugged_in":
                if battery_level is None:
                    prerequisites_met = False
                    failure_reasons.append("Battery level unknown")
                elif battery_level <= 20:
                    prerequisites_met = False
                    failure_reasons.append(f"Battery level too low ({battery_level}% <= 20%)")

            if signal_strength is not None and signal_strength <= -70:
                prerequisites_met = False
                failure_reasons.append(f"Signal strength too weak ({signal_strength} dBm <= -70 dBm)")

            if not prerequisites_met:
                return json.dumps({
                    "success": False,
                    "operation": "initiate_update",
                    "device_id": device_id,
                    "error": "Device does not meet firmware update prerequisites",
                    "failure_reasons": failure_reasons,
                    "prerequisites": {
                        "connection_status": connection_status,
                        "battery_level": battery_level,
                        "signal_strength": signal_strength,
                        "power_source": power_source
                    }
                })

            # Store previous firmware version for rollback capability
            current_version = device.get("firmware_version")
            if current_version:
                device["previous_firmware_version"] = current_version

            device["update_status"] = "in_progress"
            device["update_started_at"] = "2025-10-01T00:00:00"

            return json.dumps({
                "success": True,
                "operation": "initiate_update",
                "device_id": device_id,
                "message": f"Firmware update initiated for device {device_id}",
                "previous_version": current_version
            })

        elif operation == "monitor_progress":
            if not device_id or device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Device '{device_id}' not found or missing"
                })

            status = devices[device_id].get("update_status", "not_started")
            progress = devices[device_id].get("update_progress", 0)

            return json.dumps({
                "success": True,
                "operation": "monitor_progress",
                "device_id": device_id,
                "status": status,
                "progress": progress,
                "message": f"Device {device_id} update status: {status}, progress: {progress}%"
            })

        elif operation == "wait_reconnection":
            if not device_id:
                return json.dumps({"success": False, "error": "device_id is required for wait_reconnection"})

            devices[device_id]["connection_status"] = "reconnected"
            return json.dumps({
                "success": True,
                "operation": "wait_reconnection",
                "device_id": device_id,
                "message": f"Device {device_id} successfully reconnected after firmware update."
            })

        elif operation == "restore_previous":
            if not device_id or device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Device '{device_id}' not found or missing"
                })

            prev_version = devices[device_id].get("previous_firmware_version")
            if not prev_version:
                return json.dumps({
                    "success": False,
                    "error": f"No previous firmware version found for device {device_id}"
                })

            devices[device_id]["firmware_version"] = prev_version
            devices[device_id]["update_status"] = "rolled_back"

            return json.dumps({
                "success": True,
                "operation": "restore_previous",
                "device_id": device_id,
                "message": f"Device {device_id} firmware restored to previous version {prev_version}"
            })

        elif operation == "initialize_tracking":
            data["firmware_tracking"] = {"initialized_at": "2025-10-01T00:00:00", "updates_in_progress": []}
            return json.dumps({
                "success": True,
                "operation": "initialize_tracking",
                "message": "Firmware update tracking initialized successfully."
            })

        elif operation == "update_tracking":
            tracking_info = data.get("firmware_tracking", {})
            if not tracking_info:
                return json.dumps({
                    "success": False,
                    "error": "Firmware tracking not initialized. Use 'initialize_tracking' first."
                })

            if operation_data:
                tracking_info.update(operation_data)
                data["firmware_tracking"] = tracking_info

            return json.dumps({
                "success": True,
                "operation": "update_tracking",
                "message": "Firmware tracking updated successfully.",
                "tracking_data": tracking_info
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "firmware_controller",
                "description": (
                    "Manage device firmware updates, monitoring, and rollbacks. "
                    "Supports full firmware lifecycle management including discovery of available updates, "
                    "initiation of update processes, monitoring progress, waiting for reconnection, and rollback to previous versions. "
                    "Also supports initializing and updating firmware tracking records for compliance and audit purposes. "
                    "Ensures secure and efficient firmware deployment across devices, reducing vulnerabilities and downtime."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": (
                                "Operation to perform: 'discover_updates', 'initiate_update', 'monitor_progress', "
                                "'wait_reconnection', 'restore_previous', 'initialize_tracking', or 'update_tracking'"
                            ),
                            "enum": [
                                "discover_updates", "initiate_update", "monitor_progress",
                                "wait_reconnection", "restore_previous", "initialize_tracking",
                                "update_tracking"
                            ]
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Specific device ID for firmware update or rollback actions"
                        },
                        "update_scope": {
                            "type": "string",
                            "description": (
                                "Scope of firmware discovery or update: 'all_devices', 'security_updates_only', "
                                "'specific_device', or 'device_type'"
                            ),
                            "enum": [
                                "all_devices", "security_updates_only", "specific_device", "device_type"
                            ]
                        },
                        "operation_data": {
                            "type": "object",
                            "description": "Additional operation-specific parameters or tracking metadata"
                        }
                    },
                    "required": ["operation"]
                }
            }
        }
