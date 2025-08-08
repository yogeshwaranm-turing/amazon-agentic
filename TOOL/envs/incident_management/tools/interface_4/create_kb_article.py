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
                            'type': 'file_function'
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
                    'is_file_function': True
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
        """Parse Python function definitions and class invoke methods from string"""
        try:
            tree = ast.parse(code_string)
            functions = {}
            
            # Look for regular function definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args],
                        'returns': self._get_return_annotation(node),
                        'docstring': ast.get_docstring(node),
                        'body': ast.unparse(node) if hasattr(ast, 'unparse') else str(node),
                        'type': 'function',
                        'outputs': self._extract_outputs_from_ast(node)
                    }
                    functions[node.name] = func_info
            
            # Look for classes with invoke methods
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    
                    # Look for invoke method in this class
                    for class_item in node.body:
                        if (isinstance(class_item, ast.FunctionDef) and 
                            class_item.name == 'invoke'):
                            
                            # Use class name as function name
                            func_info = {
                                'name': class_name,
                                'args': [arg.arg for arg in class_item.args.args if arg.arg != 'self'],  # Exclude 'self'
                                'returns': self._get_return_annotation(class_item),
                                'docstring': ast.get_docstring(class_item) or ast.get_docstring(node),
                                'body': ast.unparse(class_item) if hasattr(ast, 'unparse') else str(class_item),
                                'type': 'class_invoke',
                                'class_name': class_name,
                                'outputs': self._extract_outputs_from_ast(class_item)
                            }
                            functions[class_name] = func_info
                            break
                    
                    # If class doesn't have invoke method, still create an entry
                    if class_name not in functions:
                        func_info = {
                            'name': class_name,
                            'args': ['data'],  # Default parameter
                            'returns': None,
                            'docstring': ast.get_docstring(node) or f"Class: {class_name}",
                            'body': f"class {class_name}",
                            'type': 'class',
                            'class_name': class_name,
                            'outputs': ['result', 'data']  # Default outputs
                        }
                        functions[class_name] = func_info
                    
            return functions
        except:
            return {}
    
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
        """Extract what this function likely outputs based on its name and context"""
        outputs = []
        name_lower = func_name.lower()
        
        # Extract from function name patterns
        if name_lower.startswith('get_'):
            outputs.append(name_lower[4:])  # get_user -> user
        elif name_lower.startswith('fetch_'):
            outputs.append(name_lower[6:])  # fetch_incident -> incident
        elif name_lower.startswith('create_'):
            outputs.append(name_lower[7:])  # create_task -> task
        elif name_lower.startswith('filter_'):
            outputs.append(name_lower[7:] + 's')  # filter_user -> users (plural)
        elif name_lower.startswith('add_'):
            outputs.append(name_lower[4:])  # add_comment -> comment
        
        # Generic outputs based on function patterns
        if 'get' in name_lower or 'fetch' in name_lower:
            outputs.extend(['data', 'result', 'response'])
        if 'create' in name_lower or 'add' in name_lower:
            outputs.extend(['created_item', 'new_item', 'result'])
        if 'filter' in name_lower or 'search' in name_lower:
            outputs.extend(['filtered_data', 'results', 'list'])
        if 'process' in name_lower:
            outputs.extend(['processed_data', 'result'])
        
        # Always include generic outputs
        outputs.extend(['output', 'return_value', 'data'])
        
        return list(set(outputs))  # Remove duplicates
    
    def _can_function_accept_input(self, func_info: Dict, potential_input: str) -> bool:
        """Check if a function can accept a particular input - MUCH more flexible"""
        input_lower = potential_input.lower()
        
        # If the function has ANY parameters, it can potentially accept the input
        # This is realistic - most functions can accept data in some form
        if func_info['args']:
            return True
        
        return False
    
    def _extract_potential_outputs(self, func_name: str, func_info: Dict) -> List[str]:
        """Extract what this function outputs - use parsed outputs if available"""
        # If we have parsed outputs from the AST, use those first
        if 'outputs' in func_info and func_info['outputs']:
            return func_info['outputs']
        
        # Fallback to name-based extraction
        return self._extract_outputs_from_name(func_name)'user' in input_lower and 'user' in param_lower:
                return True
            if 'incident' in input_lower and 'incident' in param_lower:
                return True
            if 'task' in input_lower and 'task' in param_lower:
                return True
            if 'comment' in input_lower and 'comment' in param_lower:
                return True
        
        return False
    
    def _find_matching_param(self, func_info: Dict, potential_input: str) -> str:
        """Find which parameter would accept this input"""
        for param in func_info['args']:
            param_lower = param.lower()
            input_lower = potential_input.lower()
            
            if (input_lower in param_lower or param_lower in input_lower or 
                param_lower in ['data', 'input', 'params', 'request', 'payload', 'info']):
                return param
        
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
    
    def _parameter_matches_json(self, param: str, json_structure: Dict, threshold=0.7) -> bool:
        """Check if parameter name matches JSON keys"""
        if json_structure.get("type") == "dict" and "keys" in json_structure:
            for key in json_structure["keys"]:
                if param.lower() in key.lower() or key.lower() in param.lower():
                    return True
                if "nested" in json_structure:
                    if self._parameter_matches_json(param, json_structure["nested"].get(key, {})):
                        return True
        return False
    
    def _generate_chain_sequences(self, functions: Dict, scored_functions: List[Dict]) -> List[Dict]:
        """Generate possible chaining sequences"""
        sequences = []
        
        starters = [f for f in scored_functions if f['can_start_chain']]
        
        for starter in starters[:3]:
            sequence = {
                'chain': [starter['function']],
                'description': f"Start with {starter['function']}",
                'confidence': starter['score'] / len(starter['parameters']) if starter['parameters'] else 0
            }
            
            current_func = functions[starter['function']]
            next_functions = self._find_next_functions(current_func, functions, starter['function'])
            
            if next_functions:
                sequence['chain'].extend(next_functions[:2])
                sequence['description'] += f" → {' → '.join(next_functions[:2])}"
            
            sequences.append(sequence)
        
        return sequences
    
    def _find_next_functions(self, current_func: Dict, all_functions: Dict, exclude: str) -> List[str]:
        """Find functions that could follow the current function"""
        next_funcs = []
        
        for func_name, func_info in all_functions.items():
            if func_name == exclude:
                continue
                
            common_params = ['data', 'result', 'output', 'value', 'response']
            
            for param in func_info['args']:
                if any(common in param.lower() for common in common_params):
                    next_funcs.append(func_name)
                    break
        
        return next_funcs

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
        st.header("📝 Inputs")
        initial_instruction = st.text_area(
            "Initial Instruction/Goal:",
            placeholder="e.g., Process user data and generate report",
            height=100
        )
        
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
        
        functions = {}
        python_files = {}
        
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
                        st.write(f"**Parameters:** {', '.join(func_info['args'])}")
                        if func_info['returns']:
                            st.write(f"**Returns:** {func_info['returns']}")
                        if func_info['docstring']:
                            st.write(f"**Description:** {func_info['docstring']}")
            else:
                st.error("❌ No Python files found or parsed.")
        
        # Show loaded functions from session state
        elif st.session_state.functions:
            st.info(f"📋 {len(st.session_state.functions)} functions loaded from previous session")
            
            st.subheader("🔧 Loaded Functions")
            for func_name, func_info in st.session_state.functions.items():
                with st.expander(f"📋 {func_name} (from {func_info.get('source_file', 'unknown')})"):
                    st.write(f"**Parameters:** {', '.join(func_info['args'])}")
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
        
        json_files = {}
        selected_json_structure = None
        
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
        st.write(f"**JSON structure available:** {'Yes' if st.session_state.selected_json_structure else 'No'}")
        st.write(f"**Initial instruction:** {'Yes' if initial_instruction.strip() else 'No'}")
        st.write(f"**Starting variable:** {starting_variable if starting_variable else 'Not specified'}")
        
        if st.session_state.functions and starting_variable and initial_instruction.strip():
            # Debug information
            st.write("🔍 **Debug Info:**")
            st.write(f"- Starting variable: `{starting_variable}`")
            st.write(f"- Available functions: {list(st.session_state.functions.keys())}")
            
            # Check which functions can accept the starting variable
            matching_functions = []
            for func_name, func_info in st.session_state.functions.items():
                for param in func_info['args']:
                    param_lower = param.lower()
                    var_lower = starting_variable.lower()
                    if (var_lower in param_lower or param_lower in var_lower or 
                        param_lower in ['data', 'input', 'params', 'request', 'payload']):
                        matching_functions.append(f"{func_name}({param})")
                        break
            
            st.write(f"- Functions that can accept `{starting_variable}`: {matching_functions}")
            
            chains = analyzer.suggest_chains(st.session_state.functions, st.session_state.selected_json_structure, initial_instruction, starting_variable)
            
            st.write(f"- Generated chains: {len(chains)}")
            
            if chains:
                st.success(f"✅ Found {len(chains)} possible chain sequences starting with '{starting_variable}'!")
                
                for i, chain in enumerate(chains):
                    with st.expander(f"🔗 Chain Option {i+1} - Length: {chain.get('length', 0)} (Confidence: {chain.get('confidence', 0):.2f})"):
                        st.write(f"**Sequence:** {' → '.join(chain['chain'])}")
                        st.write(f"**Description:** {chain['description']}")
                        
                        if len(chain['chain']) > 1:
                            fig, ax = plt.subplots(figsize=(max(12, len(chain['chain']) * 2), 3))
                            
                            # Add starting variable box
                            positions = [(-1, 0)] + [(i*2, 0) for i in range(len(chain['chain']))]
                            labels = [chain['starting_variable']] + chain['chain']
                            colors = ['lightgreen'] + ['lightblue'] * len(chain['chain'])
                            
                            for j, (pos, label, color) in enumerate(zip(positions, labels, colors)):
                                rect = plt.Rectangle((pos[0]-0.4, pos[1]-0.2), 0.8, 0.4, 
                                                   fill=True, facecolor=color, 
                                                   edgecolor='blue' if color == 'lightblue' else 'green')
                                ax.add_patch(rect)
                                # Truncate long function names for display
                                display_label = label[:15] + "..." if len(label) > 15 else label
                                ax.text(pos[0], pos[1], display_label, ha='center', va='center', 
                                       fontsize=8, weight='bold')
                                
                                if j < len(positions) - 1:
                                    ax.arrow(pos[0]+0.4, pos[1], 1.2, 0, 
                                           head_width=0.1, head_length=0.1, 
                                           fc='green', ec='green')
                            
                            ax.set_xlim(-1.5, len(chain['chain'])*2)
                            ax.set_ylim(-0.5, 0.5)
                            ax.set_aspect('equal')
                            ax.axis('off')
                            ax.set_title(f"Chain {i+1}: {len(chain['chain'])} functions")
                            
                            st.pyplot(fig)
                            plt.close()
            else:
                st.warning(f"⚠️ No suitable chains found starting with '{starting_variable}'. Check the debug info above.")
        else:
            missing = []
            if not st.session_state.functions:
                missing.append("functions")
            if not starting_variable:
                missing.append("starting variable")
            if not initial_instruction.strip():
                missing.append("initial instruction")
                
            st.info(f"📝 Please provide: {', '.join(missing)}")

if __name__ == "__main__":
    main()