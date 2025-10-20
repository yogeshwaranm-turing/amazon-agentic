import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class TrackSystem(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], monitoring_type: str, monitoring_parameters: Dict[str, Any] = None) -> str:
        """
        Monitor system health, activity, and logs in the smart home management system.
        Generates summary reports for health status, activity patterns, and firmware update status
        across all devices and system components.
        """

        # Validate monitoring_type
        valid_types = ["health_summary", "activity_summary", "update_summary"]
        if monitoring_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid monitoring_type '{monitoring_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not monitoring_parameters:
            monitoring_parameters = {}

        # Get relevant tables from schema
        devices = data.get("devices", {})
        routines = data.get("routines", {})
        users = data.get("users", {})
        access_logs = data.get("access_logs", {})

        if monitoring_type == "health_summary":
            # Calculate overall system health summary

            # Device health statistics
            total_devices = len(devices)
            online_devices = sum(1 for d in devices.values() if d.get("connection_status") == "online")
            offline_devices = sum(1 for d in devices.values() if d.get("connection_status") == "offline")
            error_devices = sum(1 for d in devices.values() if d.get("connection_status") == "error")

            # Battery-powered device statistics
            battery_devices = [d for d in devices.values() if d.get("battery_level") is not None]
            low_battery_devices = sum(1 for d in battery_devices if d.get("battery_level", 100) < 20)
            critical_battery_devices = sum(1 for d in battery_devices if d.get("battery_level", 100) < 10)

            # Signal strength statistics
            weak_signal_devices = sum(1 for d in devices.values()
                                     if d.get("signal_strength") and d.get("signal_strength") < -70)

            # Routine statistics
            total_routines = len(routines)
            enabled_routines = sum(1 for r in routines.values() if r.get("status") == "enabled")
            disabled_routines = sum(1 for r in routines.values() if r.get("status") == "disabled")

            # Calculate health scores
            device_health_score = (online_devices / total_devices * 100) if total_devices > 0 else 100
            battery_health_score = ((len(battery_devices) - critical_battery_devices) / len(battery_devices) * 100) if battery_devices else 100
            routine_health_score = (enabled_routines / total_routines * 100) if total_routines > 0 else 100
            overall_health_score = (device_health_score * 0.5 + battery_health_score * 0.3 + routine_health_score * 0.2)

            # Determine health status
            if overall_health_score >= 90:
                health_status = "healthy"
            elif overall_health_score >= 70:
                health_status = "warning"
            else:
                health_status = "critical"

            # Identify critical issues
            critical_issues = []
            if offline_devices > 0:
                critical_issues.append(f"{offline_devices} devices offline")
            if error_devices > 0:
                critical_issues.append(f"{error_devices} devices in error state")
            if critical_battery_devices > 0:
                critical_issues.append(f"{critical_battery_devices} devices with critical battery")
            if weak_signal_devices > 5:
                critical_issues.append(f"{weak_signal_devices} devices with weak signal")

            return json.dumps({
                "success": True,
                "monitoring_type": "health_summary",
                "timestamp": "2025-10-16T14:30:00",
                "overall_health_score": round(overall_health_score, 2),
                "health_status": health_status,
                "device_statistics": {
                    "total": total_devices,
                    "online": online_devices,
                    "offline": offline_devices,
                    "error": error_devices,
                    "device_health_score": round(device_health_score, 2)
                },
                "battery_statistics": {
                    "total_battery_devices": len(battery_devices),
                    "low_battery": low_battery_devices,
                    "critical_battery": critical_battery_devices,
                    "battery_health_score": round(battery_health_score, 2)
                },
                "routine_statistics": {
                    "total": total_routines,
                    "enabled": enabled_routines,
                    "disabled": disabled_routines,
                    "routine_health_score": round(routine_health_score, 2)
                },
                "network_statistics": {
                    "weak_signal_devices": weak_signal_devices
                },
                "critical_issues": critical_issues,
                "message": f"System health: {health_status} ({round(overall_health_score, 1)}% score)"
            })

        elif monitoring_type == "activity_summary":
            # Calculate system activity summary
            time_period = monitoring_parameters.get("time_period", "last_24_hours")

            # Count recent access logs (simulated filtering)
            total_log_entries = len(access_logs)
            successful_operations = sum(1 for log in access_logs.values() if log.get("outcome") == "success")
            failed_operations = sum(1 for log in access_logs.values() if log.get("outcome") == "failure")

            # Count operations by type
            operation_counts = {}
            for log in access_logs.values():
                action_type = log.get("action_type", "unknown")
                operation_counts[action_type] = operation_counts.get(action_type, 0) + 1

            # Top operations
            top_operations = sorted(operation_counts.items(), key=lambda x: x[1], reverse=True)[:5]

            # Active users
            active_users = set()
            for log in access_logs.values():
                user_id = log.get("user_id")
                if user_id:
                    active_users.add(user_id)

            # Calculate activity metrics
            success_rate = (successful_operations / total_log_entries * 100) if total_log_entries > 0 else 100

            return json.dumps({
                "success": True,
                "monitoring_type": "activity_summary",
                "timestamp": "2025-10-16T14:30:00",
                "time_period": time_period,
                "total_operations": total_log_entries,
                "successful_operations": successful_operations,
                "failed_operations": failed_operations,
                "success_rate": round(success_rate, 2),
                "active_users_count": len(active_users),
                "top_operations": [{"operation": op[0], "count": op[1]} for op in top_operations],
                "operation_breakdown": operation_counts,
                "message": f"Activity summary: {total_log_entries} operations in {time_period}"
            })

        elif monitoring_type == "update_summary":
            # Calculate firmware update summary
            devices_with_updates = sum(1 for d in devices.values() if d.get("has_updates", False))
            devices_current = total_devices - devices_with_updates if total_devices > 0 else 0
            total_devices = len(devices)

            # Group devices by update status
            devices_needing_update = []
            for device_id, device in devices.items():
                if device.get("has_updates", False):
                    devices_needing_update.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "device_type": device.get("device_type"),
                        "current_version": device.get("firmware_version"),
                        "connection_status": device.get("connection_status")
                    })

            # Calculate update metrics
            update_coverage = (devices_current / total_devices * 100) if total_devices > 0 else 100
            critical_updates = sum(1 for d in devices_needing_update if d.get("connection_status") in ["online", "offline"])

            return json.dumps({
                "success": True,
                "monitoring_type": "update_summary",
                "timestamp": "2025-10-16T14:30:00",
                "total_devices": total_devices,
                "devices_with_updates": devices_with_updates,
                "devices_current": devices_current,
                "update_coverage": round(update_coverage, 2),
                "critical_updates": critical_updates,
                "devices_needing_update": devices_needing_update,
                "message": f"Update summary: {devices_with_updates} devices need updates"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "track_system",
                "description": "Monitor system health, activity, and logs in the smart home management system. Generates health summary calculating overall system health score from device connectivity (online/offline/error), battery levels (low/critical), signal strength, and routine status, with health classification (healthy/warning/critical) and critical issue identification (SOP 6.7.1). Creates activity summary tracking successful/failed operations, operation types distribution, active users, and success rate over specified time period for security monitoring and usage analysis. Produces update summary showing firmware update status across devices, identifying devices needing updates, calculating update coverage percentage, and prioritizing critical updates for security patches.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "monitoring_type": {
                            "type": "string",
                            "description": "Type of monitoring summary to generate",
                            "enum": ["health_summary", "activity_summary", "update_summary"]
                        },
                        "monitoring_parameters": {
                            "type": "object",
                            "description": "Optional monitoring parameters. For activity_summary: {time_period} (default: 'last_24_hours')",
                            "properties": {
                                "time_period": {
                                    "type": "string",
                                    "description": "Time period for activity analysis (e.g., 'last_24_hours', 'last_7_days')"
                                }
                            }
                        }
                    },
                    "required": ["monitoring_type"]
                }
            }
        }
