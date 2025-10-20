import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class HandleRoutineTasks(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, routine_id: str, operation_parameters: Dict[str, Any] = None) -> str:
        """
        Execute and test routine operations in the smart home management system.
        Handles test execution, retrieving test results, and manual triggering of routines.
        """
        
        def generate_id(table: Dict[str, Any]) -> int:
            if not table:
                return 1
            return max(int(k) for k in table.keys()) + 1
        
        # Validate operation type
        valid_operations = ["test_execution", "get_test_results", "manual_trigger"]
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
        
        # Get relevant tables from schema
        routines = data.get("routines", {})
        devices = data.get("devices", {})
        routine_execution_logs = data.get("routine_execution_logs", {})
        
        # Validate routine exists
        if routine_id not in routines:
            return json.dumps({
                "success": False,
                "error": f"Halt: Routine not found - routine_id '{routine_id}' does not exist"
            })
        
        routine = routines[routine_id]
        
        if operation == "test_execution":
            # Parse device actions from JSON string
            try:
                device_actions = json.loads(routine.get("device_actions", "[]"))
            except (json.JSONDecodeError, TypeError):
                device_actions = routine.get("device_actions", [])
                if not isinstance(device_actions, list):
                    device_actions = []
            
            test_results = []
            overall_success = True
            
            # Test each device action
            for action in device_actions:
                device_id = action.get("device_id")
                action_type = action.get("action")
                parameters = action.get("parameters", {})
                
                # Check if device exists
                if device_id not in devices:
                    test_results.append({
                        "device_id": device_id,
                        "action": action_type,
                        "status": "failed",
                        "error": "Device not found"
                    })
                    overall_success = False
                    continue
                
                device = devices[device_id]
                
                # Check device connection status
                if device.get("connection_status") != "online":
                    test_results.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "action": action_type,
                        "status": "failed",
                        "error": f"Device offline"
                    })
                    overall_success = False
                    continue
                
                # Check signal strength
                signal_strength = device.get("signal_strength", -50)
                if signal_strength and signal_strength < -70:
                    test_results.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "action": action_type,
                        "status": "success_with_warning",
                        "warning": f"Weak signal: {signal_strength} dBm"
                    })
                else:
                    test_results.append({
                        "device_id": device_id,
                        "device_name": device.get("device_name"),
                        "action": action_type,
                        "status": "success"
                    })
            
            # Create test execution log entry
            new_log_id = generate_id(routine_execution_logs)
            test_log_entry = {
                "execution_id": str(new_log_id),
                "routine_id": routine_id,
                "timestamp": "2025-10-16T14:30:00",
                "trigger_source": "test",
                "outcome": "success" if overall_success else "failure",
                "execution_duration_ms": 250,
                "device_execution_details": json.dumps(test_results)
            }
            routine_execution_logs[str(new_log_id)] = test_log_entry
            
            return json.dumps({
                "success": True,
                "operation": "test_execution",
                "routine_id": routine_id,
                "execution_id": str(new_log_id),
                "test_results": {
                    "overall_success": overall_success,
                    "device_results": test_results
                },
                "message": f"Test execution completed for routine '{routine.get('routine_name')}'"
            })
        
        elif operation == "get_test_results":
            # Get the most recent test execution from logs
            test_logs = []
            for log_id, log_entry in routine_execution_logs.items():
                if (log_entry.get("routine_id") == routine_id and 
                    log_entry.get("trigger_source") == "test"):
                    test_logs.append(log_entry)
            
            if not test_logs:
                return json.dumps({
                    "success": False,
                    "error": f"No test results found for routine '{routine_id}'"
                })
            
            # Sort by timestamp and get most recent
            test_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            latest_test = test_logs[0]
            
            # Parse device execution details
            try:
                device_results = json.loads(latest_test.get("device_execution_details", "[]"))
            except (json.JSONDecodeError, TypeError):
                device_results = []
            
            return json.dumps({
                "success": True,
                "operation": "get_test_results",
                "routine_id": routine_id,
                "execution_id": latest_test.get("execution_id"),
                "test_timestamp": latest_test.get("timestamp"),
                "test_results": {
                    "outcome": latest_test.get("outcome"),
                    "execution_duration_ms": latest_test.get("execution_duration_ms"),
                    "device_results": device_results
                },
                "message": f"Retrieved test results for routine '{routine.get('routine_name')}'"
            })
        
        elif operation == "manual_trigger":
            # Check routine status
            if routine.get("status") == "disabled":
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Routine '{routine_id}' is disabled"
                })
            
            # Get optional parameters
            if not operation_parameters:
                operation_parameters = {}
            
            test_mode = operation_parameters.get("test_mode", False)
            user_id = operation_parameters.get("user_id")
            
            # Parse device actions
            try:
                device_actions = json.loads(routine.get("device_actions", "[]"))
            except (json.JSONDecodeError, TypeError):
                device_actions = routine.get("device_actions", [])
                if not isinstance(device_actions, list):
                    device_actions = []
            
            execution_results = []
            execution_success = True
            error_messages = []
            
            # Execute each device action
            for action in device_actions:
                device_id = action.get("device_id")
                action_type = action.get("action")
                
                if device_id not in devices:
                    execution_results.append({
                        "device_id": device_id,
                        "status": "failed",
                        "error": "Device not found"
                    })
                    error_messages.append(f"Device {device_id} not found")
                    execution_success = False
                    continue
                
                device = devices[device_id]
                
                if device.get("connection_status") != "online":
                    execution_results.append({
                        "device_id": device_id,
                        "status": "failed", 
                        "error": "Device offline"
                    })
                    error_messages.append(f"Device {device_id} offline")
                    execution_success = False
                    continue
                
                # Execute action (update device state if not test mode)
                if not test_mode:
                    if action_type in ["turn_on", "activate", "enable", "lock"]:
                        device["status"] = "active"
                    elif action_type in ["turn_off", "deactivate", "disable", "unlock"]:
                        device["status"] = "suspended"
                
                execution_results.append({
                    "device_id": device_id,
                    "device_name": device.get("device_name"),
                    "action": action_type,
                    "status": "executed"
                })
            
            # Update routine execution count and last execution
            current_count = routine.get("execution_count", 0)
            routine["execution_count"] = current_count + 1
            routine["last_execution"] = "2025-10-16T14:35:00"
            
            # Create execution log
            new_log_id = generate_id(routine_execution_logs)
            log_entry = {
                "execution_id": str(new_log_id),
                "routine_id": routine_id,
                "timestamp": "2025-10-16T14:35:00",
                "triggered_by_user_id": user_id,
                "trigger_source": "manual",
                "outcome": "success" if execution_success else "failure",
                "error_message": "; ".join(error_messages) if error_messages else None,
                "execution_duration_ms": 500,
                "device_execution_details": json.dumps(execution_results)
            }
            routine_execution_logs[str(new_log_id)] = log_entry
            
            return json.dumps({
                "success": True,
                "operation": "manual_trigger",
                "routine_id": routine_id,
                "execution_id": str(new_log_id),
                "test_mode": test_mode,
                "execution_status": "success" if execution_success else "partial_failure",
                "devices_executed": len(execution_results),
                "errors": error_messages if error_messages else None,
                "message": f"Routine '{routine.get('routine_name')}' manually triggered"
            })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "handle_routine_tasks",
                "description": "Execute and test routine operations in the smart home management system. Handles test execution to validate routine functionality, retrieves cached test results for analysis, and enables manual triggering of routines. Validates routine existence, checks device availability and connection status, simulates device actions during tests, and creates execution logs for audit trails. Essential for routine testing, troubleshooting, and manual control.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Operation to perform on the routine",
                            "enum": ["test_execution", "get_test_results", "manual_trigger"]
                        },
                        "routine_id": {
                            "type": "string",
                            "description": "Unique identifier of the routine to operate on"
                        },
                        "operation_parameters": {
                            "type": "object",
                            "description": "Optional parameters for manual_trigger operation",
                            "properties": {
                                "test_mode": {
                                    "type": "boolean",
                                    "description": "If true, simulates execution without changing device states (for manual_trigger)"
                                },
                                "user_id": {
                                    "type": "string",
                                    "description": "ID of user triggering the routine (for manual_trigger)"
                                }
                            }
                        }
                    },
                    "required": ["operation", "routine_id"]
                }
            }
        }