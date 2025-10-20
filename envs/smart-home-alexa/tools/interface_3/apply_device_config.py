import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class ApplyDeviceConfig(Tool):
    """
    A tool to configure device settings (network, privacy, status, or voice profile settings).
    """

    @staticmethod
    def invoke(data: Dict[str, Any],
               configuration_type: str,
               device_id: str,
               config_data: Dict[str, Any]) -> str:
        """
        Configures a device's settings based on the configuration type.

        Args:
            data: The database JSON.
            configuration_type: Type of configuration - "network", "privacy", "status", or "voice_profile_settings".
            device_id: The unique identifier for the device.
            config_data: The configuration parameters as a dictionary.

        Returns:
            A JSON string with the updated device configuration or an error message.
        """
        valid_configuration_types = [
            "network",
            "privacy",
            "status",
            "voice_profile_settings"
        ]

        devices = data.get("devices", {})

        # Validation: device existence
        if device_id not in devices:
            return json.dumps({
                "success": False,
                "error": f"Device '{device_id}' not found"
            })

        # Validation: configuration type
        if configuration_type not in valid_configuration_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid configuration_type '{configuration_type}'. "
                         f"Must be one of {valid_configuration_types}"
            })

        # Validation: config_data
        if not isinstance(config_data, dict) or not config_data:
            return json.dumps({
                "success": False,
                "error": "config_data must be a non-empty JSON object"
            })

        device = devices[device_id]
        timestamp = "2025-10-01T00:00:00"

        # Apply configuration based on configuration type
        if configuration_type == "network":
            allowed_fields = ["network_name", "network_frequency", "ip_address", "mac_address"]
        elif configuration_type == "privacy":
            allowed_fields = ["microphone_enabled", "camera_enabled", "location_access", "voice_recording_enabled"]
        elif configuration_type == "status":
            allowed_fields = ["connection_status", "power_state", "last_active"]
        elif configuration_type == "voice_profile_settings":
            allowed_fields = ["voice_id", "wake_word", "sensitivity_level"]
        else:
            allowed_fields = []

        # Filter config_data to only allowed fields
        filtered_config = {k: v for k, v in config_data.items() if k in allowed_fields}

        if not filtered_config:
            return json.dumps({
                "success": False,
                "error": f"No valid fields found in config_data for '{configuration_type}' configuration"
            })

        # Validate configuration values
        validation_error = ApplyDeviceConfig._validate_config_values(
            configuration_type,
            filtered_config
        )
        if validation_error:
            return json.dumps({
                "success": False,
                "error": validation_error
            })

        # Update the device configuration
        if "configurations" not in device:
            device["configurations"] = {}

        if configuration_type not in device["configurations"]:
            device["configurations"][configuration_type] = {}

        device["configurations"][configuration_type].update(filtered_config)
        device["updated_at"] = timestamp

        return json.dumps({
            "success": True,
            "device_id": device_id,
            "configuration_type": configuration_type,
            "updated_config": filtered_config,
            "updated_at": timestamp
        })

    @staticmethod
    def _validate_config_values(configuration_type: str, config: Dict[str, Any]) -> Optional[str]:
        """
        Validates configuration values based on the configuration type.

        Returns:
            Error message string if validation fails, None if validation passes.
        """
        if configuration_type == "network":
            # Validate network configuration
            if "network_frequency" in config:
                freq = config["network_frequency"]
                valid_frequencies = ["2.4GHz", "5GHz", "6GHz"]
                if freq not in valid_frequencies:
                    return f"Invalid network_frequency '{freq}'. Must be one of {valid_frequencies}"

            if "ip_address" in config:
                ip = config["ip_address"]
                if not isinstance(ip, str) or not ip:
                    return "ip_address must be a non-empty string"
                # Basic IP format validation
                import re
                ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
                if not re.match(ip_pattern, ip):
                    return f"Invalid ip_address format: '{ip}'. Expected format: xxx.xxx.xxx.xxx"

            if "mac_address" in config:
                mac = config["mac_address"]
                if not isinstance(mac, str) or not mac:
                    return "mac_address must be a non-empty string"
                # Basic MAC format validation
                import re
                mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
                if not re.match(mac_pattern, mac):
                    return f"Invalid mac_address format: '{mac}'. Expected format: XX:XX:XX:XX:XX:XX"

            if "network_name" in config:
                name = config["network_name"]
                if not isinstance(name, str) or not name:
                    return "network_name must be a non-empty string"

        elif configuration_type == "privacy":
            # Validate privacy configuration - all should be boolean
            boolean_fields = ["microphone_enabled", "camera_enabled", "location_access", "voice_recording_enabled"]
            for field in boolean_fields:
                if field in config:
                    if not isinstance(config[field], bool):
                        return f"'{field}' must be a boolean value (true or false)"

        elif configuration_type == "status":
            # Validate status configuration
            if "connection_status" in config:
                status = config["connection_status"]
                valid_statuses = ["online", "offline", "connecting", "disconnected"]
                if status not in valid_statuses:
                    return f"Invalid connection_status '{status}'. Must be one of {valid_statuses}"

            if "power_state" in config:
                power = config["power_state"]
                valid_states = ["on", "off", "standby", "sleep"]
                if power not in valid_states:
                    return f"Invalid power_state '{power}'. Must be one of {valid_states}"

            if "last_active" in config:
                # Validate timestamp format
                last_active = config["last_active"]
                if not isinstance(last_active, str):
                    return "last_active must be a string timestamp"

        elif configuration_type == "voice_profile_settings":
            # Validate voice profile settings
            if "voice_id" in config:
                voice_id = config["voice_id"]
                if not isinstance(voice_id, str) or not voice_id:
                    return "voice_id must be a non-empty string"

            if "wake_word" in config:
                wake_word = config["wake_word"]
                valid_wake_words = ["alexa", "amazon", "echo", "computer"]
                if wake_word not in valid_wake_words:
                    return f"Invalid wake_word '{wake_word}'. Must be one of {valid_wake_words}"

            if "sensitivity_level" in config:
                sensitivity = config["sensitivity_level"]
                if not isinstance(sensitivity, (int, float)):
                    return "sensitivity_level must be a numeric value"
                if not (0 <= sensitivity <= 10):
                    return "sensitivity_level must be between 0 and 10"

        return None

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the ApplyDeviceConfig tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "apply_device_config",
                "description": (
                    "Configures device settings for a given device. "
                    "Supported configuration types include 'network', 'privacy', 'status', "
                    "and 'voice_profile_settings'. Each type accepts specific configuration parameters."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "configuration_type": {
                            "type": "string",
                            "description": (
                                "Type of configuration to apply. "
                                "Allowed values: network, privacy, status, voice_profile_settings."
                            )
                        },
                        "device_id": {
                            "type": "string",
                            "description": "The unique device identifier to configure."
                        },
                        "config_data": {
                            "type": "object",
                            "description": (
                                "A JSON object containing configuration parameters relevant "
                                "to the specified configuration_type."
                            )
                        }
                    },
                    "required": ["configuration_type", "device_id", "config_data"]
                }
            }
        }
