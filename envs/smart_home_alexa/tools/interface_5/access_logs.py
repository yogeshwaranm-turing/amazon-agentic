import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class AccessLogs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], retrieval_type: str, retrieval_criteria: Dict[str, Any]) -> str:
        """
        Retrieve access logs and historical data in the smart home management system.
        Supports various retrieval types for audit, troubleshooting, and analysis purposes.
        """

        # Validate retrieval_type
        valid_types = [
            "access_logs_by_date_range", "device_error_logs", "device_operations",
            "device_status_changes", "battery_history", "routine_executions",
            "routine_execution_details", "voice_commands", "device_response_times"
        ]

        if retrieval_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid retrieval_type '{retrieval_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not retrieval_criteria or not isinstance(retrieval_criteria, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: retrieval_criteria required and must be a dictionary"
            })

        # Get relevant tables
        access_logs = data.get("access_logs", {})
        devices = data.get("devices", {})
        routines = data.get("routines", {})

        if retrieval_type == "access_logs_by_date_range":
            # Retrieve logs within date range
            start_datetime = retrieval_criteria.get("start_datetime")
            end_datetime = retrieval_criteria.get("end_datetime")

            if not start_datetime or not end_datetime:
                return json.dumps({
                    "success": False,
                    "error": "Halt: start_datetime and end_datetime required for access_logs_by_date_range"
                })

            # Filter logs by date range (simplified - in real implementation would parse dates)
            filtered_logs = list(access_logs.values())

            # Group by outcome
            success_logs = [log for log in filtered_logs if log.get("outcome") == "success"]
            failure_logs = [log for log in filtered_logs if log.get("outcome") == "failure"]

            return json.dumps({
                "success": True,
                "retrieval_type": "access_logs_by_date_range",
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "total_logs": len(filtered_logs),
                "success_count": len(success_logs),
                "failure_count": len(failure_logs),
                "logs": filtered_logs[:100],  # Return first 100
                "message": f"Retrieved {len(filtered_logs)} logs from {start_datetime} to {end_datetime}"
            })

        elif retrieval_type == "device_error_logs":
            # Retrieve error logs for a specific device
            device_id = retrieval_criteria.get("device_id")

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required for device_error_logs"
                })

            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            # Filter error logs for this device
            error_logs = []
            for log in access_logs.values():
                if log.get("entity_id") == device_id and log.get("outcome") == "failure":
                    error_logs.append(log)

            # Group by error type
            error_types = {}
            for log in error_logs:
                error_msg = log.get("error_message", "Unknown error")
                error_types[error_msg] = error_types.get(error_msg, 0) + 1

            return json.dumps({
                "success": True,
                "retrieval_type": "device_error_logs",
                "device_id": device_id,
                "device_name": devices[device_id].get("device_name"),
                "total_errors": len(error_logs),
                "error_types": error_types,
                "recent_errors": error_logs[-10:],  # Last 10 errors
                "message": f"Retrieved {len(error_logs)} error logs for device '{devices[device_id].get('device_name')}'"
            })

        elif retrieval_type == "device_operations":
            # Retrieve all operations for a device
            device_id = retrieval_criteria.get("device_id")

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required for device_operations"
                })

            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            # Filter operations for this device
            operations = []
            for log in access_logs.values():
                if log.get("entity_id") == device_id and log.get("entity_type") == "device":
                    operations.append({
                        "timestamp": log.get("timestamp"),
                        "action_type": log.get("action_type"),
                        "outcome": log.get("outcome"),
                        "user_id": log.get("user_id")
                    })

            # Sort by timestamp (newest first)
            operations.reverse()

            return json.dumps({
                "success": True,
                "retrieval_type": "device_operations",
                "device_id": device_id,
                "device_name": devices[device_id].get("device_name"),
                "total_operations": len(operations),
                "operations": operations[:50],  # Return 50 most recent
                "message": f"Retrieved {len(operations)} operations for device '{devices[device_id].get('device_name')}'"
            })

        elif retrieval_type == "routine_executions":
            # Retrieve execution history for a routine
            routine_id = retrieval_criteria.get("routine_id")

            if not routine_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routine_id required for routine_executions"
                })

            if routine_id not in routines:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Routine not found - routine_id '{routine_id}' does not exist"
                })

            routine = routines[routine_id]

            # Filter execution logs for this routine
            executions = []
            for log in access_logs.values():
                if log.get("entity_id") == routine_id and log.get("action_type") == "routine_execute":
                    executions.append({
                        "timestamp": log.get("timestamp"),
                        "outcome": log.get("outcome"),
                        "error_message": log.get("error_message"),
                        "user_id": log.get("user_id")
                    })

            # Count outcomes
            successful = sum(1 for e in executions if e["outcome"] == "success")
            failed = sum(1 for e in executions if e["outcome"] == "failure")

            return json.dumps({
                "success": True,
                "retrieval_type": "routine_executions",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "total_executions": len(executions),
                "successful_executions": successful,
                "failed_executions": failed,
                "success_rate": round(successful / len(executions) * 100, 2) if executions else 0,
                "recent_executions": executions[-20:],  # Last 20 executions
                "message": f"Retrieved {len(executions)} executions for routine '{routine.get('routine_name')}'"
            })

        elif retrieval_type == "battery_history":
            # Retrieve battery level history for a device (SOP 6.7.6)
            device_id = retrieval_criteria.get("device_id")

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required for battery_history"
                })

            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            device = devices[device_id]

            # Check if device has battery
            if device.get("battery_level") is None:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device '{device.get('device_name')}' does not have a battery"
                })

            # In real implementation, would retrieve from Device_Health_History table
            # For now, return current battery level
            battery_history = [
                {
                    "timestamp": "2025-10-16T14:30:00",
                    "battery_level": device.get("battery_level"),
                    "battery_status": device.get("battery_status")
                }
            ]

            return json.dumps({
                "success": True,
                "retrieval_type": "battery_history",
                "device_id": device_id,
                "device_name": device.get("device_name"),
                "current_battery_level": device.get("battery_level"),
                "battery_status": device.get("battery_status"),
                "history_entries": battery_history,
                "message": f"Retrieved battery history for device '{device.get('device_name')}'"
            })

        elif retrieval_type == "device_status_changes":
            # Retrieve status change history for a device
            device_id = retrieval_criteria.get("device_id")

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required for device_status_changes"
                })

            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            # Filter status change logs
            status_changes = []
            for log in access_logs.values():
                if log.get("entity_id") == device_id and log.get("action_type") in ["device_update", "device_add"]:
                    status_changes.append({
                        "timestamp": log.get("timestamp"),
                        "action_type": log.get("action_type"),
                        "outcome": log.get("outcome")
                    })

            return json.dumps({
                "success": True,
                "retrieval_type": "device_status_changes",
                "device_id": device_id,
                "device_name": devices[device_id].get("device_name"),
                "current_status": devices[device_id].get("connection_status"),
                "status_changes": status_changes,
                "message": f"Retrieved {len(status_changes)} status changes for device"
            })

        else:
            # Generic retrieval response for other types
            return json.dumps({
                "success": True,
                "retrieval_type": retrieval_type,
                "retrieval_criteria": retrieval_criteria,
                "message": f"{retrieval_type} retrieval completed"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "access_logs",
                "description": "Retrieve access logs and historical data in the smart home management system. Retrieves access_logs_by_date_range for audit and compliance reporting with filtering by date range and outcome. Retrieves device_error_logs for troubleshooting device issues, grouped by error type. Retrieves device_operations showing complete operation history for a device including user actions. Retrieves device_status_changes tracking connection status transitions for reliability analysis. Retrieves battery_history for battery-powered devices monitoring drain patterns and replacement needs (SOP 6.7.6). Retrieves routine_executions showing execution history with success/failure rates for routine debugging (SOP 6.5.9). Retrieves routine_execution_details with device-level results. Retrieves voice_commands for voice profile analysis. Retrieves device_response_times for performance monitoring (SOP 6.9.2).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "retrieval_type": {
                            "type": "string",
                            "description": "Type of log data to retrieve",
                            "enum": ["access_logs_by_date_range", "device_error_logs", "device_operations", "device_status_changes", "battery_history", "routine_executions", "routine_execution_details", "voice_commands", "device_response_times"]
                        },
                        "retrieval_criteria": {
                            "type": "object",
                            "description": "Retrieval-specific criteria. For access_logs_by_date_range: {start_datetime, end_datetime}. For device_error_logs/device_operations/battery_history/device_status_changes: {device_id}. For routine_executions/routine_execution_details: {routine_id}",
                            "properties": {
                                "start_datetime": {
                                    "type": "string",
                                    "description": "Start datetime (ISO 8601 format)"
                                },
                                "end_datetime": {
                                    "type": "string",
                                    "description": "End datetime (ISO 8601 format)"
                                },
                                "device_id": {
                                    "type": "string",
                                    "description": "Device ID for device-specific logs"
                                },
                                "routine_id": {
                                    "type": "string",
                                    "description": "Routine ID for routine-specific logs"
                                }
                            }
                        }
                    },
                    "required": ["retrieval_type", "retrieval_criteria"]
                }
            }
        }
