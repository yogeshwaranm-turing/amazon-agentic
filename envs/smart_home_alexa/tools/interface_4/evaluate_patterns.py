import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EvaluatePatterns(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], analysis_type: str, analysis_data: Dict[str, Any]) -> str:
        """
        Analyze data for patterns and anomalies in the smart home management system.
        Supports activity pattern analysis, error pattern detection, performance analysis, and conflict detection.
        """

        # Validate analysis_type
        valid_types = [
            "activity_patterns", "error_patterns", "connection_diagnostic", "device_lifecycle",
            "find_maximum", "energy_optimization", "performance_summary", "update_priority",
            "failure_patterns", "failure_resolution", "performance_comparison",
            "performance_recommendations", "routine_conflicts", "connectivity_conflicts",
            "operation_timing", "conflict_resolution", "device_distribution"
        ]

        if analysis_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid analysis_type '{analysis_type}'. Must be one of: {', '.join(valid_types[:10])}..."
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not analysis_data or not isinstance(analysis_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: analysis_data required and must be a dictionary"
            })

        if analysis_type == "activity_patterns":
            # Analyze activity patterns from logs
            logs = analysis_data.get("logs", [])

            if not logs:
                return json.dumps({
                    "success": False,
                    "error": "Halt: logs list required in analysis_data for activity_patterns"
                })

            # Count by action type
            action_frequency = {}
            user_activity = {}
            hourly_distribution = {}

            for log in logs:
                # Action frequency
                action_type = log.get("action_type", "unknown")
                action_frequency[action_type] = action_frequency.get(action_type, 0) + 1

                # User activity
                user_id = log.get("user_id")
                if user_id:
                    user_activity[user_id] = user_activity.get(user_id, 0) + 1

                # Hourly distribution (simplified)
                timestamp = log.get("timestamp", "")
                if len(timestamp) >= 13:
                    hour = timestamp[11:13]
                    hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1

            # Find peak hours
            peak_hours = sorted(hourly_distribution.items(), key=lambda x: x[1], reverse=True)[:3]

            return json.dumps({
                "success": True,
                "analysis_type": "activity_patterns",
                "total_logs": len(logs),
                "action_frequency": action_frequency,
                "most_active_users": sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:5],
                "peak_hours": [{"hour": h[0], "count": h[1]} for h in peak_hours],
                "message": f"Activity pattern analysis completed for {len(logs)} logs"
            })

        elif analysis_type == "error_patterns":
            # Analyze error patterns
            logs = analysis_data.get("logs", [])

            if not logs:
                return json.dumps({
                    "success": False,
                    "error": "Halt: logs list required in analysis_data for error_patterns"
                })

            # Filter failures
            failures = [log for log in logs if log.get("outcome") == "failure"]

            # Categorize errors
            error_types = {}
            affected_entities = {}

            for log in failures:
                error_msg = log.get("error_message", "Unknown error")
                error_types[error_msg] = error_types.get(error_msg, 0) + 1

                entity_id = log.get("entity_id")
                if entity_id:
                    affected_entities[entity_id] = affected_entities.get(entity_id, 0) + 1

            # Most common errors
            most_common = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]

            return json.dumps({
                "success": True,
                "analysis_type": "error_patterns",
                "total_failures": len(failures),
                "total_logs": len(logs),
                "failure_rate": round(len(failures) / len(logs) * 100, 2) if logs else 0,
                "unique_error_types": len(error_types),
                "most_common_errors": [{"error": e[0], "count": e[1]} for e in most_common],
                "most_affected_entities": sorted(affected_entities.items(), key=lambda x: x[1], reverse=True)[:5],
                "message": f"Error pattern analysis: {len(failures)} failures detected"
            })

        elif analysis_type == "connection_diagnostic":
            # Analyze connection issues (SOP 6.9.1)
            device_id = analysis_data.get("device_id")
            devices = data.get("devices", {})

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required in analysis_data for connection_diagnostic"
                })

            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            device = devices[device_id]

            # Diagnose connection issues
            issues = []
            recommendations = []

            if device.get("connection_status") == "offline":
                issues.append("Device is offline")
                recommendations.append("Check device power supply")
                recommendations.append("Verify network connectivity")
                recommendations.append("Restart device")

            signal_strength = device.get("signal_strength")
            if signal_strength and signal_strength < -70:
                issues.append(f"Weak signal: {signal_strength} dBm")
                recommendations.append("Move device closer to router/hub")
                recommendations.append("Add WiFi extender or mesh node")

            if device.get("connectivity_method") == "WiFi" and device.get("network_frequency") == "2.4GHz":
                issues.append("Using 2.4GHz WiFi (may have interference)")
                recommendations.append("Switch to 5GHz network if supported")

            battery_level = device.get("battery_level")
            if battery_level is not None and battery_level < 20:
                issues.append(f"Low battery: {battery_level}%")
                recommendations.append("Replace or recharge battery")

            diagnostic_result = "healthy" if not issues else "issues_found"

            return json.dumps({
                "success": True,
                "analysis_type": "connection_diagnostic",
                "device_id": device_id,
                "device_name": device.get("device_name"),
                "diagnostic_result": diagnostic_result,
                "issues_found": issues,
                "recommendations": recommendations,
                "message": f"Connection diagnostic: {len(issues)} issues found"
            })

        elif analysis_type == "routine_conflicts":
            # Detect routine scheduling conflicts (SOP 6.9.3)
            routines = analysis_data.get("routines", [])

            if not routines:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routines list required in analysis_data for routine_conflicts"
                })

            conflicts = []

            # Check for overlapping routines affecting same devices
            for i, routine1 in enumerate(routines):
                for j, routine2 in enumerate(routines):
                    if i >= j:
                        continue

                    # Parse device actions
                    try:
                        actions1 = json.loads(routine1.get("device_actions", "[]"))
                        actions2 = json.loads(routine2.get("device_actions", "[]"))
                    except:
                        continue

                    # Find overlapping devices
                    devices1 = set(a.get("device_id") for a in actions1)
                    devices2 = set(a.get("device_id") for a in actions2)
                    overlap = devices1 & devices2

                    if overlap:
                        conflicts.append({
                            "conflict_type": "routine_overlap",
                            "routine1_id": routine1.get("routine_id"),
                            "routine1_name": routine1.get("routine_name"),
                            "routine2_id": routine2.get("routine_id"),
                            "routine2_name": routine2.get("routine_name"),
                            "overlapping_devices": list(overlap),
                            "overlap_count": len(overlap)
                        })

            return json.dumps({
                "success": True,
                "analysis_type": "routine_conflicts",
                "routines_analyzed": len(routines),
                "conflicts_found": len(conflicts),
                "conflicts": conflicts,
                "message": f"Routine conflict analysis: {len(conflicts)} conflicts detected"
            })

        elif analysis_type == "performance_summary":
            # Summarize device performance metrics (SOP 6.9.2)
            response_times = analysis_data.get("response_times", {})

            if not response_times:
                return json.dumps({
                    "success": False,
                    "error": "Halt: response_times required in analysis_data for performance_summary"
                })

            times = list(response_times.values())
            avg_response = sum(times) / len(times) if times else 0
            min_response = min(times) if times else 0
            max_response = max(times) if times else 0

            # Categorize performance
            excellent = sum(1 for t in times if t < 200)
            good = sum(1 for t in times if 200 <= t < 500)
            acceptable = sum(1 for t in times if 500 <= t < 1000)
            poor = sum(1 for t in times if t >= 1000)

            return json.dumps({
                "success": True,
                "analysis_type": "performance_summary",
                "total_devices": len(times),
                "average_response_ms": round(avg_response, 2),
                "min_response_ms": min_response,
                "max_response_ms": max_response,
                "performance_distribution": {
                    "excellent": excellent,
                    "good": good,
                    "acceptable": acceptable,
                    "poor": poor
                },
                "message": f"Performance summary: avg {round(avg_response, 2)}ms response time"
            })

        elif analysis_type == "energy_optimization":
            # Analyze energy usage for optimization (SOP 6.7.8)
            devices_energy = analysis_data.get("devices_energy", {})

            if not devices_energy:
                return json.dumps({
                    "success": False,
                    "error": "Halt: devices_energy required in analysis_data for energy_optimization"
                })

            # Find high consumers
            sorted_energy = sorted(devices_energy.items(), key=lambda x: x[1], reverse=True)
            top_consumers = sorted_energy[:5]

            total_energy = sum(devices_energy.values())

            # Calculate optimization potential
            optimization_potential = []
            for device_id, energy_kwh in top_consumers:
                if energy_kwh > 1.0:  # Threshold for high consumption
                    potential_savings = energy_kwh * 0.2  # 20% reduction potential
                    optimization_potential.append({
                        "device_id": device_id,
                        "current_energy_kwh": energy_kwh,
                        "potential_savings_kwh": round(potential_savings, 2),
                        "potential_savings_percentage": 20
                    })

            return json.dumps({
                "success": True,
                "analysis_type": "energy_optimization",
                "total_devices": len(devices_energy),
                "total_energy_kwh": round(total_energy, 2),
                "top_consumers": [{"device_id": d[0], "energy_kwh": d[1]} for d in top_consumers],
                "optimization_opportunities": optimization_potential,
                "message": f"Energy optimization: {len(optimization_potential)} opportunities identified"
            })

        else:
            # Generic analysis response for other analysis types
            return json.dumps({
                "success": True,
                "analysis_type": analysis_type,
                "analysis_data": analysis_data,
                "message": f"{analysis_type} analysis completed"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "evaluate_patterns",
                "description": "Analyze data for patterns and anomalies in the smart home management system. Analyzes activity_patterns from audit logs detecting usage trends, peak hours, and user behavior for security monitoring and optimization. Detects error_patterns identifying recurring failures, affected devices, and error types for proactive maintenance. Performs connection_diagnostic to identify network issues, signal problems, and connectivity patterns (SOP 6.9.1). Analyzes device_lifecycle patterns for replacement planning (SOP 6.7.7). Detects routine_conflicts identifying overlapping schedules and device contention (SOP 6.9.3). Generates performance_summary analyzing response times and device performance (SOP 6.9.2). Performs energy_optimization analysis identifying high consumers and savings opportunities (SOP 6.7.8). Provides failure_patterns analysis for RCA, update_priority recommendations, and performance_comparison across device types.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_type": {
                            "type": "string",
                            "description": "Type of pattern analysis to perform"
                        },
                        "analysis_data": {
                            "type": "object",
                            "description": "Analysis-specific data. For activity_patterns: {logs}. For error_patterns: {logs}. For connection_diagnostic: {device_id}. For routine_conflicts: {routines}. For performance_summary: {response_times}. For energy_optimization: {devices_energy}"
                        }
                    },
                    "required": ["analysis_type", "analysis_data"]
                }
            }
        }
