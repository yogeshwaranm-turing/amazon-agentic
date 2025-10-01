#!/usr/bin/env python3
"""
Mock tau_bench module to bypass dependencies during validation.
This allows tools to import tau_bench classes without requiring the full tau_bench package.
"""

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

# Mock the entire tau_bench module structure
class MockTauBench:
    class envs:
        class tool:
            Tool = Tool
        class user:
            load_user = load_user
            UserStrategy = UserStrategy
    
    class types:
        Action = Action
        Task = Task

# Install mock in sys.modules to intercept imports
import sys
sys.modules['tau_bench'] = MockTauBench()
sys.modules['tau_bench.envs'] = MockTauBench.envs
sys.modules['tau_bench.envs.tool'] = MockTauBench.envs.tool
sys.modules['tau_bench.envs.user'] = MockTauBench.envs.user
sys.modules['tau_bench.types'] = MockTauBench.types