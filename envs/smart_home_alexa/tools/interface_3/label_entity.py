import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class LabelEntity(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], flag_type: str, entity_id: str, flag_data: Dict[str, Any]) -> str:
        """
        Flag entities for attention or special handling in the smart home management system.
        Used to mark devices or other entities that require immediate attention, investigation, or special handling.
        """

        # Validate flag_type
        valid_types = ["device_for_attention", "critical_issue"]
        if flag_type not in valid_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid flag_type '{flag_type}'. Must be one of: {', '.join(valid_types)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not entity_id:
            return json.dumps({
                "success": False,
                "error": "Halt: entity_id required for flag operation"
            })

        if not flag_data or not isinstance(flag_data, dict):
            return json.dumps({
                "success": False,
                "error": "Halt: flag_data required and must be a dictionary"
            })

        # Get relevant tables
        devices = data.get("devices", {})
        system_alerts = data.get("system_alerts", {})

        if flag_type == "device_for_attention":
            # Flag a device that needs immediate attention (SOP 6.1.2)

            # Validate device exists
            if entity_id not in devices:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Device not found - entity_id '{entity_id}' does not exist"
                })

            device = devices[entity_id]

            # Get flag details
            reason = flag_data.get("reason")
            priority = flag_data.get("priority", "high")
            issue_type = flag_data.get("issue_type", "general")

            if not reason:
                return json.dumps({
                    "success": False,
                    "error": "Halt: reason required in flag_data for device_for_attention"
                })

            # Validate priority
            valid_priorities = ["low", "medium", "high", "critical"]
            if priority not in valid_priorities:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}"
                })

            # Create alert for the flagged device
            def generate_id(table: Dict[str, Any]) -> int:
                if not table:
                    return 1
                return max(int(k) for k in table.keys()) + 1

            alert_id = f"alert_{generate_id(system_alerts)}"
            timestamp = "2025-10-16T14:30:00"

            alert_record = {
                "alert_id": alert_id,
                "alert_type": issue_type,
                "priority": priority,
                "message": f"Device flagged for attention: {reason}",
                "affected_device_id": entity_id,
                "affected_entity_type": "device",
                "affected_entity_id": entity_id,
                "acknowledged": False,
                "acknowledged_by_user_id": None,
                "acknowledged_at": None,
                "resolved": False,
                "resolved_at": None,
                "created_date": timestamp,
                "updated_date": timestamp
            }

            system_alerts[alert_id] = alert_record

            # Add flag metadata to device (in real implementation, might have a separate flags table)
            if "flags" not in device:
                device["flags"] = []

            flag_entry = {
                "flag_type": "attention_required",
                "reason": reason,
                "priority": priority,
                "issue_type": issue_type,
                "flagged_at": timestamp,
                "alert_id": alert_id,
                "resolved": False
            }

            # Store as JSON string if needed
            device["flags"] = json.dumps([flag_entry])

            return json.dumps({
                "success": True,
                "flag_type": "device_for_attention",
                "entity_id": entity_id,
                "device_name": device.get("device_name"),
                "reason": reason,
                "priority": priority,
                "issue_type": issue_type,
                "alert_id": alert_id,
                "alert_created": True,
                "timestamp": timestamp,
                "message": f"Device '{device.get('device_name')}' flagged for attention with {priority} priority"
            })

        elif flag_type == "critical_issue":
            # Flag a critical issue affecting an entity

            # Get issue details
            reason = flag_data.get("reason")
            issue_description = flag_data.get("issue_description")
            requires_immediate_action = flag_data.get("requires_immediate_action", True)

            if not reason:
                return json.dumps({
                    "success": False,
                    "error": "Halt: reason required in flag_data for critical_issue"
                })

            # Create critical alert
            def generate_id(table: Dict[str, Any]) -> int:
                if not table:
                    return 1
                return max(int(k) for k in table.keys()) + 1

            alert_id = f"alert_{generate_id(system_alerts)}"
            timestamp = "2025-10-16T14:30:00"

            alert_record = {
                "alert_id": alert_id,
                "alert_type": "critical_issue",
                "priority": "critical",
                "message": f"CRITICAL: {reason}",
                "affected_device_id": entity_id if entity_id in devices else None,
                "affected_entity_type": "device" if entity_id in devices else "system",
                "affected_entity_id": entity_id,
                "acknowledged": False,
                "acknowledged_by_user_id": None,
                "acknowledged_at": None,
                "resolved": False,
                "resolved_at": None,
                "created_date": timestamp,
                "updated_date": timestamp
            }

            system_alerts[alert_id] = alert_record

            # Determine entity type and name
            entity_type = "unknown"
            entity_name = entity_id

            if entity_id in devices:
                entity_type = "device"
                entity_name = devices[entity_id].get("device_name", entity_id)

            return json.dumps({
                "success": True,
                "flag_type": "critical_issue",
                "entity_id": entity_id,
                "entity_type": entity_type,
                "entity_name": entity_name,
                "reason": reason,
                "issue_description": issue_description,
                "requires_immediate_action": requires_immediate_action,
                "alert_id": alert_id,
                "priority": "critical",
                "timestamp": timestamp,
                "message": f"CRITICAL ISSUE flagged for {entity_type} '{entity_name}': {reason}"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "label_entity",
                "description": "Flag entities for attention or special handling in the smart home management system. Flags device_for_attention marking devices that require immediate attention due to offline status, critical battery, errors, or security concerns with priority levels (low/medium/high/critical) and issue categorization (SOP 6.1.2). Creates system alerts automatically when devices are flagged for tracking and notification. Flags critical_issue for severe problems affecting entities requiring immediate action and escalation. Supports reason documentation and issue descriptions for context. Creates audit trail entries for flagged entities. Essential for proactive monitoring, issue escalation, and admin notifications. Integrates with system_alerts table for centralized alert management and acknowledgment tracking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "flag_type": {
                            "type": "string",
                            "description": "Type of flag to apply",
                            "enum": ["device_for_attention", "critical_issue"]
                        },
                        "entity_id": {
                            "type": "string",
                            "description": "ID of entity to flag (required)"
                        },
                        "flag_data": {
                            "type": "object",
                            "description": "Flag-specific data. For device_for_attention: {reason, priority, issue_type}. For critical_issue: {reason, issue_description, requires_immediate_action}",
                            "properties": {
                                "reason": {
                                    "type": "string",
                                    "description": "Reason for flagging (required)"
                                },
                                "priority": {
                                    "type": "string",
                                    "description": "Priority level: low, medium, high, critical (default: high)",
                                    "enum": ["low", "medium", "high", "critical"]
                                },
                                "issue_type": {
                                    "type": "string",
                                    "description": "Type of issue: connectivity, battery, security, hardware, configuration, etc."
                                },
                                "issue_description": {
                                    "type": "string",
                                    "description": "Detailed description of the critical issue"
                                },
                                "requires_immediate_action": {
                                    "type": "boolean",
                                    "description": "Whether issue requires immediate action (default: true)"
                                }
                            },
                            "required": ["reason"]
                        }
                    },
                    "required": ["flag_type", "entity_id", "flag_data"]
                }
            }
        }
