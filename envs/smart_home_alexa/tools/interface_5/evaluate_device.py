import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class EvaluateDevice(Tool):
    """
    A tool to diagnose device issues and generate recommendations.
    """

    @staticmethod
    def invoke(data: Dict[str, Any],
               diagnostic_type: str,
               device_id: Optional[str] = None,
               diagnostic_scope: Optional[str] = None,
               diagnostic_parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Runs diagnostics on a device or group of devices.

        Args:
            data: The database JSON.
            diagnostic_type: Type of diagnostic - "connection", "health",
                             "performance", "conflicts", "routine_action_failure",
                             or "performance_issues".
            device_id: The specific device to diagnose (optional).
            diagnostic_scope: The scope of the diagnostic - "single_device",
                              "all_devices", "device_type", or "group" (optional).
            diagnostic_parameters: Additional diagnostic criteria (optional).

        Returns:
            A JSON string containing diagnostic results and recommendations.
        """
        valid_diagnostic_types = [
            "connection",
            "health",
            "performance",
            "conflicts",
            "routine_action_failure",
            "performance_issues"
        ]
        valid_scopes = ["single_device", "all_devices", "device_type", "group"]

        devices = data.get("devices", {})
        timestamp = "2025-10-01T00:00:00"

        # Validate diagnostic_type
        if diagnostic_type not in valid_diagnostic_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid diagnostic_type '{diagnostic_type}'. "
                         f"Must be one of {valid_diagnostic_types}"
            })

        # Validate scope
        if diagnostic_scope and diagnostic_scope not in valid_scopes:
            return json.dumps({
                "success": False,
                "error": f"Invalid diagnostic_scope '{diagnostic_scope}'. "
                         f"Must be one of {valid_scopes}"
            })

        # Validate device_id if provided
        if device_id and device_id not in devices:
            return json.dumps({
                "success": False,
                "error": f"Device '{device_id}' not found"
            })

        # Default values
        diagnostic_scope = diagnostic_scope or ("single_device" if device_id else "all_devices")
        diagnostic_parameters = diagnostic_parameters or {}

        # Simulate diagnostic result
        result = {
            "success": True,
            "timestamp": timestamp,
            "diagnostic_type": diagnostic_type,
            "diagnostic_scope": diagnostic_scope,
            "device_id": device_id,
            "parameters_used": diagnostic_parameters,
            "issues_detected": [],
            "recommendations": []
        }

        # Determine devices to diagnose based on scope
        target_devices = []
        if diagnostic_scope == "single_device" and device_id:
            target_devices = [(device_id, devices[device_id])]
        elif diagnostic_scope == "all_devices":
            target_devices = list(devices.items())
        elif diagnostic_scope == "device_type":
            device_type = diagnostic_parameters.get("device_type")
            target_devices = [(did, dev) for did, dev in devices.items() if dev.get("device_type") == device_type]
        elif diagnostic_scope == "group":
            group_id = diagnostic_parameters.get("group_id")
            # Filter devices by group_id
            target_devices = [(did, dev) for did, dev in devices.items() if dev.get("group_id") == group_id]

        # Analyze devices based on diagnostic type
        if diagnostic_type == "connection":
            for dev_id, device in target_devices:
                signal = device.get("signal_strength")
                conn_status = device.get("connection_status")

                if conn_status != "online":
                    result["issues_detected"].append(f"Device {dev_id} is {conn_status}")
                    result["recommendations"].append(f"Check device {dev_id} connectivity and restart if needed")

                if signal and signal < -70:
                    result["issues_detected"].append(f"Device {dev_id} has weak signal ({signal} dBm)")
                    result["recommendations"].append(f"Move device {dev_id} closer to router or add Wi-Fi extender")

                if signal and -70 <= signal < -60:
                    result["issues_detected"].append(f"Device {dev_id} has marginal signal ({signal} dBm)")
                    result["recommendations"].append(f"Consider repositioning device {dev_id} for better signal")

        elif diagnostic_type == "health":
            for dev_id, device in target_devices:
                battery = device.get("battery_level")
                firmware = device.get("firmware_version")
                available_firmware = device.get("available_firmware")
                last_active = device.get("last_active")

                if battery is not None and battery < 20:
                    result["issues_detected"].append(f"Device {dev_id} has low battery ({battery}%)")
                    result["recommendations"].append(f"Replace or charge battery for device {dev_id}")

                if firmware and available_firmware and firmware != available_firmware:
                    result["issues_detected"].append(f"Device {dev_id} firmware outdated (current: {firmware}, available: {available_firmware})")
                    result["recommendations"].append(f"Update device {dev_id} to latest firmware version {available_firmware}")

                if device.get("firmware_outdated"):
                    result["issues_detected"].append(f"Device {dev_id} requires firmware update")
                    result["recommendations"].append(f"Schedule firmware update for device {dev_id}")

        elif diagnostic_type == "performance":
            for dev_id, device in target_devices:
                response_time = device.get("response_time_ms", 0)
                cpu_usage = device.get("cpu_usage", 0)
                memory_usage = device.get("memory_usage", 0)

                if response_time > 2000:
                    result["issues_detected"].append(f"Device {dev_id} has slow response time ({response_time}ms)")
                    result["recommendations"].append(f"Reboot device {dev_id} to clear cache and improve performance")

                if cpu_usage > 80:
                    result["issues_detected"].append(f"Device {dev_id} has high CPU usage ({cpu_usage}%)")
                    result["recommendations"].append(f"Close background processes on device {dev_id}")

                if memory_usage > 85:
                    result["issues_detected"].append(f"Device {dev_id} has high memory usage ({memory_usage}%)")
                    result["recommendations"].append(f"Clear cache or restart device {dev_id}")

        elif diagnostic_type == "conflicts":
            net_name = diagnostic_parameters.get("network_name", "unknown")
            # Check for IP conflicts
            ip_addresses = {}
            for dev_id, device in target_devices:
                ip = device.get("ip_address")
                if ip:
                    if ip in ip_addresses:
                        result["issues_detected"].append(f"IP conflict detected: {ip} used by devices {ip_addresses[ip]} and {dev_id}")
                        result["recommendations"].append(f"Assign static IP or reconfigure DHCP for devices {ip_addresses[ip]} and {dev_id}")
                    else:
                        ip_addresses[ip] = dev_id

        elif diagnostic_type == "routine_action_failure":
            # Check devices that might be causing routine failures
            for dev_id, device in target_devices:
                if device.get("connection_status") != "online":
                    result["issues_detected"].append(f"Device {dev_id} is offline and may cause routine failures")
                    result["recommendations"].append(f"Reconnect device {dev_id} before executing routines")

                if device.get("error_count", 0) > 0:
                    result["issues_detected"].append(f"Device {dev_id} has {device.get('error_count')} recent errors")
                    result["recommendations"].append(f"Check device {dev_id} logs and reset if necessary")

        elif diagnostic_type == "performance_issues":
            for dev_id, device in target_devices:
                temp = device.get("temperature_celsius")
                uptime = device.get("uptime_hours", 0)

                if temp and temp > 70:
                    result["issues_detected"].append(f"Device {dev_id} temperature high ({temp}°C)")
                    result["recommendations"].append(f"Ensure proper ventilation for device {dev_id}")

                if uptime > 720:  # 30 days
                    result["issues_detected"].append(f"Device {dev_id} has been running for {uptime} hours without restart")
                    result["recommendations"].append(f"Schedule maintenance restart for device {dev_id}")

        # Provide default message if no issues found
        if not result["issues_detected"]:
            result["issues_detected"] = ["No issues detected"]
            result["recommendations"] = ["System is operating normally"]

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the EvaluateDevice tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "evaluate_device",
                "description": (
                    "Diagnoses device issues and provides recommendations based on "
                    "the specified diagnostic type. Supports individual or group-level "
                    "diagnostics for connection, health, performance, and conflicts."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "diagnostic_type": {
                            "type": "string",
                            "description": (
                                "Specifies the type of diagnostic to perform. "
                                "Allowed values: connection, health, performance, "
                                "conflicts, routine_action_failure, performance_issues."
                            )
                        },
                        "device_id": {
                            "type": "string",
                            "description": (
                                "Optional specific device ID for targeted diagnostics."
                            )
                        },
                        "diagnostic_scope": {
                            "type": "string",
                            "description": (
                                "Defines the scope of the diagnostic operation. "
                                "Allowed values: single_device, all_devices, device_type, group."
                            )
                        },
                        "diagnostic_parameters": {
                            "type": "object",
                            "description": (
                                "Additional parameters or criteria for diagnostics. "
                                "Example: {network_name: 'HomeWiFi'} for conflict analysis."
                            )
                        }
                    },
                    "required": ["diagnostic_type"]
                }
            }
        }
