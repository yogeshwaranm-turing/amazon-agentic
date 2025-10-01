#!/usr/bin/env python3
"""
Mock tau_bench module to bypass dependencies during validation.
This allows tools to import tau_bench classes without requiring the full tau_bench package.
"""

import sys
from types import ModuleType

class Tool:
    """Mock Tool class that replaces tau_bench.envs.tool.Tool"""
    
    @staticmethod
    def invoke(data=None, **kwargs):
        """Default invoke method - should be overridden by actual tools"""
        return {"success": False, "error": "Tool not implemented"}

class UserStrategy:
    """Mock UserStrategy class"""
    pass

def load_user(*args, **kwargs):
    """Mock load_user function"""
    return None

# Mock tau_bench.types
class Action:
    """Mock Action class"""
    pass

class Task:
    """Mock Task class"""
    pass

# Create comprehensive mock module structure
def create_mock_module(name):
    """Create a mock module with the given name"""
    module = ModuleType(name)
    sys.modules[name] = module
    return module

# Create the complete tau_bench module hierarchy
tau_bench = create_mock_module('tau_bench')
tau_bench_envs = create_mock_module('tau_bench.envs')
tau_bench_envs_base = create_mock_module('tau_bench.envs.base')
tau_bench_envs_tool = create_mock_module('tau_bench.envs.tool')
tau_bench_envs_user = create_mock_module('tau_bench.envs.user')
tau_bench_types = create_mock_module('tau_bench.types')

# Set up the module attributes
tau_bench.envs = tau_bench_envs
tau_bench_envs.base = tau_bench_envs_base
tau_bench_envs.tool = tau_bench_envs_tool
tau_bench_envs.user = tau_bench_envs_user
tau_bench.types = tau_bench_types

# Add classes to appropriate modules
tau_bench_envs_tool.Tool = Tool
tau_bench_envs_user.load_user = load_user
tau_bench_envs_user.UserStrategy = UserStrategy
tau_bench_types.Action = Action
tau_bench_types.Task = Task

# Add base classes that might be imported
tau_bench_envs_base.Tool = Tool
tau_bench_envs_base.load_user = load_user
tau_bench_envs_base.UserStrategy = UserStrategy

print("Mock tau_bench modules installed successfully")