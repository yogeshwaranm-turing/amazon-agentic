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

class Env:
    """Mock Env class that replaces tau_bench.envs.base.Env"""
    pass

class UserStrategy:
    """Mock UserStrategy class"""
    LLM = "mock_llm"  # Add the LLM attribute that's being accessed
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

# Create environment-specific mock modules
tau_bench_envs_fund_finance = create_mock_module('tau_bench.envs.fund_finance')
tau_bench_envs_fund_finance_data = create_mock_module('tau_bench.envs.fund_finance.data')
tau_bench_envs_fund_finance_rules = create_mock_module('tau_bench.envs.fund_finance.rules')
tau_bench_envs_fund_finance_tools = create_mock_module('tau_bench.envs.fund_finance.tools')
tau_bench_envs_fund_finance_wiki = create_mock_module('tau_bench.envs.fund_finance.wiki')
tau_bench_envs_fund_finance_tasks = create_mock_module('tau_bench.envs.fund_finance.tasks')
tau_bench_envs_fund_finance_interface_1 = create_mock_module('tau_bench.envs.fund_finance.interface_1_tasks')
tau_bench_envs_fund_finance_interface_2 = create_mock_module('tau_bench.envs.fund_finance.interface_2_tasks')
tau_bench_envs_fund_finance_interface_3 = create_mock_module('tau_bench.envs.fund_finance.interface_3_tasks')
tau_bench_envs_fund_finance_interface_4 = create_mock_module('tau_bench.envs.fund_finance.interface_4_tasks')
tau_bench_envs_fund_finance_interface_5 = create_mock_module('tau_bench.envs.fund_finance.interface_5_tasks')

# Create hr_experts mock modules
tau_bench_envs_hr_experts = create_mock_module('tau_bench.envs.hr_experts')
tau_bench_envs_hr_experts_data = create_mock_module('tau_bench.envs.hr_experts.data')
tau_bench_envs_hr_experts_rules = create_mock_module('tau_bench.envs.hr_experts.rules')
tau_bench_envs_hr_experts_tools = create_mock_module('tau_bench.envs.hr_experts.tools')
tau_bench_envs_hr_experts_wiki = create_mock_module('tau_bench.envs.hr_experts.wiki')
tau_bench_envs_hr_experts_tasks = create_mock_module('tau_bench.envs.hr_experts.tasks')
tau_bench_envs_hr_experts_tasks_test = create_mock_module('tau_bench.envs.hr_experts.tasks_test')
tau_bench_envs_hr_experts_interface_1 = create_mock_module('tau_bench.envs.hr_experts.interface_1_tasks')
tau_bench_envs_hr_experts_interface_2 = create_mock_module('tau_bench.envs.hr_experts.interface_2_tasks')
tau_bench_envs_hr_experts_interface_3 = create_mock_module('tau_bench.envs.hr_experts.interface_3_tasks')
tau_bench_envs_hr_experts_interface_4 = create_mock_module('tau_bench.envs.hr_experts.interface_4_tasks')
tau_bench_envs_hr_experts_interface_5 = create_mock_module('tau_bench.envs.hr_experts.interface_5_tasks')

# Set up the module attributes
tau_bench.envs = tau_bench_envs
tau_bench_envs.base = tau_bench_envs_base
tau_bench_envs.tool = tau_bench_envs_tool
tau_bench_envs.user = tau_bench_envs_user
tau_bench_envs.fund_finance = tau_bench_envs_fund_finance
tau_bench_envs.hr_experts = tau_bench_envs_hr_experts
tau_bench.types = tau_bench_types

# Add classes to appropriate modules
tau_bench_envs_tool.Tool = Tool
tau_bench_envs_user.load_user = load_user
tau_bench_envs_user.UserStrategy = UserStrategy
tau_bench_types.Action = Action
tau_bench_types.Task = Task

# Add base classes that might be imported
tau_bench_envs_base.Tool = Tool
tau_bench_envs_base.Env = Env
tau_bench_envs_base.load_user = load_user
tau_bench_envs_base.UserStrategy = UserStrategy

# Add mock functions and data for fund_finance environment
tau_bench_envs_fund_finance_data.load_data = lambda: {}
tau_bench_envs_fund_finance_rules.RULES = {}
tau_bench_envs_fund_finance_wiki.WIKI = {}
tau_bench_envs_fund_finance_tasks.tasks = []

# Add mock test interfaces for fund_finance
tau_bench_envs_fund_finance_interface_1.INTERFACE_1_TEST = []
tau_bench_envs_fund_finance_interface_2.INTERFACE_2_TEST = []
tau_bench_envs_fund_finance_interface_3.INTERFACE_3_TEST = []
tau_bench_envs_fund_finance_interface_4.INTERFACE_4_TEST = []
tau_bench_envs_fund_finance_interface_5.INTERFACE_5_TEST = []

# Add mock functions and data for hr_experts environment
tau_bench_envs_hr_experts_data.load_data = lambda: {}
tau_bench_envs_hr_experts_rules.RULES = {}
tau_bench_envs_hr_experts_wiki.WIKI = {}
tau_bench_envs_hr_experts_tasks.tasks = []
tau_bench_envs_hr_experts_tasks_test.TASKS_TEST = []

# Add mock test interfaces for hr_experts
tau_bench_envs_hr_experts_interface_1.INTERFACE_1_TEST = []
tau_bench_envs_hr_experts_interface_2.INTERFACE_2_TEST = []
tau_bench_envs_hr_experts_interface_3.INTERFACE_3_TEST = []
tau_bench_envs_hr_experts_interface_4.INTERFACE_4_TEST = []
tau_bench_envs_hr_experts_interface_5.INTERFACE_5_TEST = []

# Add mock tool functions for fund_finance
def mock_search_user_entities(**kwargs):
    return {"success": False, "error": "Mock function - not implemented"}

tau_bench_envs_fund_finance_tools.search_user_entities = mock_search_user_entities
tau_bench_envs_fund_finance_tools.ALL_TOOLS_INTERFACE_1 = []
tau_bench_envs_fund_finance_tools.ALL_TOOLS_INTERFACE_2 = []
tau_bench_envs_fund_finance_tools.ALL_TOOLS_INTERFACE_3 = []
tau_bench_envs_fund_finance_tools.ALL_TOOLS_INTERFACE_4 = []
tau_bench_envs_fund_finance_tools.ALL_TOOLS_INTERFACE_5 = []

# Add the missing class that the environment is looking for
class MockFundFinanceDomainEnv(Env):
    """Mock fund finance domain environment class"""
    def __init__(self, *args, **kwargs):
        pass

# Make it available in the fund_finance module
tau_bench_envs_fund_finance.MockFundFinanceDomainEnv = MockFundFinanceDomainEnv

# HR Experts Mock Environment
class MockHRExpertsDomainEnv(Env):
    """Mock HR Experts Domain Environment"""
    def __init__(self, user_strategy="LLM", user_model="gpt-4o", 
                 user_provider=None, task_split="test", task_index=None, interface_num=None):
        self.user_strategy = user_strategy
        self.user_model = user_model
        self.interface_num = interface_num

# Make HR environment available
tau_bench_envs_hr_experts.MockHRExpertsDomainEnv = MockHRExpertsDomainEnv

tau_bench_envs_hr_experts_tools.ALL_TOOLS_INTERFACE_1 = []
tau_bench_envs_hr_experts_tools.ALL_TOOLS_INTERFACE_2 = []
tau_bench_envs_hr_experts_tools.ALL_TOOLS_INTERFACE_3 = []
tau_bench_envs_hr_experts_tools.ALL_TOOLS_INTERFACE_4 = []
tau_bench_envs_hr_experts_tools.ALL_TOOLS_INTERFACE_5 = []

print("Mock tau_bench modules installed successfully")