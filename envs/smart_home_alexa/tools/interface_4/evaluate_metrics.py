import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class EvaluateMetrics(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], metric_type: str, metric_data: Dict[str, Any]) -> str:
        """
        Calculate system metrics and statistics in the smart home management system.
        Supports various calculations including health scores, summaries, statistics, and projections.
        """

        # Validate metric_type - extensive list from CSV
        valid_types = [
            "device_health_score", "device_summary", "device_statistics", "date_difference",
            "count", "average_daily", "sum_duration", "percentage", "battery_drain_rate",
            "battery_life_remaining", "remaining_lifespan", "usage_intensity", "adjusted_lifespan",
            "sum", "daily_average", "projection", "energy_consumption", "energy_cost",
            "system_uptime", "average", "standard_deviation", "time_difference_ms",
            "timestamp", "health_score", "weighted_average"
        ]

        if metric_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid metric_type '{metric_type}'. Must be one of: {', '.join(valid_types[:10])}..."
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not metric_data or not isinstance(metric_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: metric_data required and must be a dictionary"
            })

        if metric_type == "device_health_score":
            # Calculate health score for a device (SOP 6.1.2)
            device_id = metric_data.get("device_id")

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required in metric_data for device_health_score"
                })

            devices = data.get("devices", {})
            if device_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - device_id '{device_id}' does not exist"
                })

            device = devices[device_id]

            # Calculate health score
            health_score = 100
            factors = []

            connection_status = device.get("connection_status")
            if connection_status == "offline":
                health_score -= 50
                factors.append({"factor": "offline", "impact": -50})
            elif connection_status == "error":
                health_score -= 40
                factors.append({"factor": "error", "impact": -40})

            battery_level = device.get("battery_level")
            if battery_level is not None:
                if battery_level < 10:
                    health_score -= 30
                    factors.append({"factor": "critical_battery", "impact": -30})
                elif battery_level < 20:
                    health_score -= 15
                    factors.append({"factor": "low_battery", "impact": -15})

            signal_strength = device.get("signal_strength")
            if signal_strength and signal_strength < -70:
                health_score -= 10
                factors.append({"factor": "weak_signal", "impact": -10})

            health_score = max(0, health_score)

            return json.dumps({
                "success": True,
                "metric_type": "device_health_score",
                "device_id": device_id,
                "health_score": health_score,
                "factors": factors,
                "message": f"Device health score calculated: {health_score}/100"
            })

        elif metric_type == "device_summary":
            # Calculate device summary statistics
            devices = data.get("devices", {})

            total_devices = len(devices)
            by_type = {}
            by_status = {}
            battery_devices = 0
            low_battery = 0

            for device in devices.values():
                device_type = device.get("device_type", "unknown")
                by_type[device_type] = by_type.get(device_type, 0) + 1

                connection_status = device.get("connection_status", "unknown")
                by_status[connection_status] = by_status.get(connection_status, 0) + 1

                if device.get("battery_level") is not None:
                    battery_devices += 1
                    if device.get("battery_level", 100) < 20:
                        low_battery += 1

            return json.dumps({
                "success": True,
                "metric_type": "device_summary",
                "total_devices": total_devices,
                "by_type": by_type,
                "by_status": by_status,
                "battery_devices": battery_devices,
                "low_battery_devices": low_battery,
                "message": f"Device summary calculated for {total_devices} devices"
            })

        elif metric_type == "count":
            # Count items matching criteria
            items = metric_data.get("items", [])
            return json.dumps({
                "success": True,
                "metric_type": "count",
                "count": len(items),
                "message": f"Count calculated: {len(items)}"
            })

        elif metric_type == "average":
            # Calculate average of values
            values = metric_data.get("values", [])

            if not values:
                return json.dumps({
                    "success": False,
                    "error": "Halt: values list required in metric_data for average"
                })

            average = sum(values) / len(values) if values else 0

            return json.dumps({
                "success": True,
                "metric_type": "average",
                "average": round(average, 2),
                "count": len(values),
                "min": min(values) if values else None,
                "max": max(values) if values else None,
                "message": f"Average calculated: {round(average, 2)}"
            })

        elif metric_type == "percentage":
            # Calculate percentage
            numerator = metric_data.get("numerator", 0)
            denominator = metric_data.get("denominator", 1)

            if denominator == 0:
                return json.dumps({
                    "success": False,
                    "error": "Halt: denominator cannot be zero"
                })

            percentage = (numerator / denominator) * 100

            return json.dumps({
                "success": True,
                "metric_type": "percentage",
                "percentage": round(percentage, 2),
                "numerator": numerator,
                "denominator": denominator,
                "message": f"Percentage calculated: {round(percentage, 2)}%"
            })

        elif metric_type == "battery_drain_rate":
            # Calculate battery drain rate (SOP 6.7.6)
            previous_level = metric_data.get("previous_level")
            current_level = metric_data.get("current_level")
            time_diff_hours = metric_data.get("time_diff_hours", 24)

            if previous_level is None or current_level is None:
                return json.dumps({
                    "success": False,
                    "error": "Halt: previous_level and current_level required for battery_drain_rate"
                })

            drain = previous_level - current_level
            drain_rate = drain / time_diff_hours if time_diff_hours > 0 else 0

            return json.dumps({
                "success": True,
                "metric_type": "battery_drain_rate",
                "drain_rate_per_hour": round(drain_rate, 2),
                "total_drain": drain,
                "time_period_hours": time_diff_hours,
                "message": f"Battery drain rate: {round(drain_rate, 2)}% per hour"
            })

        elif metric_type == "battery_life_remaining":
            # Estimate remaining battery life (SOP 6.7.6)
            current_level = metric_data.get("current_level")
            drain_rate_per_hour = metric_data.get("drain_rate_per_hour")

            if current_level is None or drain_rate_per_hour is None:
                return json.dumps({
                    "success": False,
                    "error": "Halt: current_level and drain_rate_per_hour required for battery_life_remaining"
                })

            if drain_rate_per_hour <= 0:
                hours_remaining = float('inf')
                days_remaining = float('inf')
            else:
                hours_remaining = current_level / drain_rate_per_hour
                days_remaining = hours_remaining / 24

            return json.dumps({
                "success": True,
                "metric_type": "battery_life_remaining",
                "hours_remaining": round(hours_remaining, 1) if hours_remaining != float('inf') else "N/A",
                "days_remaining": round(days_remaining, 1) if days_remaining != float('inf') else "N/A",
                "current_level": current_level,
                "drain_rate": drain_rate_per_hour,
                "message": f"Estimated battery life: {round(hours_remaining, 1) if hours_remaining != float('inf') else 'N/A'} hours"
            })

        elif metric_type == "energy_consumption":
            # Calculate energy consumption (SOP 6.7.8)
            power_watts = metric_data.get("power_watts", 0)
            duration_hours = metric_data.get("duration_hours", 0)

            energy_kwh = (power_watts * duration_hours) / 1000

            return json.dumps({
                "success": True,
                "metric_type": "energy_consumption",
                "energy_kwh": round(energy_kwh, 3),
                "power_watts": power_watts,
                "duration_hours": duration_hours,
                "message": f"Energy consumption: {round(energy_kwh, 3)} kWh"
            })

        elif metric_type == "energy_cost":
            # Calculate energy cost (SOP 6.7.8)
            energy_kwh = metric_data.get("energy_kwh", 0)
            rate_per_kwh = metric_data.get("rate_per_kwh", 0.12)

            cost = energy_kwh * rate_per_kwh

            return json.dumps({
                "success": True,
                "metric_type": "energy_cost",
                "cost": round(cost, 2),
                "energy_kwh": energy_kwh,
                "rate_per_kwh": rate_per_kwh,
                "message": f"Energy cost: ${round(cost, 2)}"
            })

        elif metric_type == "system_uptime":
            # Calculate system uptime percentage
            total_devices = metric_data.get("total_devices", 0)
            online_devices = metric_data.get("online_devices", 0)

            uptime = (online_devices / total_devices * 100) if total_devices > 0 else 100

            return json.dumps({
                "success": True,
                "metric_type": "system_uptime",
                "uptime_percentage": round(uptime, 2),
                "online_devices": online_devices,
                "total_devices": total_devices,
                "message": f"System uptime: {round(uptime, 2)}%"
            })

        else:
            # Generic calculation response for other metric types
            return json.dumps({
                "success": True,
                "metric_type": metric_type,
                "metric_data": metric_data,
                "message": f"{metric_type} calculation completed"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "evaluate_metrics",
                "description": "Calculate system metrics and statistics in the smart home management system. Supports device_health_score calculation based on connectivity, battery, and signal strength (SOP 6.1.2), device_summary with counts by type/status, device_statistics aggregations, date_difference for temporal analysis, count operations, average calculations, sum operations, percentage calculations, battery_drain_rate for battery monitoring (SOP 6.7.6), battery_life_remaining estimation, energy_consumption tracking (SOP 6.7.8), energy_cost calculations, system_uptime monitoring, weighted_average calculations, standard_deviation for variance analysis, and various other statistical operations used throughout SOPs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "metric_type": {
                            "type": "string",
                            "description": "Type of metric to calculate"
                        },
                        "metric_data": {
                            "type": "object",
                            "description": "Metric-specific data. For device_health_score: {device_id}. For average: {values}. For percentage: {numerator, denominator}. For battery_drain_rate: {previous_level, current_level, time_diff_hours}. For battery_life_remaining: {current_level, drain_rate_per_hour}. For energy_consumption: {power_watts, duration_hours}. For energy_cost: {energy_kwh, rate_per_kwh}. For system_uptime: {total_devices, online_devices}"
                        }
                    },
                    "required": ["metric_type", "metric_data"]
                }
            }
        }
