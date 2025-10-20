import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CategorizeData(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], categorization_type: str, categorization_data: Dict[str, Any]) -> str:
        """
        Categorize entities by specific attributes in the smart home management system.
        Supports categorization by health status, log types, severity, and performance metrics.
        """

        # Validate categorization_type
        valid_types = ["device_health", "logs_by_type", "devices_by_severity", "routine_health", "response_performance", "health_category", "conflict_classification"]
        if categorization_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid categorization_type '{categorization_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not categorization_data or not isinstance(categorization_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: categorization_data required and must be a dictionary"
            })

        if categorization_type == "device_health":
            # Categorize devices by health status (SOP 6.1.2)
            device_list = categorization_data.get("devices", [])

            if not device_list:
                return json.dumps({
                    "success": False,
                    "error": "Halt: devices list required in categorization_data for device_health"
                })

            categories = {
                "healthy": [],
                "warning": [],
                "critical": []
            }

            for device_info in device_list:
                device_id = device_info.get("device_id")
                health_score = device_info.get("health_score", 100)

                # Categorize by health score
                if health_score >= 80:
                    category = "healthy"
                elif health_score >= 60:
                    category = "warning"
                else:
                    category = "critical"

                categories[category].append(device_info)

            return json.dumps({
                "success": True,
                "categorization_type": "device_health",
                "categories": categories,
                "summary": {
                    "healthy": len(categories["healthy"]),
                    "warning": len(categories["warning"]),
                    "critical": len(categories["critical"]),
                    "total": len(device_list)
                },
                "message": f"Categorized {len(device_list)} devices by health status"
            })

        elif categorization_type == "logs_by_type":
            # Categorize logs by action type
            logs = categorization_data.get("logs", [])

            if not logs:
                return json.dumps({
                    "success": False,
                    "error": "Halt: logs list required in categorization_data for logs_by_type"
                })

            categories = {}

            for log in logs:
                action_type = log.get("action_type", "unknown")
                if action_type not in categories:
                    categories[action_type] = []
                categories[action_type].append(log)

            summary = {action: len(logs) for action, logs in categories.items()}

            return json.dumps({
                "success": True,
                "categorization_type": "logs_by_type",
                "categories": {k: {"count": len(v), "logs": v[:5]} for k, v in categories.items()},
                "summary": summary,
                "total_categories": len(categories),
                "message": f"Categorized {len(logs)} logs into {len(categories)} action types"
            })

        elif categorization_type == "devices_by_severity":
            # Categorize devices by issue severity (SOP 6.1.2)
            devices = categorization_data.get("devices", [])

            if not devices:
                return json.dumps({
                    "success": False,
                    "error": "Halt: devices list required in categorization_data for devices_by_severity"
                })

            categories = {
                "critical": [],
                "warning": [],
                "informational": []
            }

            for device_info in devices.items():
                # Determine severity based on issues
                connection_status = device_info.get("connection_status")
                battery_level = device_info.get("battery_level")
                signal_strength = device_info.get("signal_strength")

                if connection_status == "offline" or (battery_level and battery_level < 10):
                    severity = "critical"
                elif connection_status == "error" or (battery_level and battery_level < 20) or (signal_strength and signal_strength < -70):
                    severity = "warning"
                else:
                    severity = "informational"

                categories[severity].append(device_info)

            return json.dumps({
                "success": True,
                "categorization_type": "devices_by_severity",
                "categories": categories,
                "summary": {
                    "critical": len(categories["critical"]),
                    "warning": len(categories["warning"]),
                    "informational": len(categories["informational"]),
                    "total": len(devices)
                },
                "message": f"Categorized {len(devices)} devices by severity"
            })

        elif categorization_type == "routine_health":
            # Categorize routines by health/status
            routines = categorization_data.get("routines", [])

            if not routines:
                return json.dumps({
                    "success": False,
                    "error": "Halt: routines list required in categorization_data for routine_health"
                })

            categories = {
                "healthy": [],
                "needs_attention": [],
                "disabled": []
            }

            for routine in routines:
                status = routine.get("status", "enabled")
                execution_count = routine.get("execution_count", 0)

                if status == "disabled":
                    category = "disabled"
                elif status == "error" or execution_count == 0:
                    category = "needs_attention"
                else:
                    category = "healthy"

                categories[category].append(routine)

            return json.dumps({
                "success": True,
                "categorization_type": "routine_health",
                "categories": categories,
                "summary": {
                    "healthy": len(categories["healthy"]),
                    "needs_attention": len(categories["needs_attention"]),
                    "disabled": len(categories["disabled"]),
                    "total": len(routines)
                },
                "message": f"Categorized {len(routines)} routines by health status"
            })

        elif categorization_type == "response_performance":
            # Categorize devices by response time performance
            response_times = categorization_data.get("response_times", {})

            if not response_times:
                return json.dumps({
                    "success": False,
                    "error": "Halt: response_times required in categorization_data for response_performance"
                })

            categories = {
                "excellent": [],  # < 200ms
                "good": [],       # 200-500ms
                "acceptable": [], # 500-1000ms
                "poor": []        # > 1000ms
            }

            for device_id, response_time in response_times.items():
                if response_time < 200:
                    category = "excellent"
                elif response_time < 500:
                    category = "good"
                elif response_time < 1000:
                    category = "acceptable"
                else:
                    category = "poor"

                categories[category].append({
                    "device_id": device_id,
                    "response_time_ms": response_time
                })

            return json.dumps({
                "success": True,
                "categorization_type": "response_performance",
                "categories": categories,
                "summary": {
                    "excellent": len(categories["excellent"]),
                    "good": len(categories["good"]),
                    "acceptable": len(categories["acceptable"]),
                    "poor": len(categories["poor"]),
                    "total": len(response_times)
                },
                "message": f"Categorized {len(response_times)} devices by response performance"
            })

        elif categorization_type == "health_category":
            # Generic health category assignment
            items = categorization_data.get("items", [])
            score_field = categorization_data.get("score_field", "health_score")

            if not items:
                return json.dumps({
                    "success": False,
                    "error": "Halt: items list required in categorization_data for health_category"
                })

            categories = {
                "healthy": [],
                "warning": [],
                "critical": []
            }

            for item in items:
                score = item.get(score_field, 100)

                if score >= 80:
                    category = "healthy"
                elif score >= 60:
                    category = "warning"
                else:
                    category = "critical"

                categories[category].append(item)

            return json.dumps({
                "success": True,
                "categorization_type": "health_category",
                "categories": categories,
                "summary": {
                    "healthy": len(categories["healthy"]),
                    "warning": len(categories["warning"]),
                    "critical": len(categories["critical"]),
                    "total": len(items)
                },
                "message": f"Categorized {len(items)} items by health category"
            })

        elif categorization_type == "conflict_classification":
            # Classify conflicts by type (SOP 6.9.3)
            conflicts = categorization_data.get("conflicts", [])

            if not conflicts:
                return json.dumps({
                    "success": False,
                    "error": "Halt: conflicts list required in categorization_data for conflict_classification"
                })

            categories = {
                "routine_schedule": [],
                "device_capability": [],
                "network_bandwidth": [],
                "resource_contention": []
            }

            for conflict in conflicts:
                conflict_type = conflict.get("type", "unknown")

                if conflict_type in categories:
                    categories[conflict_type].append(conflict)
                else:
                    # Default to resource_contention if unknown
                    categories["resource_contention"].append(conflict)

            return json.dumps({
                "success": True,
                "categorization_type": "conflict_classification",
                "categories": categories,
                "summary": {k: len(v) for k, v in categories.items()},
                "total_conflicts": len(conflicts),
                "message": f"Classified {len(conflicts)} conflicts into categories"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "categorize_data",
                "description": "Categorize entities by specific attributes in the smart home management system. Categorizes devices by health status (healthy/warning/critical) based on health scores for monitoring and alerting (SOP 6.1.2). Categorizes audit logs by action type for security analysis and compliance reporting. Categorizes devices by issue severity (critical/warning/informational) based on connection status, battery, and signal strength (SOP 6.1.2). Categorizes routines by health status (healthy/needs_attention/disabled) for automation monitoring. Categorizes devices by response time performance (excellent/good/acceptable/poor) for performance optimization (SOP 6.9.2). Applies generic health category assignment using custom score fields. Classifies conflicts by type (routine_schedule, device_capability, network_bandwidth, resource_contention) for conflict resolution (SOP 6.9.3).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "categorization_type": {
                            "type": "string",
                            "description": "Type of categorization to perform",
                            "enum": ["device_health", "logs_by_type", "devices_by_severity", "routine_health", "response_performance", "health_category", "conflict_classification"]
                        },
                        "categorization_data": {
                            "type": "object",
                            "description": "Data to categorize. For device_health: {devices}. For logs_by_type: {logs}. For devices_by_severity: {devices}. For routine_health: {routines}. For response_performance: {response_times}. For health_category: {items, score_field}. For conflict_classification: {conflicts}",
                            "properties": {
                                "devices": {
                                    "type": "array",
                                    "description": "List of device objects to categorize"
                                },
                                "logs": {
                                    "type": "array",
                                    "description": "List of log objects to categorize"
                                },
                                "routines": {
                                    "type": "array",
                                    "description": "List of routine objects to categorize"
                                },
                                "response_times": {
                                    "type": "object",
                                    "description": "Map of device_id to response time in milliseconds"
                                },
                                "items": {
                                    "type": "array",
                                    "description": "Generic list of items to categorize"
                                },
                                "score_field": {
                                    "type": "string",
                                    "description": "Field name containing health score"
                                },
                                "conflicts": {
                                    "type": "array",
                                    "description": "List of conflict objects to classify"
                                }
                            }
                        }
                    },
                    "required": ["categorization_type", "categorization_data"]
                }
            }
        }
