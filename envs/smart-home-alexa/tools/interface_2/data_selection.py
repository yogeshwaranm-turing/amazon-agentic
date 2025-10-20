import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DataSelection(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filter_type: str, filter_criteria: Dict[str, Any]) -> str:
        """
        Filter entities by specific criteria in the smart home management system.
        Supports filtering devices by battery level, status, errors, type, and custom criteria.
        """

        # Validate filter_type
        valid_types = ["devices_by_battery", "devices_by_status", "devices_by_errors", "devices_by_type", "devices_by_criterion", "threshold", "critical_issues"]
        if filter_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid filter_type '{filter_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not filter_criteria or not isinstance(filter_criteria, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: filter_criteria required and must be a dictionary"
            })

        # Get devices table
        devices = data.get("devices", {})

        if filter_type == "devices_by_battery":
            # Filter devices by battery level threshold (SOP 6.7.6)
            threshold = filter_criteria.get("threshold", 20)

            if not isinstance(threshold, (int, float)) or threshold < 0 or threshold > 100:
                return json.dumps({
                    "success": False,
                    "error": "Halt: threshold must be a number between 0 and 100"
                })

            # Filter battery-powered devices below threshold
            filtered_devices = []
            for device_id, device in devices.items():
                battery_level = device.get("battery_level")
                if battery_level is not None and battery_level < threshold:
                    filtered_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        "battery_level": battery_level,
                        "battery_status": device.get("battery_status"),
                        "connection_status": device.get("connection_status")
                    })

            # Sort by battery level (lowest first)
            filtered_devices.sort(key=lambda x: x["battery_level"])

            return json.dumps({
                "success": True,
                "filter_type": "devices_by_battery",
                "threshold": threshold,
                "devices_found": len(filtered_devices),
                "devices": filtered_devices,
                "message": f"Found {len(filtered_devices)} devices with battery below {threshold}%"
            })

        elif filter_type == "devices_by_status":
            # Filter devices by connection status
            status = filter_criteria.get("status")

            if not status:
                return json.dumps({
                    "success": False,
                    "error": "Halt: status required in filter_criteria for devices_by_status"
                })

            # Validate status
            valid_statuses = ["registered", "online", "offline", "error"]
            if status not in valid_statuses:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                })

            # Filter devices by status
            filtered_devices = []
            for device_id, device in devices.items():
                if device.get("connection_status") == status:
                    filtered_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        "connection_status": device.get("connection_status"),
                        "last_communication": device.get("last_communication")
                    })

            return json.dumps({
                "success": True,
                "filter_type": "devices_by_status",
                "status": status,
                "devices_found": len(filtered_devices),
                "devices": filtered_devices,
                "message": f"Found {len(filtered_devices)} devices with status '{status}'"
            })

        elif filter_type == "devices_by_errors":
            # Filter devices with error conditions
            error_type = filter_criteria.get("error_type", "all")

            filtered_devices = []
            for device_id, device in devices.items():
                error_conditions = device.get("error_conditions")

                # Check for errors
                has_error = (
                    device.get("connection_status") == "error" or
                    (error_conditions and error_conditions != "null" and error_conditions != "[]")
                )

                if has_error:
                    # Parse error conditions if JSON
                    try:
                        errors = json.loads(error_conditions) if isinstance(error_conditions, str) else error_conditions
                    except:
                        errors = [error_conditions] if error_conditions else []

                    filtered_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        "connection_status": device.get("connection_status"),
                        "error_conditions": errors
                    })

            return json.dumps({
                "success": True,
                "filter_type": "devices_by_errors",
                "error_type": error_type,
                "devices_found": len(filtered_devices),
                "devices": filtered_devices,
                "message": f"Found {len(filtered_devices)} devices with errors"
            })

        elif filter_type == "devices_by_type":
            # Filter devices by device type (SOP 6.1.3)
            device_type = filter_criteria.get("device_type")

            if not device_type:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_type required in filter_criteria for devices_by_type"
                })

            # Filter devices by type
            filtered_devices = []
            for device_id, device in devices.items():
                if device.get("device_type") == device_type:
                    filtered_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        "manufacturer": device.get("manufacturer"),
                        "model": device.get("model"),
                        "connection_status": device.get("connection_status")
                    })

            return json.dumps({
                "success": True,
                "filter_type": "devices_by_type",
                "device_type": device_type,
                "devices_found": len(filtered_devices),
                "devices": filtered_devices,
                "message": f"Found {len(filtered_devices)} devices of type '{device_type}'"
            })

        elif filter_type == "devices_by_criterion":
            # Filter devices by custom criterion (SOP 6.1.2)
            criterion = filter_criteria.get("criterion")
            value = filter_criteria.get("value")

            if not criterion:
                return json.dumps({
                    "success": False,
                    "error": "Halt: criterion required in filter_criteria for devices_by_criterion"
                })

            # Filter devices matching criterion
            filtered_devices = []
            for device_id, device in devices.items():
                if criterion in device and device.get(criterion) == value:
                    filtered_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        criterion: device.get(criterion)
                    })

            return json.dumps({
                "success": True,
                "filter_type": "devices_by_criterion",
                "criterion": criterion,
                "value": value,
                "devices_found": len(filtered_devices),
                "devices": filtered_devices,
                "message": f"Found {len(filtered_devices)} devices matching {criterion}={value}"
            })

        elif filter_type == "threshold":
            # Generic threshold filtering
            field = filter_criteria.get("field")
            operator = filter_criteria.get("operator", "<")
            threshold_value = filter_criteria.get("value")

            if not field or threshold_value is None:
                return json.dumps({
                    "success": False,
                    "error": "Halt: field and value required in filter_criteria for threshold filter"
                })

            filtered_devices = []
            for device_id, device in devices.items():
                field_value = device.get(field)
                if field_value is None:
                    continue

                # Apply operator
                matches = False
                try:
                    if operator == "<" and field_value < threshold_value:
                        matches = True
                    elif operator == "<=" and field_value <= threshold_value:
                        matches = True
                    elif operator == ">" and field_value > threshold_value:
                        matches = True
                    elif operator == ">=" and field_value >= threshold_value:
                        matches = True
                    elif operator == "==" and field_value == threshold_value:
                        matches = True
                except:
                    pass

                if matches:
                    filtered_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        field: field_value
                    })

            return json.dumps({
                "success": True,
                "filter_type": "threshold",
                "field": field,
                "operator": operator,
                "threshold_value": threshold_value,
                "devices_found": len(filtered_devices),
                "devices": filtered_devices,
                "message": f"Found {len(filtered_devices)} devices where {field} {operator} {threshold_value}"
            })

        elif filter_type == "critical_issues":
            # Filter devices with critical issues
            critical_devices = []

            for device_id, device in devices.items():
                issues = []
                is_critical = False

                # Check for critical conditions
                if device.get("connection_status") == "offline":
                    issues.append("Device offline")
                    is_critical = True

                battery_level = device.get("battery_level")
                if battery_level is not None and battery_level < 10:
                    issues.append("Critical battery level")
                    is_critical = True

                if device.get("connection_status") == "error":
                    issues.append("Connection error")
                    is_critical = True

                if is_critical:
                    critical_devices.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        "critical_issues": issues,
                        "connection_status": device.get("connection_status"),
                        "battery_level": battery_level
                    })

            return json.dumps({
                "success": True,
                "filter_type": "critical_issues",
                "devices_found": len(critical_devices),
                "devices": critical_devices,
                "message": f"Found {len(critical_devices)} devices with critical issues"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "data_selection",
                "description": "Select entities by specific criteria in the smart home management system. Filters devices by battery level threshold identifying low-battery devices for proactive maintenance (SOP 6.7.6). Filters devices by connection status (online/offline/error/registered) for health monitoring (SOP 6.1.2). Filters devices with error conditions for troubleshooting and diagnostics (SOP 6.9.1). Filters devices by device type (light/lock/thermostat/camera/sensor/speaker/switch/plug/appliance) for inventory and management (SOP 6.1.3). Filters devices by custom criterion and value for flexible querying. Applies threshold filtering with operators (<, <=, >, >=, ==) on numeric fields like signal_strength, battery_level. Identifies devices with critical issues (offline, critical battery, errors) for immediate attention.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filter_type": {
                            "type": "string",
                            "description": "Type of filtering to apply",
                            "enum": ["devices_by_battery", "devices_by_status", "devices_by_errors", "devices_by_type", "devices_by_criterion", "threshold", "critical_issues"]
                        },
                        "filter_criteria": {
                            "type": "object",
                            "description": "Filter-specific criteria. For devices_by_battery: {threshold}. For devices_by_status: {status}. For devices_by_errors: {error_type}. For devices_by_type: {device_type}. For devices_by_criterion: {criterion, value}. For threshold: {field, operator, value}",
                            "properties": {
                                "threshold": {
                                    "type": "number",
                                    "description": "Battery level threshold (0-100)"
                                },
                                "status": {
                                    "type": "string",
                                    "description": "Connection status to filter by",
                                    "enum": ["registered", "online", "offline", "error"]
                                },
                                "error_type": {
                                    "type": "string",
                                    "description": "Type of error to filter (or 'all')"
                                },
                                "device_type": {
                                    "type": "string",
                                    "description": "Device type to filter by"
                                },
                                "criterion": {
                                    "type": "string",
                                    "description": "Field name to filter on"
                                },
                                "value": {
                                    "description": "Value to match for criterion"
                                },
                                "field": {
                                    "type": "string",
                                    "description": "Numeric field for threshold filtering"
                                },
                                "operator": {
                                    "type": "string",
                                    "description": "Comparison operator for threshold",
                                    "enum": ["<", "<=", ">", ">=", "=="]
                                }
                            }
                        }
                    },
                    "required": ["filter_type", "filter_criteria"]
                }
            }
        }
