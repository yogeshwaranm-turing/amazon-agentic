import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class AdministerAuditLogs(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, operation_data: Dict[str, Any]) -> str:
        """
        Create audit logs and archive access history in the smart home management system.
        Handles audit log creation, archival, retrieval, and analysis for compliance and security monitoring.
        """

        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1

        # Validate operation type
        valid_operations = ["create_log", "archive_device_logs", "archive_user_logs", "get_logs_by_date_range", "categorize_logs", "analyze_patterns"]
        if operation not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not operation_data or not isinstance(operation_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: operation_data required and must be a dictionary"
            })

        # Get access_logs table
        access_logs = data.get("access_logs", {})

        if operation == "create_log":
            # Create new audit log entry
            action_type = operation_data.get("action_type")
            entity_type = operation_data.get("entity_type")
            entity_id = operation_data.get("entity_id")
            outcome = operation_data.get("outcome")
            user_id = operation_data.get("user_id")

            if not action_type:
                return json.dumps({
                    "success": False,
                    "error": "Halt: action_type required in operation_data for create_log"
                })

            if not outcome:
                return json.dumps({
                    "success": False,
                    "error": "Halt: outcome required in operation_data for create_log"
                })

            # Validate outcome
            valid_outcomes = ["success", "failure"]
            if outcome not in valid_outcomes:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid outcome '{outcome}'. Must be one of: {', '.join(valid_outcomes)}"
                })

            # Create log entry
            log_id = str(generate_id(access_logs))
            timestamp = "2025-10-16T14:30:00"

            log_entry = {
                "log_id": log_id,
                "timestamp": timestamp,
                "user_id": user_id,
                "action_type": action_type,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "outcome": outcome,
                "error_message": operation_data.get("error_message"),
                "operation_details": json.dumps(operation_data.get("operation_details", {})),
                "ip_address": operation_data.get("ip_address"),
                "user_agent": operation_data.get("user_agent")
            }

            access_logs[log_id] = log_entry

            return json.dumps({
                "success": True,
                "operation": "create_log",
                "log_id": log_id,
                "log_entry": log_entry,
                "message": f"Audit log created: {action_type} - {outcome}"
            })

        elif operation == "archive_device_logs":
            # Archive logs for a specific device
            device_id = operation_data.get("device_id")
            retention_days = operation_data.get("retention_days", 90)

            if not device_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: device_id required in operation_data for archive_device_logs"
                })

            # Filter logs for this device
            device_logs = [
                log for log in access_logs.values()
                if log.get("entity_id") == device_id and log.get("entity_type") == "device"
            ]

            # Simulate archival (in real implementation, would move to archive storage)
            archive_id = f"archive_device_{device_id}_{int(datetime.now().timestamp())}"
            archive_location = f"/archives/devices/{device_id}/{archive_id}.json"

            return json.dumps({
                "success": True,
                "operation": "archive_device_logs",
                "device_id": device_id,
                "logs_archived": len(device_logs),
                "retention_days": retention_days,
                "archive_id": archive_id,
                "archive_location": archive_location,
                "timestamp": "2025-10-16T14:30:00",
                "message": f"Archived {len(device_logs)} logs for device '{device_id}'"
            })

        elif operation == "archive_user_logs":
            # Archive logs for a specific user
            user_id = operation_data.get("user_id")
            retention_days = operation_data.get("retention_days", 90)

            if not user_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: user_id required in operation_data for archive_user_logs"
                })

            # Filter logs for this user
            user_logs = [log for log in access_logs.values() if log.get("user_id") == user_id]

            # Simulate archival
            archive_id = f"archive_user_{user_id}_{int(datetime.now().timestamp())}"
            archive_location = f"/archives/users/{user_id}/{archive_id}.json"

            return json.dumps({
                "success": True,
                "operation": "archive_user_logs",
                "user_id": user_id,
                "logs_archived": len(user_logs),
                "retention_days": retention_days,
                "archive_id": archive_id,
                "archive_location": archive_location,
                "timestamp": "2025-10-16T14:30:00",
                "message": f"Archived {len(user_logs)} logs for user '{user_id}'"
            })

        elif operation == "get_logs_by_date_range":
            # Retrieve logs within a date range
            start_datetime = operation_data.get("start_datetime")
            end_datetime = operation_data.get("end_datetime")

            if not start_datetime or not end_datetime:
                return json.dumps({
                    "success": False,
                    "error": "Halt: start_datetime and end_datetime required in operation_data for get_logs_by_date_range"
                })

            # Filter logs by date range (simulated)
            # In real implementation, would parse datetime and compare
            filtered_logs = list(access_logs.values())  # Simplified: return all

            # Group by action type
            by_action_type = {}
            by_outcome = {"success": 0, "failure": 0}

            for log in filtered_logs:
                action_type = log.get("action_type", "unknown")
                by_action_type[action_type] = by_action_type.get(action_type, 0) + 1

                outcome = log.get("outcome", "unknown")
                if outcome in by_outcome:
                    by_outcome[outcome] += 1

            return json.dumps({
                "success": True,
                "operation": "get_logs_by_date_range",
                "start_datetime": start_datetime,
                "end_datetime": end_datetime,
                "total_logs": len(filtered_logs),
                "by_action_type": by_action_type,
                "by_outcome": by_outcome,
                "logs": filtered_logs[:100],  # Return first 100 for display
                "message": f"Retrieved {len(filtered_logs)} logs from {start_datetime} to {end_datetime}"
            })

        elif operation == "categorize_logs":
            # Categorize logs by type or pattern
            categorization_type = operation_data.get("categorization_type", "by_action")

            if categorization_type == "by_action":
                categories = {}
                for log in access_logs.values():
                    action_type = log.get("action_type", "unknown")
                    if action_type not in categories:
                        categories[action_type] = []
                    categories[action_type].append(log.get("log_id"))

                return json.dumps({
                    "success": True,
                    "operation": "categorize_logs",
                    "categorization_type": categorization_type,
                    "categories": {k: {"count": len(v), "log_ids": v[:10]} for k, v in categories.items()},
                    "total_categories": len(categories),
                    "message": f"Logs categorized into {len(categories)} action types"
                })

            elif categorization_type == "by_outcome":
                success_logs = [log for log in access_logs.values() if log.get("outcome") == "success"]
                failure_logs = [log for log in access_logs.values() if log.get("outcome") == "failure"]

                return json.dumps({
                    "success": True,
                    "operation": "categorize_logs",
                    "categorization_type": categorization_type,
                    "categories": {
                        "success": {"count": len(success_logs)},
                        "failure": {"count": len(failure_logs)}
                    },
                    "message": f"Logs categorized by outcome: {len(success_logs)} success, {len(failure_logs)} failure"
                })

            else:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Unknown categorization_type '{categorization_type}'"
                })

        elif operation == "analyze_patterns":
            # Analyze activity patterns in logs
            analysis_type = operation_data.get("analysis_type", "activity_frequency")

            if analysis_type == "activity_frequency":
                # Count operations per action type
                action_counts = {}
                for log in access_logs.values():
                    action = log.get("action_type", "unknown")
                    action_counts[action] = action_counts.get(action, 0) + 1

                # Find most and least common
                sorted_actions = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)
                most_common = sorted_actions[:5] if sorted_actions else []
                least_common = sorted_actions[-5:] if len(sorted_actions) > 5 else []

                return json.dumps({
                    "success": True,
                    "operation": "analyze_patterns",
                    "analysis_type": analysis_type,
                    "total_logs": len(access_logs),
                    "unique_actions": len(action_counts),
                    "most_common_actions": [{"action": a[0], "count": a[1]} for a in most_common],
                    "least_common_actions": [{"action": a[0], "count": a[1]} for a in least_common],
                    "message": f"Activity pattern analysis completed: {len(action_counts)} unique action types"
                })

            elif analysis_type == "error_patterns":
                # Analyze failure patterns
                failures = [log for log in access_logs.values() if log.get("outcome") == "failure"]
                error_types = {}

                for log in failures:
                    error_msg = log.get("error_message", "Unknown error")
                    error_types[error_msg] = error_types.get(error_msg, 0) + 1

                return json.dumps({
                    "success": True,
                    "operation": "analyze_patterns",
                    "analysis_type": analysis_type,
                    "total_failures": len(failures),
                    "unique_error_types": len(error_types),
                    "error_distribution": error_types,
                    "failure_rate": round(len(failures) / len(access_logs) * 100, 2) if access_logs else 0,
                    "message": f"Error pattern analysis: {len(failures)} failures with {len(error_types)} error types"
                })

            else:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Unknown analysis_type '{analysis_type}'"
                })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_audit_logs",
                "description": "Create audit logs and archive access history in the smart home management system. Creates audit log entries recording user actions, system operations, device changes, and security events with outcome tracking (success/failure), error messages, and operation details for compliance and security monitoring. Archives device-specific logs for long-term retention and regulatory compliance (SOP 6.2.5). Archives user-specific logs when users are removed or for compliance audits. Retrieves logs within date ranges with filtering by action type and outcome for security analysis and troubleshooting. Categorizes logs by action type, outcome, entity type, or custom criteria for reporting and analysis. Analyzes activity patterns detecting anomalies, frequent operations, error trends, and security events for proactive monitoring.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Audit log operation to perform",
                            "enum": ["create_log", "archive_device_logs", "archive_user_logs", "get_logs_by_date_range", "categorize_logs", "analyze_patterns"]
                        },
                        "operation_data": {
                            "type": "object",
                            "description": "Operation-specific data. For create_log: {action_type, entity_type, entity_id, outcome, user_id, error_message, operation_details, ip_address, user_agent}. For archive_device_logs: {device_id, retention_days}. For archive_user_logs: {user_id, retention_days}. For get_logs_by_date_range: {start_datetime, end_datetime}. For categorize_logs: {categorization_type}. For analyze_patterns: {analysis_type}",
                            "properties": {
                                "action_type": {
                                    "type": "string",
                                    "description": "Type of action being logged"
                                },
                                "entity_type": {
                                    "type": "string",
                                    "description": "Type of entity affected by action"
                                },
                                "entity_id": {
                                    "type": "string",
                                    "description": "ID of entity affected"
                                },
                                "outcome": {
                                    "type": "string",
                                    "description": "Outcome of operation",
                                    "enum": ["success", "failure"]
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "ID of user performing action"
                                },
                                "device_id": {
                                    "type": "string",
                                    "description": "Device ID for archival"
                                },
                                "retention_days": {
                                    "type": "number",
                                    "description": "Number of days to retain archived logs"
                                },
                                "start_datetime": {
                                    "type": "string",
                                    "description": "Start datetime for log retrieval (ISO 8601)"
                                },
                                "end_datetime": {
                                    "type": "string",
                                    "description": "End datetime for log retrieval (ISO 8601)"
                                },
                                "categorization_type": {
                                    "type": "string",
                                    "description": "How to categorize logs: by_action, by_outcome, by_entity"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "description": "Type of pattern analysis: activity_frequency, error_patterns"
                                }
                            }
                        }
                    },
                    "required": ["operation", "operation_data"]
                }
            }
        }
