import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class CompileReport(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], report_type: str, report_data: Dict[str, Any]) -> str:
        """
        Generate system reports and summaries in the smart home management system.
        Supports various report types including health, activity, diagnostics, and operational reports.
        """

        # Validate report_type
        valid_types = [
            "health", "update", "activity", "privacy_changes", "connection_diagnostic",
            "troubleshooting_steps", "device_recommendations", "network_change",
            "lifecycle", "energy", "performance", "routine_diagnostics",
            "device_performance", "conflict_diagnosis", "voice_profile",
            "announcement_preview", "announcement_delivery"
        ]

        if report_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid report_type '{report_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not report_data or not isinstance(report_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: report_data required and must be a dictionary"
            })

        # Get relevant tables
        devices = data.get("devices", {})
        routines = data.get("routines", {})
        access_logs = data.get("access_logs", {})

        if report_type == "health":
            # Generate device health report (SOP 6.7.5)
            device_list = report_data.get("device_list", list(devices.keys()))

            report_items = []
            for device_id in device_list:
                if device_id not in devices:
                    continue

                device = devices[device_id]

                # Calculate health metrics
                health_score = 100
                issues = []

                if device.get("connection_status") == "offline":
                    health_score -= 50
                    issues.append("Device offline")
                elif device.get("connection_status") == "error":
                    health_score -= 40
                    issues.append("Connection error")

                battery_level = device.get("battery_level")
                if battery_level is not None:
                    if battery_level < 10:
                        health_score -= 30
                        issues.append("Critical battery")
                    elif battery_level < 20:
                        health_score -= 15
                        issues.append("Low battery")

                signal_strength = device.get("signal_strength")
                if signal_strength and signal_strength < -70:
                    health_score -= 10
                    issues.append("Weak signal")

                health_status = "healthy" if health_score >= 80 else ("warning" if health_score >= 60 else "critical")

                report_items.append({
                    "device_id": device_id,
                    "device_name": device.get("device_name"),
                    "device_type": device.get("device_type"),
                    "health_score": max(0, health_score),
                    "health_status": health_status,
                    "connection_status": device.get("connection_status"),
                    "battery_level": battery_level,
                    "signal_strength": signal_strength,
                    "issues": issues,
                    "last_communication": device.get("last_communication")
                })

            summary = {
                "total_devices": len(report_items),
                "healthy": sum(1 for item in report_items if item["health_status"] == "healthy"),
                "warning": sum(1 for item in report_items if item["health_status"] == "warning"),
                "critical": sum(1 for item in report_items if item["health_status"] == "critical")
            }

            return json.dumps({
                "success": True,
                "report_type": "health",
                "timestamp": "2025-10-16T14:30:00",
                "summary": summary,
                "devices": report_items,
                "message": f"Health report generated for {len(report_items)} devices"
            })

        elif report_type == "update":
            # Generate firmware update report (SOP 6.7.2)
            devices_with_updates = []
            devices_current = []

            for device_id, device in devices.items():
                device_info = {
                    "device_id": device_id,
                    "device_name": device.get("device_name"),
                    "device_type": device.get("device_type"),
                    "current_version": device.get("firmware_version"),
                    "connection_status": device.get("connection_status")
                }

                if device.get("has_updates", False):
                    devices_with_updates.append(device_info)
                else:
                    devices_current.append(device_info)

            return json.dumps({
                "success": True,
                "report_type": "update",
                "timestamp": "2025-10-16T14:30:00",
                "summary": {
                    "total_devices": len(devices),
                    "devices_with_updates": len(devices_with_updates),
                    "devices_current": len(devices_current),
                    "update_coverage": round(len(devices_current) / len(devices) * 100, 2) if devices else 100
                },
                "devices_needing_updates": devices_with_updates,
                "devices_up_to_date": devices_current,
                "message": f"Update report: {len(devices_with_updates)} devices need updates"
            })

        elif report_type == "activity":
            # Generate activity report
            time_period = report_data.get("time_period", "last_24_hours")

            operation_counts = {}
            user_activity = {}

            for log in access_logs.values():
                # Count by action type
                action_type = log.get("action_type", "unknown")
                operation_counts[action_type] = operation_counts.get(action_type, 0) + 1

                # Count by user
                user_id = log.get("user_id")
                if user_id:
                    if user_id not in user_activity:
                        user_activity[user_id] = {"total": 0, "success": 0, "failure": 0}
                    user_activity[user_id]["total"] += 1
                    if log.get("outcome") == "success":
                        user_activity[user_id]["success"] += 1
                    else:
                        user_activity[user_id]["failure"] += 1

            return json.dumps({
                "success": True,
                "report_type": "activity",
                "timestamp": "2025-10-16T14:30:00",
                "time_period": time_period,
                "total_operations": len(access_logs),
                "operation_breakdown": operation_counts,
                "user_activity": user_activity,
                "message": f"Activity report for {time_period}"
            })

        elif report_type == "routine_diagnostics":
            # Generate routine diagnostic report (SOP 6.5.9)
            routine_id = report_data.get("routine_id")

            if not routine_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routine_id required for routine_diagnostics report"
                })

            if routine_id not in routines:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Routine not found - routine_id '{routine_id}' does not exist"
                })

            routine = routines[routine_id]

            # Parse device actions
            try:
                device_actions = json.loads(routine.get("device_actions", "[]"))
            except:
                device_actions = []

            # Validate each device action
            action_diagnostics = []
            issues_found = []

            for action in device_actions:
                device_id = action.get("device_id")
                action_type = action.get("action")

                diagnostic = {
                    "device_id": device_id,
                    "action": action_type,
                    "status": "valid"
                }

                if device_id not in devices:
                    diagnostic["status"] = "error"
                    diagnostic["issue"] = "Device not found"
                    issues_found.append(f"Device {device_id} not found")
                else:
                    device = devices[device_id]
                    if device.get("connection_status") == "offline":
                        diagnostic["status"] = "warning"
                        diagnostic["issue"] = "Device offline"
                        issues_found.append(f"Device {device.get('device_name')} is offline")
                    elif device.get("status") == "removed":
                        diagnostic["status"] = "error"
                        diagnostic["issue"] = "Device removed"
                        issues_found.append(f"Device {device.get('device_name')} removed")

                action_diagnostics.append(diagnostic)

            overall_status = "healthy" if not issues_found else ("warning" if any(d["status"] == "warning" for d in action_diagnostics) else "critical")

            return json.dumps({
                "success": True,
                "report_type": "routine_diagnostics",
                "timestamp": "2025-10-16T14:30:00",
                "routine_id": routine_id,
                "routine_name": routine.get("routine_name"),
                "routine_status": routine.get("status"),
                "overall_diagnostic_status": overall_status,
                "device_actions_count": len(device_actions),
                "action_diagnostics": action_diagnostics,
                "issues_found": issues_found,
                "message": f"Routine diagnostics: {len(issues_found)} issues found"
            })

        elif report_type == "connection_diagnostic":
            # Generate connection diagnostic report (SOP 6.9.1)
            device_id = report_data.get("device_id")

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required for connection_diagnostic report"
                })

            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            device = devices[device_id]

            # Analyze connection
            diagnostics = []
            recommendations = []

            connection_status = device.get("connection_status")
            if connection_status == "offline":
                diagnostics.append("Device is offline")
                recommendations.append("Check device power supply")
                recommendations.append("Verify network connectivity")

            signal_strength = device.get("signal_strength")
            if signal_strength and signal_strength < -70:
                diagnostics.append(f"Weak signal strength: {signal_strength} dBm")
                recommendations.append("Move device closer to router")
                recommendations.append("Consider adding WiFi extender")

            connectivity_method = device.get("connectivity_method")
            if connectivity_method == "WiFi":
                diagnostics.append("Device uses WiFi connectivity")
                recommendations.append("Check WiFi network stability")
                if device.get("network_frequency") == "2.4GHz":
                    recommendations.append("Consider switching to 5GHz for better performance")

            battery_level = device.get("battery_level")
            if battery_level is not None and battery_level < 20:
                diagnostics.append(f"Low battery: {battery_level}%")
                recommendations.append("Replace or recharge device battery")

            diagnostic_status = "issue_found" if len(recommendations) > 0 else "healthy"

            return json.dumps({
                "success": True,
                "report_type": "connection_diagnostic",
                "timestamp": "2025-10-16T14:30:00",
                "device_id": device_id,
                "device_name": device.get("device_name"),
                "diagnostic_status": diagnostic_status,
                "connection_status": connection_status,
                "signal_strength": signal_strength,
                "connectivity_method": connectivity_method,
                "diagnostics": diagnostics,
                "recommendations": recommendations,
                "message": f"Connection diagnostic: {len(recommendations)} recommendations"
            })

        else:
            # Generic report response for other report types
            return json.dumps({
                "success": True,
                "report_type": report_type,
                "timestamp": "2025-10-16T14:30:00",
                "report_data": report_data,
                "message": f"{report_type} report generated successfully"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "compile_report",
                "description": "Generate system reports and summaries in the smart home management system. Supports multiple report types: health reports with device health scores and issue identification (SOP 6.7.5), update reports showing firmware status, activity reports with operation and user analytics, privacy change summaries, connection diagnostics for troubleshooting network issues (SOP 6.9.1), troubleshooting steps for common problems, device recommendations based on usage patterns, network change impact analysis, device lifecycle reports, energy consumption analysis (SOP 6.7.8), performance reports, routine diagnostics for debugging automation failures (SOP 6.5.9), device performance analysis (SOP 6.9.2), conflict diagnosis for routine and connectivity conflicts (SOP 6.9.3), voice profile quality reports (SOP 6.10.1), announcement preview and delivery confirmation reports (SOP 6.10.2).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "report_type": {
                            "type": "string",
                            "description": "Type of report to generate",
                            "enum": ["health", "update", "activity", "privacy_changes", "connection_diagnostic", "troubleshooting_steps", "device_recommendations", "network_change", "lifecycle", "energy", "performance", "routine_diagnostics", "device_performance", "conflict_diagnosis", "voice_profile", "announcement_preview", "announcement_delivery"]
                        },
                        "report_data": {
                            "type": "object",
                            "description": "Report-specific data. For health: {device_list}. For routine_diagnostics: {routine_id}. For connection_diagnostic: {device_id}. For activity: {time_period}",
                            "properties": {
                                "device_list": {
                                    "type": "array",
                                    "description": "List of device IDs to include in report"
                                },
                                "routine_id": {
                                    "type": "string",
                                    "description": "Routine ID for routine diagnostics"
                                },
                                "device_id": {
                                    "type": "string",
                                    "description": "Device ID for device-specific reports"
                                },
                                "time_period": {
                                    "type": "string",
                                    "description": "Time period for activity reports"
                                }
                            }
                        }
                    },
                    "required": ["report_type", "report_data"]
                }
            }
        }
