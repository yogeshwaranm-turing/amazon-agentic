import streamlit as st
import json
import ast
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Tuple
import os
import glob

class FunctionAnalyzer:
    def __init__(self):
        self.functions = {}
        self.function_signatures = {}
        self.json_files = {}
        self.python_files = {}
    
    def load_python_files_from_directory(self, directory_path: str) -> Tuple[Dict, Dict]:
        """Load all Python files from a directory"""
        python_files = {}
        functions_found = {}
        
        if not os.path.exists(directory_path):
            return {}, {}
        
        # Get all files except init files
        all_files = glob.glob(os.path.join(directory_path, "*"))
        py_files = [f for f in all_files if os.path.isfile(f) and 'init' not in os.path.basename(f).lower()]
        
        for file_path in py_files:
            file_name = os.path.basename(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    python_files[file_name] = content
                    
                    # First try to parse classes and function definitions
                    file_functions = self.parse_function_def(content)
                    
                    # If no classes or functions found, treat the file itself as a function
                    if not file_functions:
                        # Extract parameters from the file content
                        params = self._extract_params_from_content(content)
                        
                        func_info = {
                            'name': file_name,
                            'args': params,
                            'returns': None,
                            'docstring': f"Function from file: {file_name}",
                            'body': content[:200] + "..." if len(content) > 200 else content,
                            'type': 'file_function',
                            'outputs': ['result', 'data']
                        }
                        file_functions[file_name] = func_info
                    
                    # Add all functions to the main collection
                    for func_name, func_info in file_functions.items():
                        func_info['source_file'] = file_name
                        functions_found[func_name] = func_info
            except:
                # Even if file reading fails, create a basic function entry
                func_info = {
                    'name': file_name,
                    'args': ['data'],  # Default parameter
                    'returns': None,
                    'docstring': f"Function from file: {file_name}",
                    'body': "Could not read file content",
                    'source_file': file_name,
                    'type': 'file_function',
                    'outputs': ['result', 'data']
                }
                functions_found[file_name] = func_info
                
        return python_files, functions_found
    
    def _extract_params_from_content(self, content: str) -> List[str]:
        """Extract likely parameters from file content"""
        params = []
        
        # Look for common parameter patterns in the content
        import re
        
        # Look for variable assignments that might be parameters
        param_patterns = [
            r'(\w+_id)\s*=',
            r'(\w+_data)\s*=',
            r'(\w+_info)\s*=',
            r'input\s*=\s*(\w+)',
            r'data\s*=\s*(\w+)',
            r'(\w+)\s*=\s*request',
            r'(\w+)\s*=\s*input',
        ]
        
        for pattern in param_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            params.extend(matches)
        
        # If no specific parameters found, add generic ones
        if not params:
            params = ['data', 'input', 'params']
        
        # Remove duplicates and return
        return list(set(params[:5]))  # Limit to 5 parameters
    
    def load_json_files_from_directory(self, directory_path: str) -> Dict:
        """Load all JSON files from a directory"""
        json_files = {}
        
        if not os.path.exists(directory_path):
            return {}
        
        json_file_paths = glob.glob(os.path.join(directory_path, "*.json"))
        
        for file_path in json_file_paths:
            file_name = os.path.basename(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    json_files[file_name] = {
                        'data': content,
                        'structure': self._analyze_data_structure(content),
                        'raw_content': json.dumps(content, indent=2)
                    }
            except:
                continue
                
        return json_files
    
    def parse_function_def(self, code_string: str) -> Dict:
        """Parse Python classes and extract their invoke methods with proper inputs/outputs"""
        try:
            tree = ast.parse(code_string)
            functions = {}
            
            # Look for classes with invoke methods
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    
                    # Look for invoke method in this class
                    invoke_method = None
                    for class_item in node.body:
                        if (isinstance(class_item, ast.FunctionDef) and 
                            class_item.name == 'invoke'):
                            invoke_method = class_item
                            break
                    
                    if invoke_method:
                        # Extract actual parameters (excluding 'self')
                        params = [arg.arg for arg in invoke_method.args.args if arg.arg != 'self']
                        
                        # Extract outputs by analyzing the invoke method body
                        outputs = self._extract_outputs_from_invoke_method(invoke_method, class_name)
                        
                        func_info = {
                            'name': class_name,
                            'args': params,
                            'returns': self._get_return_annotation(invoke_method),
                            'docstring': ast.get_docstring(invoke_method) or ast.get_docstring(node),
                            'body': ast.unparse(invoke_method) if hasattr(ast, 'unparse') else str(invoke_method),
                            'type': 'class_invoke',
                            'class_name': class_name,
                            'outputs': outputs,
                            'raw_code': code_string[:500]  # Store raw code for debugging
                        }
                        functions[class_name] = func_info
                    else:
                        # Class without invoke method - create basic entry
                        func_info = {
                            'name': class_name,
                            'args': ['input_data'],  # Default parameter
                            'returns': None,
                            'docstring': ast.get_docstring(node) or f"Class: {class_name}",
                            'body': f"class {class_name}",
                            'type': 'class_no_invoke',
                            'class_name': class_name,
                            'outputs': ['result'],
                            'raw_code': code_string[:500]
                        }
                        functions[class_name] = func_info
                    
            return functions
        except Exception as e:
            # If parsing fails, try to extract class name from the code manually
            return self._fallback_class_extraction(code_string, str(e))
    
    def _extract_outputs_from_invoke_method(self, invoke_method, class_name: str) -> List[str]:
        """Extract outputs by analyzing the invoke method body more thoroughly"""
        outputs = []
        
        # Look for return statements
        for node in ast.walk(invoke_method):
            if isinstance(node, ast.Return) and node.value:
                outputs.extend(self._parse_return_value(node.value))
        
        # Look for variable assignments that might be outputs
        for node in ast.walk(invoke_method):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # Common output variable patterns
                        if any(pattern in var_name.lower() for pattern in 
                               ['result', 'output', 'response', 'data', 'info']):
                            outputs.append(var_name)
        
        # Extract from class name patterns
        name_outputs = self._extract_outputs_from_name(class_name)
        outputs.extend(name_outputs)
        
        # Remove duplicates and return
        return list(set(outputs)) if outputs else ['result']
    
    def _parse_return_value(self, return_node) -> List[str]:
        """Parse different types of return values"""
        outputs = []
        
        if isinstance(return_node, ast.Dict):
            # return {"key1": value1, "key2": value2}
            for key in return_node.keys:
                if isinstance(key, ast.Constant):
                    outputs.append(str(key.value))
                elif hasattr(key, 's'):  # Python < 3.8
                    outputs.append(key.s)
        
        elif isinstance(return_node, ast.Name):
            # return variable_name
            outputs.append(return_node.id)
        
        elif isinstance(return_node, ast.Tuple) or isinstance(return_node, ast.List):
            # return (a, b, c) or return [a, b, c]
            for elt in return_node.elts:
                if isinstance(elt, ast.Name):
                    outputs.append(elt.id)
                elif isinstance(elt, ast.Constant):
                    outputs.append(str(elt.value))
        
        elif isinstance(return_node, ast.Call):
            # return function_call()
            if isinstance(return_node.func, ast.Name):
                func_name = return_node.func.id
                outputs.append(f"{func_name}_result")
        
        return outputs
    
    def _fallback_class_extraction(self, code_string: str, error: str) -> Dict:
        """Fallback method to extract class info when AST parsing fails"""
        functions = {}
        
        # Use regex to find class definitions
        import re
        class_pattern = r'class\s+(\w+)(?:\([^)]*\))?:'
        matches = re.findall(class_pattern, code_string)
        
        for class_name in matches:
            func_info = {
                'name': class_name,
                'args': ['input_data'],
                'returns': None,
                'docstring': f"Class: {class_name} (fallback parsing)",
                'body': f"class {class_name}",
                'type': 'class_fallback',
                'class_name': class_name,
                'outputs': ['result'],
                'parse_error': error,
                'raw_code': code_string[:500]
            }
            functions[class_name] = func_info
        
        return functions
    
    def _extract_outputs_from_ast(self, func_node) -> List[str]:
        """Extract outputs by analyzing return statements in the AST"""
        outputs = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return) and node.value:
                # Handle different return patterns
                if isinstance(node.value, ast.Dict):
                    # return {"key1": value1, "key2": value2}
                    for key in node.value.keys:
                        if isinstance(key, ast.Constant):
                            outputs.append(str(key.value))
                        elif isinstance(key, ast.Str):  # Python < 3.8
                            outputs.append(key.s)
                
                elif isinstance(node.value, ast.Name):
                    # return variable_name
                    outputs.append(node.value.id)
                
                elif isinstance(node.value, ast.Call):
                    # return function_call() - try to infer from function name
                    if isinstance(node.value.func, ast.Name):
                        func_name = node.value.func.id.lower()
                        if 'get' in func_name:
                            outputs.append('data')
                        elif 'create' in func_name:
                            outputs.append('created_item')
                        elif 'update' in func_name:
                            outputs.append('updated_item')
                
                elif isinstance(node.value, ast.Constant):
                    # return "string" or return 123
                    if isinstance(node.value.value, str):
                        outputs.append(node.value.value)
        
        # Also extract from the function/class name
        func_name = func_node.name.lower()
        name_outputs = self._extract_outputs_from_name(func_name)
        outputs.extend(name_outputs)
        
        # Remove duplicates and return
        return list(set(outputs)) if outputs else ['result', 'data']
    
    def _extract_outputs_from_name(self, name: str) -> List[str]:
        """Extract likely outputs from function/class name"""
        outputs = []
        name_lower = name.lower()
        
        # Extract entities from function names
        common_entities = ['user', 'incident', 'task', 'comment', 'attachment', 'department', 
                          'category', 'company', 'article', 'change', 'request', 'overdue']
        
        for entity in common_entities:
            if entity in name_lower:
                outputs.append(entity)
                outputs.append(entity + '_data')
                outputs.append(entity + '_info')
        
        # Based on function action patterns
        if any(action in name_lower for action in ['get', 'fetch', 'retrieve']):
            outputs.extend(['data', 'result', 'info', 'details'])
        
        if any(action in name_lower for action in ['create', 'add', 'insert']):
            outputs.extend(['created_item', 'new_item', 'id'])
        
        if any(action in name_lower for action in ['filter', 'search', 'find']):
            outputs.extend(['filtered_data', 'results', 'list'])
        
        if any(action in name_lower for action in ['update', 'modify', 'edit']):
            outputs.extend(['updated_item', 'status'])
        
        return outputs
    
    def _get_return_annotation(self, node):
        """Extract return type annotation if present"""
        if node.returns:
            if hasattr(ast, 'unparse'):
                return ast.unparse(node.returns)
            else:
                return str(node.returns)
        return None
    
    def analyze_json_structure(self, json_data: str) -> Dict:
        """Analyze JSON data structure"""
        try:
            data = json.loads(json_data)
            return self._analyze_data_structure(data)
        except:
            return {}
    
    def _analyze_data_structure(self, data, path="root"):
        """Recursively analyze data structure"""
        structure = {"type": type(data).__name__, "path": path}
        
        if isinstance(data, dict):
            structure["keys"] = list(data.keys())
            structure["nested"] = {}
            for key, value in data.items():
                structure["nested"][key] = self._analyze_data_structure(value, f"{path}.{key}")
        elif isinstance(data, list) and data:
            structure["length"] = len(data)
            structure["item_type"] = type(data[0]).__name__
            if isinstance(data[0], (dict, list)):
                structure["item_structure"] = self._analyze_data_structure(data[0], f"{path}[0]")
        
        return structure
    
    def suggest_chains(self, functions: Dict, json_structure: Dict, initial_instruction: str, starting_variable: str = None) -> List[Dict]:
        """Suggest function chains by following input/output dependencies"""
        if not starting_variable:
            return []
        
        # Build dependency graph
        dependency_graph = self._build_dependency_graph(functions)
        
        # Find all chains starting from the variable
        all_chains = self._find_all_chains_from_variable(starting_variable, functions, dependency_graph, max_length=20)
        
        # Filter and rank chains
        good_chains = [chain for chain in all_chains if len(chain['chain']) >= 3]  # At least 3 functions
        good_chains.sort(key=lambda x: len(x['chain']), reverse=True)  # Longer chains first
        
        return good_chains[:5]  # Return top 5 chains
    
    def _build_dependency_graph(self, functions: Dict) -> Dict:
        """Build a graph showing which functions can feed into which other functions"""
        graph = {}
        
        # First, extract potential outputs from each function
        function_outputs = {}
        for func_name, func_info in functions.items():
            outputs = self._extract_potential_outputs(func_name, func_info)
            function_outputs[func_name] = outputs
        
        # Build the dependency graph
        for func_name in functions:
            graph[func_name] = []
            
            # Find which other functions can accept this function's outputs
            for output in function_outputs[func_name]:
                for other_func, other_info in functions.items():
                    if other_func != func_name:
                        if self._can_function_accept_input(other_info, output):
                            graph[func_name].append({
                                'function': other_func,
                                'via_output': output,
                                'matching_param': self._find_matching_param(other_info, output)
                            })
        
        return graph
    
    def _extract_potential_outputs(self, func_name: str, func_info: Dict) -> List[str]:
        """Extract what this function outputs - use parsed outputs if available"""
        # If we have parsed outputs from the AST, use those first
        if 'outputs' in func_info and func_info['outputs']:
            return func_info['outputs']
        
        # Fallback to name-based extraction
        return self._extract_outputs_from_name(func_name)
    
    def _can_function_accept_input(self, func_info: Dict, potential_input: str) -> bool:
        """Check if a function can accept a particular input based on parameter names"""
        input_lower = potential_input.lower()
        
        # Make sure input is not the same as any of the function's outputs
        outputs = func_info.get('outputs', [])
        for output in outputs:
            if input_lower == output.lower():
                return False  # Input can't be same as output
        
        # Only accept if there's a meaningful parameter match
        for param in func_info['args']:
            param_lower = param.lower()
            
            # Exact or partial name matching
            if input_lower == param_lower:  # Exact match
                return True
            if input_lower in param_lower and len(input_lower) > 2:  # Partial match (avoid short matches)
                return True
            if param_lower in input_lower and len(param_lower) > 2:
                return True
        
        return False
    
    def suggest_chains(self, functions: Dict, json_structure: Dict, initial_instruction: str, starting_variable: str = None) -> List[Dict]:
        """Build chains by following input->output->input flow"""
        if not starting_variable:
            return []
        
        chains = []
        
        # Find functions that can accept the starting variable
        starter_functions = self._find_functions_that_accept(starting_variable, functions)
        
        # Build multiple chains starting from different functions
        for starter_func in starter_functions[:5]:  # Try top 5 starters
            chain = self._build_single_chain(starting_variable, starter_func, functions, max_length=40)
            if len(chain['steps']) >= 3:  # Only keep chains with at least 3 steps
                chains.append(chain)
        
        return chains[:3]  # Return top 3 chains
    
    def _find_functions_that_accept(self, input_var: str, functions: Dict) -> List[str]:
        """Find functions that can actually accept the input variable"""
        matching_functions = []
        
        for func_name, func_info in functions.items():
            if self._can_function_accept_input(func_info, input_var):
                matching_functions.append(func_name)
        
        return matching_functions
    
    def _build_single_chain(self, starting_var: str, start_func: str, functions: Dict, max_length: int = 40) -> Dict:
        """Build a single chain following input->output->input flow"""
        steps = []
        current_var = starting_var
        used_functions = set()
        used_variables = {starting_var.lower()}  # Track used variables to avoid repetition
        
        # Start with the initial function
        current_func = start_func
        
        for i in range(max_length):
            if current_func in used_functions:
                break  # Avoid cycles
            
            if current_func not in functions:
                break  # Function not found
            
            used_functions.add(current_func)
            func_info = functions.get(current_func, {})
            
            # Get outputs from current function
            outputs = self._extract_potential_outputs(current_func, func_info)
            if not outputs:
                outputs = ['result']  # Default output
            
            # Pick the first meaningful output that hasn't been used
            chosen_output = self._pick_unused_output(outputs, used_variables, current_func)
            if not chosen_output:
                break  # No unused outputs available
            
            # Get all required inputs for this function
            required_inputs = func_info.get('args', [])
            other_inputs = [inp for inp in required_inputs if inp.lower() != current_var.lower()]
            
            # Add this step to the chain
            step = {
                'input': current_var,
                'function': current_func,
                'all_required_inputs': required_inputs,
                'other_inputs_needed': other_inputs,
                'outputs': outputs,
                'chosen_output': chosen_output
            }
            steps.append(step)
            
            # Mark this output as used
            used_variables.add(chosen_output.lower())
            
            # Find next function that can accept this output
            next_functions = self._find_functions_that_accept(chosen_output, functions)
            next_functions = [f for f in next_functions if f not in used_functions]  # Exclude used
            
            if not next_functions:
                # Try with alternative unused outputs if no function found
                for alt_output in outputs[1:]:
                    if alt_output.lower() not in used_variables:  # Only try unused outputs
                        alt_next_functions = self._find_functions_that_accept(alt_output, functions)
                        alt_next_functions = [f for f in alt_next_functions if f not in used_functions]
                        if alt_next_functions:
                            chosen_output = alt_output
                            steps[-1]['chosen_output'] = chosen_output  # Update the step
                            used_variables.add(chosen_output.lower())  # Mark as used
                            next_functions = alt_next_functions
                            break
                
                if not next_functions:
                    break  # No more functions can accept any unused output
            
            # Pick the next function (could be random, or based on some logic)
            current_func = next_functions[0]  # Take first available
            current_var = chosen_output  # This becomes the input for next function
        
        # Build description
        description_parts = [starting_var]
        for step in steps:
            description_parts.append(f"{step['function']}({step['chosen_output']})")
        
        return {
            'chain': [step['function'] for step in steps],
            'steps': steps,
            'description': ' → '.join(description_parts),
            'starting_variable': starting_var,
            'length': len(steps),
            'confidence': min(1.0, len(steps) / 20.0),
            'unique_variables': list(used_variables)
        }
    
    def _pick_unused_output(self, outputs: List[str], used_variables: set, func_name: str) -> str:
        """Pick the most meaningful output that hasn't been used yet"""
        if not outputs:
            return None
        
        # Filter out already used outputs
        unused_outputs = [o for o in outputs if o.lower() not in used_variables]
        if not unused_outputs:
            return None  # All outputs have been used
        
        # Prefer outputs that match the function name
        func_lower = func_name.lower()
        for output in unused_outputs:
            if any(word in output.lower() for word in func_lower.split('_')):
                return output
        
        # Prefer non-generic outputs
        non_generic = [o for o in unused_outputs if o.lower() not in ['result', 'data', 'output', 'response']]
        if non_generic:
            return non_generic[0]
        
        # Fall back to first unused output
        return unused_outputs[0]
    
    def _find_matching_param(self, func_info: Dict, potential_input: str) -> str:
        """Find which parameter would accept this input"""
        input_lower = potential_input.lower()
        
        for param in func_info['args']:
            param_lower = param.lower()
            
            # Direct name matching
            if input_lower in param_lower or param_lower in input_lower:
                return param
            
            # Generic parameter names
            if param_lower in ['data', 'input', 'params', 'request', 'payload', 'info', 'content']:
                return param
            
            # Specific entity matching
            if 'incident' in input_lower and 'incident' in param_lower:
                return param
            if 'user' in input_lower and 'user' in param_lower:
                return param
            if 'task' in input_lower and 'task' in param_lower:
                return param
            if 'comment' in input_lower and 'comment' in param_lower:
                return param
        
        # If no specific match, return first parameter
        return func_info['args'][0] if func_info['args'] else 'unknown'
    
    def _find_all_chains_from_variable(self, starting_variable: str, functions: Dict, dependency_graph: Dict, max_length: int = 20) -> List[Dict]:
        """Find all possible chains starting from a variable using DFS"""
        chains = []
        
        # Find functions that can accept the starting variable
        starting_functions = []
        for func_name, func_info in functions.items():
            if self._can_function_accept_input(func_info, starting_variable):
                starting_functions.append(func_name)
        
        # Build chains from each starting function using DFS
        for start_func in starting_functions:
            visited = set()
            current_chain = []
            self._dfs_build_chain(start_func, dependency_graph, visited, current_chain, chains, starting_variable, max_length)
        
        return chains
    
    def _dfs_build_chain(self, current_func: str, graph: Dict, visited: set, current_chain: List, all_chains: List, starting_var: str, max_length: int):
        """Use DFS to build chains recursively"""
        if len(current_chain) >= max_length:
            return
        
        visited.add(current_func)
        current_chain.append(current_func)
        
        # If we have at least 3 functions, save this as a valid chain
        if len(current_chain) >= 3:
            chain_info = {
                'chain': current_chain.copy(),
                'description': f"{starting_var} → {' → '.join(current_chain)}",
                'confidence': min(1.0, len(current_chain) / 10.0),
                'starting_variable': starting_var,
                'length': len(current_chain)
            }
            all_chains.append(chain_info)
        
        # Continue building the chain
        for next_option in graph.get(current_func, []):
            next_func = next_option['function']
            if next_func not in visited:  # Avoid cycles
                self._dfs_build_chain(next_func, graph, visited.copy(), current_chain.copy(), all_chains, starting_var, max_length)
        
        # Backtrack
        visited.remove(current_func)
        current_chain.pop()

def main():
    st.set_page_config(page_title="Function Chain Analyzer", layout="wide")
    
    st.title("🔗 Function Chain Analyzer")
    st.markdown("Analyze Python functions and JSON data to suggest optimal chaining patterns")
    
    analyzer = FunctionAnalyzer()
    
    # Initialize session state
    if 'functions' not in st.session_state:
        st.session_state.functions = {}
    if 'python_files' not in st.session_state:
        st.session_state.python_files = {}
    if 'json_files' not in st.session_state:
        st.session_state.json_files = {}
    if 'selected_json_structure' not in st.session_state:
        st.session_state.selected_json_structure = None
    
    with st.sidebar:
        st.header("🚀 Starting Variable")
        starting_variable = st.text_input(
            "What variable do you start with?",
            placeholder="e.g., user_id, incident_id, data",
            help="Enter the name of the variable/data you have available to start the chain"
        )
    
    tab1, tab2, tab3 = st.tabs(["🔧 Functions", "📊 JSON Data", "🔍 Analysis"])
    
    with tab1:
        st.header("Python Function Definitions")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            python_dir = st.text_input(
                "Python Files Directory Path:",
                value="",
                help="Enter the path to directory containing Python files"
            )
        
        with col2:
            load_python = st.button("📁 Load Python Files", type="primary")
        
        if load_python and python_dir:
            python_files, functions = analyzer.load_python_files_from_directory(python_dir)
            
            # Store in session state
            st.session_state.python_files = python_files
            st.session_state.functions = functions
            
            if python_files:
                st.success(f"✅ Loaded {len(python_files)} Python files with {len(functions)} functions!")
                
                st.subheader("🔧 Parsed Functions")
                for func_name, func_info in functions.items():
                    with st.expander(f"📋 {func_name} (from {func_info.get('source_file', 'unknown')})"):
                        st.write(f"**Type:** {func_info.get('type', 'unknown')}")
                        st.write(f"**Parameters:** {', '.join(func_info['args'])}")
                        if func_info.get('outputs'):
                            st.write(f"**Outputs:** {', '.join(func_info['outputs'])}")
                        if func_info['returns']:
                            st.write(f"**Returns:** {func_info['returns']}")
                        if func_info['docstring']:
                            st.write(f"**Description:** {func_info['docstring']}")
                            
                # Debug: Show first few files and their parsing results
                st.subheader("🔍 Debug: Function Inputs & Outputs")
                st.write("**First 5 functions with their actual inputs and outputs:**")
                
                func_count = 0
                for func_name, func_info in functions.items():
                    if func_count < 5:
                        with st.expander(f"🔧 {func_name}"):
                            st.write(f"**Type:** {func_info.get('type', 'unknown')}")
                            st.write(f"**Input Parameters:** {func_info.get('args', [])}")
                            st.write(f"**Output Variables:** {func_info.get('outputs', [])}")
                            if func_info.get('parse_error'):
                                st.write(f"**Parse Error:** {func_info.get('parse_error')}")
                            st.write(f"**Raw Code Preview:**")
                            st.code(func_info.get('raw_code', 'No code available')[:300])
                        func_count += 1
            else:
                st.error("❌ No Python files found or parsed.")
        
        # Show loaded functions from session state
        elif st.session_state.functions:
            st.info(f"📋 {len(st.session_state.functions)} functions loaded from previous session")
            
            st.subheader("🔧 Loaded Functions")
            for func_name, func_info in st.session_state.functions.items():
                with st.expander(f"📋 {func_name} (from {func_info.get('source_file', 'unknown')})"):
                    st.write(f"**Type:** {func_info.get('type', 'unknown')}")
                    st.write(f"**Parameters:** {', '.join(func_info['args'])}")
                    if func_info.get('outputs'):
                        st.write(f"**Outputs:** {', '.join(func_info['outputs'])}")
                    if func_info['returns']:
                        st.write(f"**Returns:** {func_info['returns']}")
                    if func_info['docstring']:
                        st.write(f"**Description:** {func_info['docstring']}")
    
    with tab2:
        st.header("JSON Data Structure")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            json_dir = st.text_input(
                "JSON Files Directory Path:",
                value="",
                help="Enter the path to directory containing JSON files"
            )
        
        with col2:
            load_json = st.button("📁 Load JSON Files", type="primary")
        
        if load_json and json_dir:
            json_files = analyzer.load_json_files_from_directory(json_dir)
            
            # Store in session state
            st.session_state.json_files = json_files
            
            if json_files:
                st.success(f"✅ Loaded {len(json_files)} JSON files!")
                
                selected_json_file = st.selectbox(
                    "Select a JSON file to analyze:",
                    list(json_files.keys()),
                    help="Choose which JSON file to use for chain analysis"
                )
                
                if selected_json_file:
                    selected_json_data = json_files[selected_json_file]
                    st.session_state.selected_json_structure = selected_json_data['structure']
                    
                    with st.expander(f"📄 {selected_json_file} - Preview"):
                        st.json(selected_json_data['data'])
            else:
                st.error("❌ No JSON files found.")
        
        # Show loaded JSON from session state
        elif st.session_state.json_files:
            st.info(f"📊 {len(st.session_state.json_files)} JSON files loaded from previous session")
            
            selected_json_file = st.selectbox(
                "Select a JSON file to analyze:",
                list(st.session_state.json_files.keys()),
                help="Choose which JSON file to use for chain analysis"
            )
            
            if selected_json_file:
                selected_json_data = st.session_state.json_files[selected_json_file]
                st.session_state.selected_json_structure = selected_json_data['structure']
                
                with st.expander(f"📄 {selected_json_file} - Preview"):
                    st.json(selected_json_data['data'])
    
    with tab3:
        st.header("Chain Analysis & Suggestions")
        
        # Show current status
        st.write(f"**Functions loaded:** {len(st.session_state.functions)}")
        st.write(f"**Starting variable:** {starting_variable if starting_variable else 'Not specified'}")
        
        if st.session_state.functions and starting_variable:
            # Debug information
            st.write("🔍 **Debug Info:**")
            st.write(f"- Starting variable: `{starting_variable}`")
            
            # Show which functions can actually accept the starting variable
            matching_functions = []
            for func_name, func_info in st.session_state.functions.items():
                if analyzer._can_function_accept_input(func_info, starting_variable):
                    matching_param = analyzer._find_matching_param(func_info, starting_variable)
                    matching_functions.append(f"{func_name}")
            
            st.write(f"- Functions that can accept `{starting_variable}`: {matching_functions[:10]}")  # Show first 10
            
            # Show what outputs the first function produces
            if matching_functions:
                first_func = matching_functions[0]
                first_func_info = st.session_state.functions[first_func]
                first_outputs = analyzer._extract_potential_outputs(first_func, first_func_info)
                st.write(f"- `{first_func}` outputs: {first_outputs}")
                
                # Check what can accept these outputs
                if first_outputs:
                    for output in first_outputs[:3]:
                        next_funcs = []
                        for fname, finfo in st.session_state.functions.items():
                            if fname != first_func and analyzer._can_function_accept_input(finfo, output):
                                next_funcs.append(fname)
                        st.write(f"- Functions that can accept `{output}`: {next_funcs[:5]}")
            
            chains = analyzer.suggest_chains(st.session_state.functions, st.session_state.selected_json_structure, "", starting_variable)
            
            st.write(f"- Generated chains: {len(chains)}")
            
            if chains:
                st.success(f"✅ Found {len(chains)} chain sequences with up to 40 steps!")
                
                for i, chain in enumerate(chains):
                    with st.expander(f"🔗 Chain Option {i+1} - Length: {chain.get('length', 0)} steps"):
                        
                        # Show the detailed step-by-step flow
                        st.subheader("📋 Detailed Chain Flow:")
                        
                        flow_text = f"**{chain['starting_variable']}**"
                        
                        for j, step in enumerate(chain['steps']):
                            flow_text += f"\n\n→ **{step['function']}**"
                            flow_text += f"\n   - Primary input: `{step['input']}`"
                            if step.get('other_inputs_needed'):
                                flow_text += f"\n   - Other inputs needed: {', '.join([f'`{inp}`' for inp in step['other_inputs_needed']])}"
                            flow_text += f"\n   - All outputs: {step['outputs']}"  
                            flow_text += f"\n   - Chosen output: `{step['chosen_output']}`"
                            
                            if j < len(chain['steps']) - 1:
                                flow_text += f"\n\n→ `{step['chosen_output']}`"
                        
                        st.markdown(flow_text)
                        
                        # Show unique variables used
                        if 'unique_variables' in chain:
                            st.write(f"**Unique variables in chain:** {', '.join([f'`{var}`' for var in chain['unique_variables']])}")
                        
                        # Show compact chain
                        st.subheader("🔗 Compact Chain:")
                        compact_chain = [chain['starting_variable']]
                        for step in chain['steps']:
                            if step.get('other_inputs_needed'):
                                func_display = f"{step['function']}(+{len(step['other_inputs_needed'])} more inputs)"
                            else:
                                func_display = step['function']
                            compact_chain.append(func_display)
                            compact_chain.append(step['chosen_output'])
                        
                        st.write(" → ".join(compact_chain))
                        
                        # Visual diagram - multi-line flow
                        if len(chain['steps']) > 0:
                            st.subheader("📊 Chain Visualization")
                            
                            # Create a multi-line flow diagram
                            display_steps = chain['steps'][:20]  # Show first 20 steps max
                            items_per_line = 8  # Number of items per line
                            
                            items = []
                            # Add starting variable
                            items.append({
                                'label': chain['starting_variable'],
                                'type': 'variable',
                                'color': '#90EE90'  # Light green
                            })
                            
                            # Add function and output pairs
                            for step in display_steps:
                                items.append({
                                    'label': step['function'],
                                    'type': 'function', 
                                    'color': '#87CEEB'  # Sky blue
                                })
                                items.append({
                                    'label': step['chosen_output'],
                                    'type': 'variable',
                                    'color': '#FFE4B5'  # Moccasin
                                })
                            
                            # Calculate number of lines needed
                            num_lines = (len(items) + items_per_line - 1) // items_per_line
                            
                            fig, ax = plt.subplots(figsize=(18, num_lines * 2.5))
                            
                            box_width = 2.0
                            box_height = 0.6
                            spacing_x = 0.3
                            spacing_y = 1.5
                            
                            for i, item in enumerate(items):
                                # Calculate position with alternating direction
                                line_num = i // items_per_line
                                pos_in_line = i % items_per_line
                                
                                # Alternate direction: even lines left-to-right, odd lines right-to-left
                                if line_num % 2 == 0:
                                    # Left to right (normal)
                                    x_pos = pos_in_line * (box_width + spacing_x)
                                else:
                                    # Right to left (reversed)
                                    x_pos = (items_per_line - 1 - pos_in_line) * (box_width + spacing_x)
                                
                                y_pos = -line_num * spacing_y
                                
                                # Create shape
                                if item['type'] == 'variable':
                                    # Oval for variables
                                    from matplotlib.patches import Ellipse
                                    ellipse = Ellipse((x_pos + box_width/2, y_pos), box_width, box_height,
                                                    facecolor=item['color'], edgecolor='black', linewidth=1.5)
                                    ax.add_patch(ellipse)
                                else:
                                    # Rectangle for functions
                                    from matplotlib.patches import FancyBboxPatch
                                    rect = FancyBboxPatch((x_pos, y_pos - box_height/2), box_width, box_height,
                                                        boxstyle="round,pad=0.1", 
                                                        facecolor=item['color'], edgecolor='black', linewidth=1.5)
                                    ax.add_patch(rect)
                                
                                # Add text
                                label = item['label']
                                if len(label) > 12:
                                    label = label[:10] + "..."
                                
                                ax.text(x_pos + box_width/2, y_pos, label,
                                       ha='center', va='center', fontsize=9, weight='bold')
                                
                                # Add arrow to next item
                                if i < len(items) - 1:
                                    next_line_num = (i + 1) // items_per_line
                                    next_pos_in_line = (i + 1) % items_per_line
                                    
                                    # Calculate next item position
                                    if next_line_num % 2 == 0:
                                        next_x_pos = next_pos_in_line * (box_width + spacing_x)
                                    else:
                                        next_x_pos = (items_per_line - 1 - next_pos_in_line) * (box_width + spacing_x)
                                    
                                    next_y_pos = -next_line_num * spacing_y
                                    
                                    if line_num == next_line_num:
                                        # Same line - horizontal arrow (direction depends on line)
                                        if line_num % 2 == 0:
                                            # Left to right
                                            arrow_start_x = x_pos + box_width + 0.05
                                            arrow_end_x = x_pos + box_width + spacing_x - 0.05
                                        else:
                                            # Right to left
                                            arrow_start_x = x_pos - 0.05
                                            arrow_end_x = x_pos - spacing_x + 0.05
                                        
                                        ax.annotate('', xy=(arrow_end_x, y_pos), xytext=(arrow_start_x, y_pos),
                                                  arrowprops=dict(arrowstyle='->', lw=2, color='#2E8B57'))
                                    else:
                                        # Next line - simple vertical arrow (no more long arcs!)
                                        if line_num % 2 == 0:
                                            # From rightmost position of current line
                                            arrow_start_x = x_pos + box_width/2
                                        else:
                                            # From leftmost position of current line
                                            arrow_start_x = x_pos + box_width/2
                                        
                                        arrow_start_y = y_pos - box_height/2
                                        arrow_end_x = next_x_pos + box_width/2
                                        arrow_end_y = next_y_pos + box_height/2
                                        
                                        ax.annotate('', xy=(arrow_end_x, arrow_end_y), xytext=(arrow_start_x, arrow_start_y),
                                                  arrowprops=dict(arrowstyle='->', lw=2, color='#2E8B57'))
                            
                            # Set plot properties
                            ax.set_xlim(-0.5, items_per_line * (box_width + spacing_x))
                            ax.set_ylim(-num_lines * spacing_y + 0.5, 1)
                            ax.set_aspect('equal')
                            ax.axis('off')
                            
                            # Add title
                            title = f"Chain {i+1}: {len(chain['steps'])} steps"
                            if len(display_steps) < len(chain['steps']):
                                title += f" (showing first {len(display_steps)})"
                            ax.set_title(title, fontsize=14, weight='bold', pad=20)
                            
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close()
            else:
                st.warning(f"⚠️ No chains found starting with '{starting_variable}'. Try a different starting variable.")
        else:
            missing = []
            if not st.session_state.functions:
                missing.append("functions")
            if not starting_variable:
                missing.append("starting variable")
                
            st.info(f"📝 Please provide: {', '.join(missing)}")

if __name__ == "__main__":
    main()