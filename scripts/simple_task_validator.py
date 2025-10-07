#!/usr/bin/env python3
"""
Simple Task Validator - Dead simple task validation using the simple environment loader.

This replaces the complex task_validator.py with a much simpler approach that:
1. Uses simple_env_loader to load any environment effortlessly
2. Validates task.json files against real tool execution
3. Works reliably in GitHub Actions without complex setup
4. Handles all environments uniformly

Usage:
    python3 simple_task_validator.py --task-file path/to/task.json
    python3 simple_task_validator.py --env hr_experts --all-tasks
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

# Import our simple environment loader
from simple_env_loader import load_environment, get_available_environments

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of validating a single action"""
    action_name: str
    success: bool
    expected_output: Any
    actual_output: Any
    error: Optional[str] = None

@dataclass
class TaskValidationResult:
    """Result of validating an entire task"""
    task_file: str
    environment: str
    success: bool
    total_actions: int
    passed_actions: int
    failed_actions: int
    results: List[ValidationResult]
    error: Optional[str] = None

def validate_task_file(task_file: str, project_root: Optional[str] = None) -> TaskValidationResult:
    """
    Validate a single task.json file.
    
    Args:
        task_file: Path to the task.json file
        project_root: Path to project root (auto-detected if None)
    
    Returns:
        TaskValidationResult with validation results
    """
    task_path = Path(task_file)
    
    if not task_path.exists():
        return TaskValidationResult(
            task_file=task_file,
            environment="unknown",
            success=False,
            total_actions=0,
            passed_actions=0,
            failed_actions=0,
            results=[],
            error=f"Task file not found: {task_file}"
        )
    
    try:
        # Load task.json
        with open(task_path, 'r') as f:
            task_data = json.load(f)
        
        # Determine environment from path or task data
        env_name = _determine_environment(task_path, task_data)
        
        if not env_name:
            return TaskValidationResult(
                task_file=task_file,
                environment="unknown",
                success=False,
                total_actions=0,
                passed_actions=0,
                failed_actions=0,
                results=[],
                error="Could not determine environment"
            )
        
        # Load environment
        logger.info(f"Loading environment: {env_name}")
        env = load_environment(env_name, project_root)
        
        # Validate actions
        results = []
        actions = task_data.get('actions', [])
        
        # Handle nested task structure
        if 'task' in task_data and 'actions' in task_data['task']:
            actions = task_data['task']['actions']
        
        for i, action in enumerate(actions):
            result = _validate_action(action, env, i)
            results.append(result)
        
        # Calculate summary
        passed = sum(1 for r in results if r.success)
        failed = len(results) - passed
        overall_success = failed == 0
        
        return TaskValidationResult(
            task_file=task_file,
            environment=env_name,
            success=overall_success,
            total_actions=len(results),
            passed_actions=passed,
            failed_actions=failed,
            results=results
        )
        
    except Exception as e:
        logger.error(f"Failed to validate task {task_file}: {e}")
        return TaskValidationResult(
            task_file=task_file,
            environment="unknown",
            success=False,
            total_actions=0,
            passed_actions=0,
            failed_actions=0,
            results=[],
            error=str(e)
        )

def _determine_environment(task_path: Path, task_data: Dict[str, Any]) -> Optional[str]:
    """Determine environment from task file path or data"""
    
    # Method 1: Check if environment is in task data
    if 'environment' in task_data:
        return task_data['environment']
    
    # Method 2: Infer from file path
    path_parts = task_path.parts
    
    # Get available environments and sort by length (longest first) to avoid partial matches
    available_envs = sorted(get_available_environments(), key=len, reverse=True)
    
    # Look for environment names in the path - check longest names first
    for env in available_envs:
        for part in path_parts:
            if env in part:
                return env
    
    # Method 3: Check full path string
    path_str = str(task_path)
    for env in available_envs:
        if env in path_str:
            return env
    
    return None

def _validate_action(action: Dict[str, Any], env, action_index: int) -> ValidationResult:
    """Validate a single action against the environment"""
    
    # Try both 'name' and 'action' fields for the tool name
    tool_name = action.get('name') or action.get('action')
    action_name = tool_name or f'action_{action_index}'
    
    try:
        # Get tool arguments and expected output
        arguments = action.get('arguments', {})
        expected_output = action.get('output')
        
        if not tool_name:
            return ValidationResult(
                action_name=action_name,
                success=False,
                expected_output=expected_output,
                actual_output=None,
                error="No action specified"
            )
        
        # Check if tool exists
        if tool_name not in env.tools:
            return ValidationResult(
                action_name=action_name,
                success=False,
                expected_output=expected_output,
                actual_output=None,
                error=f"Tool '{tool_name}' not found in environment"
            )
        
        # Execute the tool
        tool = env.tools[tool_name]
        
        # Parse JSON string arguments if needed
        parsed_args = {}
        for key, value in arguments.items():
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                try:
                    parsed_args[key] = json.loads(value)
                except json.JSONDecodeError:
                    parsed_args[key] = value
            else:
                parsed_args[key] = value
        
        # Execute tool
        actual_output = tool.invoke(env.data, **parsed_args)
        
        # Compare outputs
        success = _compare_outputs(expected_output, actual_output)
        
        return ValidationResult(
            action_name=action_name,
            success=success,
            expected_output=expected_output,
            actual_output=actual_output
        )
        
    except Exception as e:
        logger.error(f"Error validating action {action_name}: {e}")
        return ValidationResult(
            action_name=action_name,
            success=False,
            expected_output=action.get('output'),
            actual_output=None,
            error=str(e)
        )

def _compare_outputs(expected: Any, actual: Any) -> bool:
    """Compare expected and actual outputs"""
    
    # Handle string/JSON parsing
    if isinstance(expected, str) and isinstance(actual, str):
        try:
            expected_parsed = json.loads(expected)
            actual_parsed = json.loads(actual)
            return _deep_compare(expected_parsed, actual_parsed)
        except json.JSONDecodeError:
            return expected == actual
    
    return _deep_compare(expected, actual)

def _deep_compare(obj1: Any, obj2: Any) -> bool:
    """Deep comparison of two objects, handling lists without order sensitivity"""
    
    if type(obj1) != type(obj2):
        return False
    
    if isinstance(obj1, dict):
        if set(obj1.keys()) != set(obj2.keys()):
            return False
        return all(_deep_compare(obj1[key], obj2[key]) for key in obj1.keys())
    
    elif isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        # For lists, try both ordered and unordered comparison
        if obj1 == obj2:
            return True
        # Try unordered comparison for lists of dicts
        if all(isinstance(item, dict) for item in obj1 + obj2):
            return sorted(obj1, key=lambda x: json.dumps(x, sort_keys=True)) == \
                   sorted(obj2, key=lambda x: json.dumps(x, sort_keys=True))
        return False
    
    else:
        return obj1 == obj2

def print_results(result: TaskValidationResult):
    """Print validation results in a nice format"""
    
    print(f"\n{'='*60}")
    print(f"Task: {result.task_file}")
    print(f"Environment: {result.environment}")
    print(f"Overall: {'✅ PASS' if result.success else '❌ FAIL'}")
    print(f"Actions: {result.passed_actions}/{result.total_actions} passed")
    
    if result.error:
        print(f"Error: {result.error}")
        return
    
    print(f"\n{'='*60}")
    
    for i, action_result in enumerate(result.results):
        status = "✅ PASS" if action_result.success else "❌ FAIL"
        print(f"\nAction {i+1}: {action_result.action_name} - {status}")
        
        if action_result.error:
            print(f"  Error: {action_result.error}")
        else:
            print(f"  Ground truth: {action_result.expected_output}")
            print(f"  Actual result: {action_result.actual_output}")

def validate_environment_tasks(env_name: str, project_root: Optional[str] = None) -> List[TaskValidationResult]:
    """Validate all task files for a specific environment"""
    
    if project_root is None:
        project_root = Path(__file__).parent.parent
    else:
        project_root = Path(project_root)
    
    env_path = project_root / "envs" / env_name
    
    if not env_path.exists():
        logger.error(f"Environment '{env_name}' not found")
        return []
    
    # Find all task.json files
    task_files = list(env_path.rglob("task.json"))
    
    if not task_files:
        logger.warning(f"No task.json files found for environment '{env_name}'")
        return []
    
    logger.info(f"Found {len(task_files)} task files for {env_name}")
    
    results = []
    for task_file in task_files:
        result = validate_task_file(str(task_file), str(project_root))
        results.append(result)
        print_results(result)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Simple Task Validator")
    parser.add_argument("--task-file", type=str, help="Path to a specific task.json file")
    parser.add_argument("--env", type=str, help="Environment name to validate all tasks for")
    parser.add_argument("--all-tasks", action="store_true", help="Validate all task files for the environment")
    parser.add_argument("--list-envs", action="store_true", help="List available environments")
    
    args = parser.parse_args()
    
    if args.list_envs:
        envs = get_available_environments()
        print("Available environments:")
        for env in envs:
            print(f"  - {env}")
        return
    
    if args.task_file:
        result = validate_task_file(args.task_file)
        print_results(result)
        sys.exit(0 if result.success else 1)
    
    elif args.env and args.all_tasks:
        results = validate_environment_tasks(args.env)
        
        # Summary
        total_tasks = len(results)
        passed_tasks = sum(1 for r in results if r.success)
        failed_tasks = total_tasks - passed_tasks
        
        print(f"\n{'='*60}")
        print(f"SUMMARY for {args.env}")
        print(f"Tasks: {passed_tasks}/{total_tasks} passed")
        print(f"Overall: {'✅ PASS' if failed_tasks == 0 else '❌ FAIL'}")
        
        sys.exit(0 if failed_tasks == 0 else 1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()