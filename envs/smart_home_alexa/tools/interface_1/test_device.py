import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool


class TestDevice(Tool):
    """
    A tool to test device functionality and responsiveness.
    """

    @staticmethod
    def invoke(data: Dict[str, Any],
               test_type: str,
               device_id: Optional[str] = None,
               routine_id: Optional[str] = None,
               skill_id: Optional[str] = None,
               test_parameters: Optional[Dict[str, Any]] = None) -> str:
        """
        Tests a device's functionality or responsiveness.

        Args:
            data: The database JSON.
            test_type: Type of test - "responsiveness", "routine_execution", 
                       "skill_invocation", "response_time", "wait_response", 
                       or "voice_recognition".
            device_id: The ID of the device for device-specific tests.
            routine_id: The ID of the routine for routine tests.
            skill_id: The ID of the skill for skill tests.
            test_parameters: Additional parameters for specialized tests.

        Returns:
            A JSON string containing test results or an error message.
        """
        valid_test_types = [
            "responsiveness",
            "routine_execution",
            "skill_invocation",
            "response_time",
            "wait_response",
            "voice_recognition"
        ]

        timestamp = "2025-10-01T00:00:00"
        devices = data.get("devices", {})
        routines = data.get("routines", {})
        skills = data.get("skills", {})

        # Validate test_type
        if test_type not in valid_test_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid test_type '{test_type}'. Must be one of {valid_test_types}"
            })

        # Ensure required context for each test type
        if test_type in ["responsiveness", "response_time", "wait_response", "voice_recognition"]:
            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": f"device_id is required for '{test_type}' tests"
                })
            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Device '{device_id}' not found"
                })

        elif test_type == "routine_execution":
            if not routine_id:
                return json.dumps({
                    "success": False,
                    "error": "routine_id is required for 'routine_execution' tests"
                })
            if routine_id not in routines:
                return json.dumps({
                    "success": False,
                    "error": f"Routine '{routine_id}' not found"
                })

        elif test_type == "skill_invocation":
            if not skill_id:
                return json.dumps({
                    "success": False,
                    "error": "skill_id is required for 'skill_invocation' tests"
                })
            if skill_id not in skills:
                return json.dumps({
                    "success": False,
                    "error": f"Skill '{skill_id}' not found"
                })

        # Default test_parameters to empty dict
        test_parameters = test_parameters or {}

        # Execute test based on test type
        result = {
            "test_type": test_type,
            "timestamp": timestamp,
            "parameters_used": test_parameters,
            "status": "completed",
            "success": True
        }

        if test_type == "responsiveness":
            device = devices.get(device_id)
            # Check actual device responsiveness based on connection and signal
            conn_status = device.get("connection_status")
            signal_strength = device.get("signal_strength", 0)
            response_time_ms = device.get("response_time_ms", 150)

            if conn_status != "online":
                result["success"] = False
                result["status"] = "failed"
                result["response_time_ms"] = None
                result["result"] = f"Device '{device_id}' is {conn_status}, cannot test responsiveness."
            elif signal_strength < -80:
                result["success"] = False
                result["status"] = "failed"
                result["response_time_ms"] = response_time_ms
                result["result"] = f"Device '{device_id}' has very weak signal ({signal_strength} dBm), responsiveness test failed."
            else:
                result["response_time_ms"] = response_time_ms
                result["signal_strength_dbm"] = signal_strength
                result["result"] = f"Device '{device_id}' responded in {response_time_ms}ms with signal strength {signal_strength} dBm."

        elif test_type == "routine_execution":
            routine = routines.get(routine_id)
            # Check if routine can execute based on device availability
            device_actions = routine.get("device_actions", [])
            unavailable_devices = []

            for action in device_actions:
                action_device_id = action.get("device_id")
                if action_device_id in devices:
                    action_device = devices[action_device_id]
                    if action_device.get("connection_status") != "online":
                        unavailable_devices.append(action_device_id)

            if unavailable_devices:
                result["success"] = False
                result["status"] = "failed"
                result["unavailable_devices"] = unavailable_devices
                result["result"] = f"Routine '{routine_id}' cannot execute: devices {unavailable_devices} are offline."
            else:
                result["devices_tested"] = len(device_actions)
                result["result"] = f"Routine '{routine_id}' executed successfully with {len(device_actions)} device actions."

        elif test_type == "skill_invocation":
            skill = skills.get(skill_id)
            cmd = test_parameters.get("command", "unknown command")

            # Check skill status and compatibility
            skill_status = skill.get("status", "unknown")
            compatibility = skill.get("compatibility_status", "unknown")

            if skill_status != "enabled":
                result["success"] = False
                result["status"] = "failed"
                result["result"] = f"Skill '{skill_id}' is {skill_status}, cannot invoke."
            elif compatibility != "compatible":
                result["success"] = False
                result["status"] = "failed"
                result["result"] = f"Skill '{skill_id}' is {compatibility}, invocation may fail."
            else:
                result["command"] = cmd
                result["skill_status"] = skill_status
                result["result"] = f"Skill '{skill_id}' invoked successfully with command: '{cmd}'."

        elif test_type == "response_time":
            device = devices.get(device_id)
            response_time_ms = device.get("response_time_ms", 100)
            conn_status = device.get("connection_status")

            if conn_status != "online":
                result["success"] = False
                result["status"] = "failed"
                result["response_time_ms"] = None
                result["result"] = f"Device '{device_id}' is offline, cannot measure response time."
            else:
                result["response_time_ms"] = response_time_ms
                # Evaluate response time
                if response_time_ms < 200:
                    result["performance_rating"] = "excellent"
                elif response_time_ms < 500:
                    result["performance_rating"] = "good"
                elif response_time_ms < 1000:
                    result["performance_rating"] = "acceptable"
                else:
                    result["performance_rating"] = "poor"
                result["result"] = f"Device '{device_id}' response time: {response_time_ms}ms ({result['performance_rating']})."

        elif test_type == "wait_response":
            device = devices.get(device_id)
            wait_duration_sec = test_parameters.get("wait_duration_sec", 5)
            conn_status = device.get("connection_status")

            if conn_status != "online":
                result["success"] = False
                result["status"] = "failed"
                result["wait_duration_sec"] = wait_duration_sec
                result["result"] = f"Device '{device_id}' is offline, failed to maintain connection."
            else:
                result["wait_duration_sec"] = wait_duration_sec
                result["connection_maintained"] = True
                result["result"] = f"Device '{device_id}' maintained connection for {wait_duration_sec} seconds."

        elif test_type == "voice_recognition":
            device = devices.get(device_id)
            # Check if device has voice recognition capability
            capabilities = device.get("capabilities", [])
            has_voice = "voice_recognition" in capabilities or "voice_control" in capabilities

            if not has_voice:
                result["success"] = False
                result["status"] = "failed"
                result["accuracy_percent"] = 0
                result["result"] = f"Device '{device_id}' does not support voice recognition."
            else:
                # Get voice profile quality if available
                voice_quality = device.get("voice_profile_quality", 90)
                result["accuracy_percent"] = voice_quality
                if voice_quality >= 90:
                    result["quality_rating"] = "excellent"
                elif voice_quality >= 75:
                    result["quality_rating"] = "good"
                elif voice_quality >= 60:
                    result["quality_rating"] = "acceptable"
                else:
                    result["quality_rating"] = "poor"
                result["result"] = f"Voice recognition test completed for device '{device_id}': {voice_quality}% accuracy ({result['quality_rating']})."

        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Returns the schema for the TestDevice tool.
        """
        return {
            "type": "function",
            "function": {
                "name": "test_device",
                "description": (
                    "Tests device functionality, responsiveness, routine execution, "
                    "skill invocation, or voice recognition. The required parameters "
                    "depend on the test_type."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "test_type": {
                            "type": "string",
                            "description": (
                                "Specifies the type of test. Allowed values: "
                                "responsiveness, routine_execution, skill_invocation, "
                                "response_time, wait_response, voice_recognition."
                            )
                        },
                        "device_id": {
                            "type": "string",
                            "description": (
                                "Device ID for device-specific tests. Required for "
                                "responsiveness, response_time, wait_response, and "
                                "voice_recognition tests."
                            )
                        },
                        "routine_id": {
                            "type": "string",
                            "description": (
                                "Routine ID for routine tests. Required for "
                                "routine_execution tests."
                            )
                        },
                        "skill_id": {
                            "type": "string",
                            "description": (
                                "Skill ID for skill tests. Required for "
                                "skill_invocation tests."
                            )
                        },
                        "test_parameters": {
                            "type": "object",
                            "description": (
                                "Optional dictionary of additional parameters specific "
                                "to the chosen test_type (e.g., command, timeout)."
                            )
                        }
                    },
                    "required": ["test_type"]
                }
            }
        }
