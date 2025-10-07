#!/usr/bin/env python3
"""
Simple Environment Loader - Dead simple way to load any environment with all its tools and data.

This module provides a one-stop solution to:
1. Load any environment (hr_experts, fund_finance, etc.)
2. Load all its data files
3. Load all tools from all interfaces
4. Handle environment-specific mappings automatically
5. Work reliably in GitHub Actions without complex setup

Usage:
    from simple_env_loader import load_environment
    env = load_environment('hr_experts')
    result = env.tools['check_approval'].invoke(env.data, ...)
"""

import json
import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleEnvironment:
    """A simple container for environment data and tools"""
    
    def __init__(self, name: str):
        self.name = name
        self.data = {}
        self.tools = {}
        self.interfaces = []
    
    def __repr__(self):
        return f"SimpleEnvironment(name='{self.name}', tools={len(self.tools)}, interfaces={len(self.interfaces)})"

def load_environment(env_name: str, project_root: Optional[str] = None) -> SimpleEnvironment:
    """
    Load an environment with all its data and tools.
    
    Args:
        env_name: Name of the environment (e.g., 'hr_experts', 'fund_finance')
        project_root: Path to project root (auto-detected if None)
    
    Returns:
        SimpleEnvironment with loaded data and tools
    """
    if project_root is None:
        # Auto-detect project root
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
    else:
        project_root = Path(project_root)
    
    env_path = project_root / "envs" / env_name
    
    if not env_path.exists():
        raise ValueError(f"Environment '{env_name}' not found at {env_path}")
    
    logger.info(f"Loading environment: {env_name}")
    env = SimpleEnvironment(env_name)
    
    # Load data
    _load_data(env, env_path)
    
    # Load tools from all interfaces
    _load_all_tools(env, env_path)
    
    logger.info(f"Successfully loaded {env}")
    return env

def _load_data(env: SimpleEnvironment, env_path: Path):
    """Load all data files for the environment"""
    data_path = env_path / "data"
    
    if not data_path.exists():
        logger.warning(f"No data directory found for {env.name}")
        return
    
    logger.info(f"Loading data from {data_path}")
    
    for data_file in data_path.glob("*.json"):
        if data_file.name.startswith('__'):
            continue
            
        table_name = data_file.stem
        try:
            with open(data_file, 'r') as f:
                env.data[table_name] = json.load(f)
            logger.debug(f"Loaded data table: {table_name}")
        except Exception as e:
            logger.error(f"Failed to load data file {data_file}: {e}")
    
    logger.info(f"Loaded {len(env.data)} data tables: {list(env.data.keys())}")

def _load_all_tools(env: SimpleEnvironment, env_path: Path):
    """Load tools from all interfaces"""
    tools_path = env_path / "tools"
    
    if not tools_path.exists():
        logger.warning(f"No tools directory found for {env.name}")
        return
    
    # Find all interface directories
    interface_dirs = [d for d in tools_path.iterdir() if d.is_dir() and d.name.startswith('interface_')]
    interface_dirs.sort()  # Process in order
    
    for interface_dir in interface_dirs:
        interface_num = interface_dir.name.split('_')[1]
        env.interfaces.append(int(interface_num))
        _load_interface_tools(env, interface_dir, int(interface_num))
    
    # Apply environment-specific mappings
    _apply_env_mappings(env)
    
    logger.info(f"Loaded {len(env.tools)} tools from {len(env.interfaces)} interfaces")

def _load_interface_tools(env: SimpleEnvironment, interface_dir: Path, interface_num: int):
    """Load tools from a specific interface directory"""
    logger.info(f"Loading tools from {interface_dir}")
    
    for tool_file in interface_dir.glob("*.py"):
        if tool_file.name in ['__init__.py', 'policy.md']:
            continue
            
        tool_name = tool_file.stem
        
        try:
            tool_class = _load_tool_class(tool_file)
            if tool_class:
                env.tools[tool_name] = tool_class()
                logger.debug(f"Loaded tool: {tool_name}")
        except Exception as e:
            logger.error(f"Failed to load tool {tool_name}: {e}")

def _load_tool_class(tool_file: Path):
    """Load a tool class from a Python file"""
    try:
        # Read the tool file
        with open(tool_file, 'r') as f:
            content = f.read()
        
        # Create a simple Tool base class to avoid tau_bench dependency
        tool_base = """
class Tool:
    def __init__(self):
        pass
"""
        
        # Replace tau_bench imports with our simple Tool class
        content = content.replace("from tau_bench.envs.tool import Tool", tool_base)
        
        # Create module spec and execute
        spec = importlib.util.spec_from_file_location(tool_file.stem, tool_file)
        module = importlib.util.module_from_spec(spec)
        
        # Execute the modified content
        exec(content, module.__dict__)
        
        # Find the tool class (should inherit from Tool and have invoke method)
        for name, obj in module.__dict__.items():
            if (isinstance(obj, type) and 
                hasattr(obj, 'invoke') and 
                name != 'Tool'):
                return obj
                
    except Exception as e:
        logger.error(f"Error loading tool from {tool_file}: {e}")
        return None

def _apply_env_mappings(env: SimpleEnvironment):
    """Apply environment-specific tool mappings"""
    
    if env.name == 'hr_experts':
        # HR Experts needs mapped tools for backwards compatibility
        if 'discover_user_employee_entities' in env.tools:
            base_tool = env.tools['discover_user_employee_entities']
            
            # Create discover_user_entities
            class DiscoverUserEntities:
                def invoke(self, data, **kwargs):
                    return base_tool.invoke(data, entity_type='users', filters=kwargs)
            
            # Create discover_employee_entities  
            class DiscoverEmployeeEntities:
                def invoke(self, data, **kwargs):
                    return base_tool.invoke(data, entity_type='employees', filters=kwargs)
            
            env.tools['discover_user_entities'] = DiscoverUserEntities()
            env.tools['discover_employee_entities'] = DiscoverEmployeeEntities()
            
            logger.info("Applied HR Experts tool mappings")
    
    # Add other environment mappings here as needed
    # elif env.name == 'fund_finance':
    #     # Add fund_finance specific mappings if needed
    #     pass

# Convenience functions
def get_available_environments(project_root: Optional[str] = None) -> List[str]:
    """Get list of available environments"""
    if project_root is None:
        project_root = Path(__file__).parent.parent
    else:
        project_root = Path(project_root)
    
    envs_path = project_root / "envs"
    if not envs_path.exists():
        return []
    
    environments = []
    for env_dir in envs_path.iterdir():
        if env_dir.is_dir() and not env_dir.name.startswith('__'):
            environments.append(env_dir.name)
    
    return sorted(environments)

def test_environment(env_name: str) -> bool:
    """Test if an environment can be loaded successfully"""
    try:
        env = load_environment(env_name)
        return len(env.tools) > 0
    except Exception as e:
        logger.error(f"Failed to test environment {env_name}: {e}")
        return False

if __name__ == "__main__":
    # Quick test/demo
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Environment Loader")
    parser.add_argument("--list", action="store_true", help="List available environments")
    parser.add_argument("--test", type=str, help="Test loading an environment")
    parser.add_argument("--load", type=str, help="Load and display environment info")
    
    args = parser.parse_args()
    
    if args.list:
        envs = get_available_environments()
        print("Available environments:")
        for env in envs:
            print(f"  - {env}")
    
    elif args.test:
        success = test_environment(args.test)
        print(f"Environment '{args.test}': {'✅ PASS' if success else '❌ FAIL'}")
    
    elif args.load:
        try:
            env = load_environment(args.load)
            print(f"Environment: {env.name}")
            print(f"Data tables: {list(env.data.keys())}")
            print(f"Tools: {list(env.tools.keys())}")
            print(f"Interfaces: {env.interfaces}")
        except Exception as e:
            print(f"Failed to load {args.load}: {e}")
    
    else:
        # Default: list environments
        envs = get_available_environments()
        print("Available environments:")
        for env in envs:
            status = "✅" if test_environment(env) else "❌"
            print(f"  {status} {env}")