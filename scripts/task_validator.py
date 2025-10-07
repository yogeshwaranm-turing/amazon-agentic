#!/usr/bin/env python3
"""
Task Validator - Executes action sequences from task.json files and validates outputs.

This script:
1. Loads task.json files 
2. Dynamically loads the specified environment
3. Executes each action in sequence
4. Compares actual outputs with expected outputs
5. Reports detailed validation results
"""

# Import mock tau_bench first to bypass dependency issues
try:
    from mock_tau_bench import *  # This sets up the mock modules
except ImportError:
    pass  # If mock not available, continue (for local development)

# Import our simple environment loader
try:
    from simple_env_loader import load_environment, get_available_environments
    SIMPLE_LOADER_AVAILABLE = True
except ImportError:
    print("Warning: Simple environment loader not available, falling back to complex method")
    SIMPLE_LOADER_AVAILABLE = False

import argparse
import json
import os
import sys
import importlib
import inspect
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
import logging

# Add the project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class ValidationResult:
    """Result of validating a single action"""
    action_name: str
    success: bool
    expected_output: Any
    actual_output: Any
    error: Optional[str] = None
    execution_time_ms: Optional[float] = None
    data_type_matches: bool = True

@dataclass
class TaskValidationResult:
    """Result of validating an entire task"""
    task_file: str
    environment: str
    success: bool
    actions_validated: int
    action_results: List[ValidationResult]
    error: Optional[str] = None
    execution_time_ms: float = 0.0

class OutputComparator:
    """Handles precise comparison of expected vs actual outputs"""
    
    @staticmethod
    def compare_outputs(expected: Any, actual: Any) -> Tuple[bool, List[str]]:
        """
        Compare two outputs with strict type and value checking.
        
        Returns:
            (matches, differences): Boolean and list of difference descriptions
        """
        differences = []
        
        # Check if both are None
        if expected is None and actual is None:
            return True, []
        
        if expected is None or actual is None:
            differences.append(f"One value is None: expected={expected}, actual={actual}")
            return False, differences
        
        # Check type matching
        if type(expected) != type(actual):
            differences.append(f"Type mismatch: expected {type(expected).__name__}, got {type(actual).__name__}")
            
            # Try to see if values are equivalent despite type difference
            try:
                if str(expected) == str(actual):
                    differences.append("Values are equivalent as strings but types differ")
                elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                    if float(expected) == float(actual):
                        differences.append("Numeric values are equal but types differ (int vs float)")
            except:
                pass
            
            return False, differences
        
        # Compare based on type
        if isinstance(expected, dict):
            return OutputComparator._compare_dicts(expected, actual)
        elif isinstance(expected, list):
            return OutputComparator._compare_lists(expected, actual)
        elif isinstance(expected, (int, float)):
            return OutputComparator._compare_numbers(expected, actual)
        elif isinstance(expected, str):
            matches = expected == actual
            if not matches:
                differences.append(f"String mismatch: expected '{expected}', got '{actual}'")
            return matches, differences
        elif isinstance(expected, bool):
            matches = expected == actual
            if not matches:
                differences.append(f"Boolean mismatch: expected {expected}, got {actual}")
            return matches, differences
        else:
            # Generic comparison for other types
            matches = expected == actual
            if not matches:
                differences.append(f"Value mismatch: expected {expected}, got {actual}")
            return matches, differences
    
    @staticmethod
    def _compare_dicts(expected: dict, actual: dict) -> Tuple[bool, List[str]]:
        """Compare two dictionaries"""
        differences = []
        all_keys = set(expected.keys()) | set(actual.keys())
        
        for key in all_keys:
            if key not in expected:
                differences.append(f"Unexpected key '{key}' in actual output")
            elif key not in actual:
                differences.append(f"Missing key '{key}' in actual output")
            else:
                key_matches, key_diffs = OutputComparator.compare_outputs(expected[key], actual[key])
                if not key_matches:
                    for diff in key_diffs:
                        differences.append(f"In key '{key}': {diff}")
        
        return len(differences) == 0, differences
    
    @staticmethod
    def _compare_lists(expected: list, actual: list) -> Tuple[bool, List[str]]:
        """Compare two lists with support for unordered comparison"""
        differences = []
        
        if len(expected) != len(actual):
            differences.append(f"List length mismatch: expected {len(expected)}, got {len(actual)}")
            return False, differences
        
        # First try exact ordered comparison
        ordered_match = True
        ordered_differences = []
        
        for i, (exp_item, act_item) in enumerate(zip(expected, actual)):
            item_matches, item_diffs = OutputComparator.compare_outputs(exp_item, act_item)
            if not item_matches:
                ordered_match = False
                for diff in item_diffs:
                    ordered_differences.append(f"At index {i}: {diff}")
        
        # If ordered comparison succeeds, return success
        if ordered_match:
            return True, []
        
        # If ordered comparison fails, try unordered comparison for simple types
        # This handles cases like ["hr_manager", "compliance_officer"] vs ["compliance_officer", "hr_manager"]
        if all(isinstance(item, (str, int, float, bool)) for item in expected + actual):
            # For arrays of simple types, check if they contain the same elements
            try:
                expected_sorted = sorted(expected)
                actual_sorted = sorted(actual)
                if expected_sorted == actual_sorted:
                    return True, []
            except TypeError:
                # If items can't be sorted (mixed types), fall back to set comparison
                if set(expected) == set(actual):
                    return True, []
        
        # If unordered comparison also fails, return the original ordered differences
        return False, ordered_differences
    
    @staticmethod
    def _compare_numbers(expected: Union[int, float], actual: Union[int, float]) -> Tuple[bool, List[str]]:
        """Compare two numbers with tolerance for floating point precision"""
        differences = []
        
        # For exact integer comparison
        if isinstance(expected, int) and isinstance(actual, int):
            matches = expected == actual
            if not matches:
                differences.append(f"Integer mismatch: expected {expected}, got {actual}")
            return matches, differences
        
        # For floating point comparison with small tolerance
        tolerance = 1e-10
        if abs(float(expected) - float(actual)) <= tolerance:
            return True, []
        else:
            differences.append(f"Number mismatch: expected {expected}, got {actual}")
            return False, differences

class EnvironmentLoader:
    """Dynamically loads and manages different environments"""
    
    # Cache for loaded tools to avoid reloading
    _tool_cache = {}
    
    @staticmethod
    def load_environment(env_name: str) -> Tuple[Any, Dict[str, Any]]:
        """
        Load environment and its data.
        
        Returns:
            (env_module, env_data): Environment module and loaded data
        """
        try:
            # For hr_experts and fund_finance, we load data directly and create a minimal module
            # since we're bypassing tau_bench entirely
            if env_name in ["hr_experts", "fund_finance"]:
                print(f"Loading {env_name} environment with direct data access")
                module_name = env_name.replace('_', '').title() + 'Module'
                env_module = type(module_name, (), {'__name__': env_name})()
            else:
                # Load environment module with better error handling
                env_module_path = f"envs.{env_name}"
                
                # Try to suppress tau_bench import errors during module loading
                import warnings
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    
                    try:
                        env_module = importlib.import_module(env_module_path)
                    except ModuleNotFoundError as e:
                        if 'tau_bench' in str(e):
                            # If it's a tau_bench import error, create a minimal module
                            print(f"Warning: tau_bench dependency issue in {env_name}, using minimal module")
                            env_module = type('MinimalEnvModule', (), {})()
                        else:
                            raise e
                    except SyntaxError as e:
                        if 'match' in str(e) or 'case' in str(e):
                            print(f"Warning: Python version incompatibility in {env_name} (requires Python 3.10+), using minimal module")
                            env_module = type('MinimalEnvModule', (), {})()
                        else:
                            raise e
                    except (ImportError, AttributeError) as e:
                        if 'tau_bench' in str(e) or any(name in str(e) for name in ['MockFundFinanceDomainEnv', 'MockFinanceDomainEnv', 'load_data', 'RULES', 'WIKI']):
                            print(f"Warning: tau_bench dependency issue in {env_name}, using minimal module: {e}")
                            env_module = type('MinimalEnvModule', (), {})()
                        else:
                            raise e
            
            # Load environment data
            env_data_path = project_root / "envs" / env_name / "data"
            env_data = {}
            
            if env_data_path.exists():
                for data_file in env_data_path.glob("*.json"):
                    with open(data_file, 'r') as f:
                        key = data_file.stem  # filename without extension
                        env_data[key] = json.load(f)
                print(f"Loaded data files for {env_name}: {list(env_data.keys())}")
            else:
                print(f"Warning: No data directory found for environment '{env_name}'")
            
            return env_module, env_data
            
        except ImportError as e:
            if 'tau_bench' in str(e) or any(name in str(e) for name in ['MockFundFinanceDomainEnv', 'MockFinanceDomainEnv', 'MockHRExpertsDomainEnv', 'load_data', 'RULES', 'WIKI']):
                print(f"Warning: tau_bench dependency issue in {env_name}, using minimal module")
                # Return minimal environment for tau_bench related errors
                minimal_module = type('MinimalEnvModule', (), {})()
                return minimal_module, {}
            else:
                raise ImportError(f"Could not load environment '{env_name}': {e}")
        except SyntaxError as e:
            print(f"Warning: Skipping environment '{env_name}' due to Python version incompatibility: {e}")
            minimal_module = type('MinimalEnvModule', (), {})()
            return minimal_module, {}
        except Exception as e:
            print(f"Warning: Skipping environment '{env_name}' due to error: {e}")
            minimal_module = type('MinimalEnvModule', (), {})()
            return minimal_module, {}
    
    @staticmethod
    def load_all_tools(env_name: str, interface_num: int = 1) -> Dict[str, Any]:
        """
        Bulk load all tools from an environment to avoid loading them one by one.
        Returns a dictionary of tool_name -> tool_class.
        """
        cache_key = f"{env_name}_{interface_num}"
        
        # Check cache first
        if cache_key in EnvironmentLoader._tool_cache:
            return EnvironmentLoader._tool_cache[cache_key]
        
        tools = {}
        tools_dir = project_root / "envs" / env_name / "tools" / f"interface_{interface_num}"
        
        if not tools_dir.exists():
            print(f"Warning: Tools directory '{tools_dir}' does not exist")
            return tools
        
        print(f"Bulk loading tools from {env_name}/interface_{interface_num}...")
        
        # Load all .py files in the tools directory
        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name in ['__init__.py', 'policy.md']:
                continue
                
            tool_name = tool_file.stem
            try:
                # Read and execute the tool file directly
                with open(tool_file, 'r') as f:
                    tool_code = f.read()
                
                # Remove tau_bench imports and replace with mock Tool class
                mock_tool_code = tool_code.replace(
                    "from tau_bench.envs.tool import Tool", 
                    "class Tool:\n    pass"
                )
                
                # Create a namespace for executing the tool code
                tool_namespace = {}
                
                # Execute the modified tool code
                exec(mock_tool_code, tool_namespace)
                
                # Find the tool class
                for name, obj in tool_namespace.items():
                    if (inspect.isclass(obj) and 
                        hasattr(obj, 'invoke') and 
                        name != 'Tool'):
                        
                        # Apply environment-specific wrappers
                        wrapped_tool = EnvironmentLoader._apply_tool_wrapper(
                            obj, tool_name, env_name
                        )
                        tools[tool_name] = wrapped_tool
                        break
                        
            except Exception as e:
                print(f"Warning: Could not load tool '{tool_name}': {e}")
                continue
        
        print(f"Loaded {len(tools)} tools: {list(tools.keys())}")
        
        # Cache the loaded tools
        EnvironmentLoader._tool_cache[cache_key] = tools
        return tools
    
    @staticmethod
    def _apply_tool_wrapper(original_tool: Any, tool_name: str, env_name: str) -> Any:
        """Apply environment-specific wrappers to tools"""
        
        # HR Experts wrappers
        if env_name == 'hr_experts':
            hr_experts_mappings = {
                'discover_user_entities': 'users',
                'discover_employee_entities': 'employees'
            }
            
            if tool_name in hr_experts_mappings:
                entity_type = hr_experts_mappings[tool_name]
                
                class HRExpertsWrapper:
                    @staticmethod
                    def invoke(data, **kwargs):
                        filters = {k: v for k, v in kwargs.items()}
                        result = original_tool.invoke(data, entity_type=entity_type, filters=filters)
                        # Return just the results array for hr_experts format
                        if isinstance(result, str):
                            parsed = json.loads(result)
                            return parsed.get("results", [])
                        elif isinstance(result, dict) and "results" in result:
                            return result["results"]
                        return result
                return HRExpertsWrapper
        
        # Fund Finance wrappers  
        elif env_name == 'fund_finance' and 'discover_' in tool_name:
            class FundFinanceDiscoverWrapper:
                @staticmethod
                def invoke(data, **kwargs):
                    # If entity_type is already provided, use the original tool directly
                    if 'entity_type' in kwargs:
                        result = original_tool.invoke(data, **kwargs)
                        # Return full response for fund_finance format
                        if isinstance(result, str):
                            return json.loads(result)
                        return result
                    else:
                        # Map tool names to entity types for legacy calls
                        entity_type_map = {
                            'discover_fund_entities': 'funds',
                            'discover_investor_entities': 'investors',
                            'discover_instrument_entities': 'instruments',
                            'discover_portfolio_entities': 'portfolios',
                            'discover_trading_entities': 'trades',
                            'discover_billing_entities': 'invoices',
                            'discover_reporting_entities': 'reports',
                            'discover_user_entities': 'users',
                            'discover_valuation_entities': 'nav_records',
                            'discover_investment_flow_entities': 'commitments',
                            'discover_system_entities': 'audit_trails'
                        }
                        
                        expected_entity_type = entity_type_map.get(tool_name)
                        if expected_entity_type:
                            filters = kwargs if kwargs else None
                            result = original_tool.invoke(data, entity_type=expected_entity_type, filters=filters)
                            # Return just the results array for legacy format
                            if isinstance(result, str):
                                parsed = json.loads(result)
                                return parsed.get("results", [])
                            elif isinstance(result, dict) and "results" in result:
                                return result["results"]
                        return result
            return FundFinanceDiscoverWrapper
        
        # Return original tool if no wrapper needed
        return original_tool
    
    @staticmethod
    def get_tool_class(env_module: Any, tool_name: str, interface_num: int = 1) -> Any:
        """
        Get the tool class from the environment module.
        Uses bulk-loaded tools for efficiency.
        
        Args:
            env_module: Loaded environment module 
            tool_name: Name of the tool to load
            interface_num: Interface number (1, 2, 3, etc.)
        """
        try:
            # Determine environment name from module
            env_name = getattr(env_module, '__name__', 'unknown')
            if 'hr_experts' in env_name.lower():
                env_name = 'hr_experts'
            elif 'fund_finance' in env_name.lower() or 'fundfinance' in env_name.lower():
                env_name = 'fund_finance'
            
            # Get all tools for this environment (bulk load)
            all_tools = EnvironmentLoader.load_all_tools(env_name, interface_num)
            
            # Handle tool name mappings for hr_experts
            if env_name == 'hr_experts':
                hr_experts_mappings = {
                    'discover_user_entities': 'discover_user_employee_entities',
                    'discover_employee_entities': 'discover_user_employee_entities',
                }
                actual_tool_name = hr_experts_mappings.get(tool_name, tool_name)
            else:
                actual_tool_name = tool_name
            
            # Look for the tool in our loaded tools
            if actual_tool_name in all_tools:
                return all_tools[actual_tool_name]
            elif tool_name in all_tools:
                return all_tools[tool_name]
            else:
                print(f"Warning: Tool '{tool_name}' not found in {env_name}/interface_{interface_num}")
                print(f"Available tools: {list(all_tools.keys())}")
                return None
            
        except Exception as e:
            print(f"Warning: Could not load tool '{tool_name}' from interface {interface_num}: {e}")
            return None

class TaskExecutor:
    """Executes task action sequences and validates outputs"""
    
    def __init__(self, env_name: str, interface_num: int = 1):
        self.env_name = env_name
        self.interface_num = interface_num
        
        # Use simple environment loader if available
        if SIMPLE_LOADER_AVAILABLE:
            self.simple_env = load_environment(env_name)
            self.env_data = self.simple_env.data
            self.env_tools = self.simple_env.tools
        else:
            # Fallback to complex method
            self.env_module, self.env_data = EnvironmentLoader.load_environment(env_name)
            self.env_tools = None
            
        self.execution_context = {}  # Store outputs from previous actions
        
    def execute_action(self, action: Dict[str, Any]) -> ValidationResult:
        """Execute a single action and validate its output"""
        action_name = action["name"]
        action_args = action["arguments"]
        expected_output = action.get("output", None)  # Make output optional
        
        start_time = datetime.now()
        
        try:
            # Use simple environment loader if available
            if SIMPLE_LOADER_AVAILABLE and self.env_tools:
                # Simple approach - just get the tool from the loaded tools
                if action_name not in self.env_tools:
                    execution_time = (datetime.now() - start_time).total_seconds() * 1000
                    return ValidationResult(
                        action_name=action_name,
                        success=False,
                        expected_output=expected_output,
                        actual_output=None,
                        error=f"Tool '{action_name}' not found in environment",
                        execution_time_ms=execution_time
                    )
                
                tool = self.env_tools[action_name]
                
                # Prepare arguments by resolving any references to previous outputs
                resolved_args = self._resolve_arguments(action_args)
                
                # Execute the tool with environment data
                actual_output = tool.invoke(self.env_data, **resolved_args)
                
            else:
                # Fallback to complex method
                # Load the tool class
                tool_class = EnvironmentLoader.get_tool_class(
                    self.env_module, action_name, self.interface_num
                )
                
                # Handle case where tool couldn't be loaded (tau_bench dependency issues)
                if tool_class is None:
                    execution_time = (datetime.now() - start_time).total_seconds() * 1000
                    return ValidationResult(
                        action_name=action_name,
                        success=False,
                        expected_output=expected_output,
                        actual_output=None,
                        error=f"Tool '{action_name}' could not be loaded due to dependency issues",
                        execution_time_ms=execution_time
                    )
                
                # Prepare arguments by resolving any references to previous outputs
                resolved_args = self._resolve_arguments(action_args)
                
                # Execute the tool
                if hasattr(tool_class, 'invoke'):
                    # Add environment data to arguments if the tool expects it
                    if 'data' in inspect.signature(tool_class.invoke).parameters:
                        actual_output = tool_class.invoke(data=self.env_data, **resolved_args)
                    else:
                        actual_output = tool_class.invoke(**resolved_args)
                else:
                    raise AttributeError(f"Tool {action_name} does not have invoke method")
            
            # Parse JSON output if it's a string
            if isinstance(actual_output, str):
                try:
                    actual_output = json.loads(actual_output)
                except json.JSONDecodeError:
                    pass  # Keep as string if not valid JSON
            
            # Store output for future action references
            self.execution_context[action_name] = actual_output
            
            # Compare outputs (skip validation if no expected output)
            if expected_output is not None:
                matches, differences = OutputComparator.compare_outputs(expected_output, actual_output)
                data_type_matches = type(expected_output) == type(actual_output)
            else:
                # No expected output to compare against - consider successful execution
                matches = True
                differences = []
                data_type_matches = True
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ValidationResult(
                action_name=action_name,
                success=matches,
                expected_output=expected_output,
                actual_output=actual_output,
                error=None if matches else "; ".join(differences),
                execution_time_ms=execution_time,
                data_type_matches=data_type_matches
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return ValidationResult(
                action_name=action_name,
                success=False,
                expected_output=expected_output,
                actual_output=None,
                error=f"Execution failed: {str(e)}",
                execution_time_ms=execution_time,
                data_type_matches=False
            )
    
    def _resolve_arguments(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve argument references to previous action outputs and parse JSON strings.
        """
        resolved = {}
        
        for key, value in args.items():
            # Parse JSON strings that look like JSON objects/arrays
            if isinstance(value, str) and value.strip().startswith(('{', '[')):
                try:
                    resolved[key] = json.loads(value)
                except json.JSONDecodeError:
                    # Try to fix Python-style booleans and retry
                    try:
                        fixed_value = value.replace('True', 'true').replace('False', 'false').replace('None', 'null')
                        resolved[key] = json.loads(fixed_value)
                    except json.JSONDecodeError:
                        # If still not valid JSON, keep as string
                        resolved[key] = value
            else:
                resolved[key] = value
        
        return resolved
    
    def validate_task(self, task_data: Dict[str, Any]) -> TaskValidationResult:
        """Validate an entire task by executing all actions in sequence"""
        task_info = task_data.get("task", {})
        actions = task_info.get("actions", [])
        
        start_time = datetime.now()
        action_results = []
        
        try:
            for action in actions:
                result = self.execute_action(action)
                action_results.append(result)
                
                # Stop on first failure for now
                if not result.success:
                    break
            
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            overall_success = all(result.success for result in action_results)
            
            return TaskValidationResult(
                task_file="",  # Will be set by caller
                environment=self.env_name,
                success=overall_success,
                actions_validated=len(action_results),
                action_results=action_results,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return TaskValidationResult(
                task_file="",  # Will be set by caller
                environment=self.env_name,
                success=False,
                actions_validated=len(action_results),
                action_results=action_results,
                error=f"Task execution failed: {str(e)}",
                execution_time_ms=execution_time
            )

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_task_file(task_file_path: str) -> Dict[str, Any]:
    """Load and parse a task.json file"""
    try:
        with open(task_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load task file {task_file_path}: {e}")

def validate_single_task(task_file_path: str) -> TaskValidationResult:
    """Validate a single task file"""
    logging.info(f"Validating task: {task_file_path}")
    
    try:
        # Load task file
        task_data = load_task_file(task_file_path)
        
        # Get environment and interface info
        env_name = task_data.get("env")
        interface_num = task_data.get("interface_num", 1)
        
        if not env_name:
            raise ValueError("Task file missing 'env' field")
        
        # Create executor and validate
        executor = TaskExecutor(env_name, interface_num)
        result = executor.validate_task(task_data)
        result.task_file = task_file_path
        
        return result
        
    except Exception as e:
        return TaskValidationResult(
            task_file=task_file_path,
            environment="unknown",
            success=False,
            actions_validated=0,
            action_results=[],
            error=str(e)
        )

def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description="Validate task.json files")
    parser.add_argument("--tasks", required=True, help="Space-separated list of task.json files")
    parser.add_argument("--environment", help="Filter by specific environment")
    parser.add_argument("--output-format", choices=["json", "text"], default="json")
    parser.add_argument("--report-file", default="validation-report.json")
    
    args = parser.parse_args()
    
    setup_logging()
    
    # Parse task files
    task_files = args.tasks.strip().split()
    if not task_files or task_files == ['']:
        logging.info("No task files provided - creating empty report")
        
        # Create empty report
        empty_report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "success_rate": 100.0
            },
            "results": [],
            "message": "No task files found to validate"
        }
        
        # Save empty report
        with open(args.report_file, 'w') as f:
            json.dump(empty_report, f, indent=2)
        
        print("✅ No validation needed - no task files found")
        return 0
    
    logging.info(f"Found {len(task_files)} task files to validate")
    
    # Validate each task
    results = []
    for task_file in task_files:
        if not os.path.exists(task_file):
            logging.warning(f"Task file not found: {task_file}")
            continue
            
        # Filter by environment if specified
        if args.environment:
            try:
                task_data = load_task_file(task_file)
                if task_data.get("env") != args.environment:
                    logging.info(f"Skipping {task_file} (environment {task_data.get('env')} != {args.environment})")
                    continue
            except:
                logging.warning(f"Could not check environment for {task_file}")
                continue
        
        result = validate_single_task(task_file)
        results.append(result)
        
        # Log result
        status = "✅ PASS" if result.success else "❌ FAIL"
        logging.info(f"{status} {task_file} ({result.actions_validated} actions)")
        if not result.success and result.error:
            logging.error(f"  Error: {result.error}")
    
    # Generate summary
    passed = sum(1 for r in results if r.success)
    failed = len(results) - passed
    
    summary = {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "success_rate": (passed / len(results) * 100) if results else 0
    }
    
    # Create report
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "results": []
    }
    
    # Process each result with proper argument extraction
    for r in results:
        # Load task file to get arguments
        task_data = None
        try:
            task_data = load_task_file(r.task_file)
        except:
            pass
        
        task_actions = task_data.get('task', {}).get('actions', []) if task_data else []
        
        result_entry = {
            "task_file": r.task_file,
            "environment": r.environment,
            "success": r.success,
            "actions_validated": r.actions_validated,
            "execution_time_ms": r.execution_time_ms,
            "error": r.error,
            "action_results": []
        }
        
        for i, ar in enumerate(r.action_results):
            # Get arguments from original task if available
            arguments = {}
            if i < len(task_actions):
                arguments = task_actions[i].get('arguments', {})
            
            action_result = {
                "action_name": ar.action_name,
                "success": ar.success,
                "error": ar.error,
                "data_type_matches": ar.data_type_matches,
                "execution_time_ms": ar.execution_time_ms,
                "arguments": arguments,
                "expected_output": ar.expected_output,
                "actual_output": ar.actual_output
            }
            result_entry["action_results"].append(action_result)
        
        report["results"].append(result_entry)
    
    # Save report
    with open(args.report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"VALIDATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total tasks: {summary['total']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success rate: {summary['success_rate']:.1f}%")
    print(f"Report saved to: {args.report_file}")
    
    if failed > 0:
        print(f"\n❌ {failed} task(s) failed validation")
        sys.exit(1)
    else:
        print(f"\n✅ All tasks passed validation!")

if __name__ == "__main__":
    main()