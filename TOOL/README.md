# 🔗 Function Chain Analyzer

Analyze Python functions and JSON data to suggest optimal chaining patterns with an intuitive Streamlit interface.

## ✨ Features

- **Smart Function Parsing**: Automatically extracts inputs and outputs from Python classes with `invoke` methods
- **Chain Generation**: Builds intelligent function chains following input→output→input flow
- **No Variable Repetition**: Ensures each variable in the chain is unique
- **Multi-line Visualization**: Beautiful alternating flow diagrams (boustrophedon pattern)
- **Additional Input Detection**: Shows what other inputs each function requires
- **Session State**: Maintains data across tab switches
- **Debug Information**: Detailed parsing and chain building insights

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/function-chain-analyzer.git
   cd function-chain-analyzer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run function_chain_analyzer.py
   ```

## 📖 Usage

### 1. Load Python Functions
- Enter the path to your directory containing Python files
- The analyzer will parse classes with `invoke` methods
- Each file is treated as a function (exclude `*init*` files)

### 2. Load JSON Data (Optional)
- Enter the path to your JSON data directory
- Select a JSON file to analyze its structure

### 3. Generate Chains
- Enter a starting variable (e.g., `incident_id`, `user_data`)
- View generated chains with up to 40 steps
- See detailed flow with required inputs and outputs

## 🏗️ How It Works

### Function Parsing
- Parses Python classes with `invoke` methods using AST
- Extracts parameters from method signatures
- Analyzes return statements to determine outputs
- Handles various return patterns (dictionaries, variables, function calls)

### Chain Building
- Finds functions that can accept the starting variable
- Follows input→output→input flow
- Prevents variable repetition and function cycles
- Shows additional inputs required for each function
- Generates multiple chain options ranked by length

### Visualization
- Multi-line flow with alternating directions
- Ovals for variables, rounded rectangles for functions
- Color-coded elements (green=start, blue=functions, yellow=outputs)
- Clean arrows following natural reading patterns

## 📁 Project Structure

```
function-chain-analyzer/
├── function_chain_analyzer.py  # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
└── .gitignore               # Git ignore patterns
```

## 🔧 Example Function Format

The analyzer expects Python classes with `invoke` methods:

```python
class GetUserDetails:
    def invoke(self, user_id, additional_params):
        # Function implementation
        user_data = fetch_user(user_id)
        return {
            "user": user_data,
            "status": "success"
        }
```

## 🎯 Chain Example

Starting with `name`:
```
name → CreateSubcategory(+2 more inputs) → category → CreateIncident(+11 more inputs) → incident_data → CreateCategory(+2 more inputs) → category_data → AddIncidentComment(+5 more inputs) → comment_data → CreateIncidentTask(+7 more inputs) → task → LogIncidentChange(+5 more inputs) → change_data → CreateSLAPolicy(+6 more inputs) → new_item
```

### 📝 Chain Flow in Plain English:

1. **Starting Point**: A `name` is provided as the initial input
2. **Create Subcategory**: The system uses the name (plus 2 additional inputs) to create a subcategory, resulting in a `category`
3. **Create Incident**: Using the category (plus 11 more inputs), an incident is created, producing `incident_data`
4. **Create Category**: The incident data (plus 2 more inputs) is used to create a broader category, generating `category_data`
5. **Add Comment**: A comment is added to the incident using category data (plus 5 more inputs), creating `comment_data`
6. **Create Task**: The comment data (plus 7 more inputs) triggers task creation, resulting in a `task`
7. **Log Change**: The task (plus 5 more inputs) is logged as a change, producing `change_data`
8. **Create SLA Policy**: Finally, the change data (plus 6 more inputs) is used to create a new SLA policy, resulting in a `new_item`

**Summary**: The name initiates a workflow that creates organizational structures (subcategory, category), generates incident records with associated comments and tasks, logs changes, and ultimately establishes new SLA policies - demonstrating how a simple input can cascade through multiple business processes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Uses [Matplotlib](https://matplotlib.org/) for chain visualizations
- AST parsing for intelligent Python code analysis
