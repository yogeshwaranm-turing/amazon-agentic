#!/usr/bin/env python3
"""
Generate HTML validation report from JSON results.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any

def generate_html_report(report_data: Dict[str, Any]) -> str:
    """Generate an HTML report from validation results"""
    
    summary = report_data.get("summary", {})
    results = report_data.get("results", [])
    timestamp = report_data.get("timestamp", datetime.now().isoformat())
    
    # Calculate additional stats
    total_actions = sum(r.get("actions_validated", 0) for r in results)
    failed_actions = sum(
        len([ar for ar in r.get("action_results", []) if not ar.get("success", False)])
        for r in results
    )
    passed_actions = total_actions - failed_actions
    
    avg_exec_time = sum(r.get("execution_time_ms", 0) for r in results) / len(results) if results else 0
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Validation Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .info {{ color: #17a2b8; }}
        
        .results {{
            padding: 30px;
        }}
        .task-result {{
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .task-header {{
            padding: 15px 20px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .task-success {{
            background: #d4edda;
            border-left: 4px solid #28a745;
        }}
        .task-failure {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }}
        .task-details {{
            padding: 20px;
            background: white;
        }}
        .action-list {{
            margin: 15px 0;
        }}
        .action-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            background: #f8f9fa;
        }}
        .action-item.success {{ border-left: 3px solid #28a745; }}
        .action-item.failure {{ border-left: 3px solid #dc3545; }}
        
        .error-details {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 4px;
            padding: 15px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 0.9em;
        }}
        .exec-time {{
            font-size: 0.8em;
            color: #666;
        }}
        
        .badge {{
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge.success {{
            background: #d4edda;
            color: #155724;
        }}
        .badge.failure {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }}
        
        @media (max-width: 768px) {{
            .summary {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .container {{
                margin: 10px;
                border-radius: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Task Validation Report</h1>
            <p>Generated on {datetime.fromisoformat(timestamp).strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-number pass">{summary.get('passed', 0)}</div>
                <div class="stat-label">Tasks Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number fail">{summary.get('failed', 0)}</div>
                <div class="stat-label">Tasks Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number info">{summary.get('total', 0)}</div>
                <div class="stat-label">Total Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number warning">{passed_actions}</div>
                <div class="stat-label">Actions Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number info">{summary.get('success_rate', 0):.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number info">{avg_exec_time:.0f}ms</div>
                <div class="stat-label">Avg Exec Time</div>
            </div>
        </div>
        
        <div class="results">
            <h2>📊 Detailed Results</h2>
            
            <div class="progress-bar">
                <div class="progress-fill" style="width: {summary.get('success_rate', 0)}%"></div>
            </div>
            <p style="text-align: center; color: #666; margin-bottom: 30px;">
                Overall Success Rate: {summary.get('success_rate', 0):.1f}%
            </p>
"""
    
    # Add individual task results
    for result in results:
        task_file = result.get("task_file", "Unknown")
        environment = result.get("environment", "Unknown")
        success = result.get("success", False)
        actions_validated = result.get("actions_validated", 0)
        execution_time = result.get("execution_time_ms", 0)
        error = result.get("error", "")
        action_results = result.get("action_results", [])
        
        status_class = "task-success" if success else "task-failure"
        status_icon = "✅" if success else "❌"
        badge_class = "success" if success else "failure"
        badge_text = "PASS" if success else "FAIL"
        
        html += f"""
            <div class="task-result">
                <div class="task-header {status_class}">
                    <div>
                        {status_icon} <strong>{os.path.basename(task_file)}</strong>
                        <span style="font-weight: normal; margin-left: 10px;">({environment})</span>
                    </div>
                    <div>
                        <span class="badge {badge_class}">{badge_text}</span>
                    </div>
                </div>
                <div class="task-details">
                    <p><strong>File:</strong> {task_file}</p>
                    <p><strong>Environment:</strong> {environment}</p>
                    <p><strong>Actions Validated:</strong> {actions_validated}</p>
                    <p><strong>Execution Time:</strong> {execution_time:.2f}ms</p>
        """
        
        if error:
            html += f"""
                    <div class="error-details">
                        <strong>❌ Error:</strong><br>
                        {error}
                    </div>
            """
        
        if action_results:
            html += """
                    <div class="action-list">
                        <h4>Action Results:</h4>
            """
            
            for action in action_results:
                action_name = action.get("action_name", "Unknown")
                action_success = action.get("success", False)
                action_error = action.get("error", "")
                action_time = action.get("execution_time_ms", 0)
                data_type_matches = action.get("data_type_matches", True)
                
                action_class = "success" if action_success else "failure"
                action_icon = "✅" if action_success else "❌"
                type_warning = "" if data_type_matches else " ⚠️ Type mismatch"
                
                html += f"""
                        <div class="action-item {action_class}">
                            <div>
                                {action_icon} <strong>{action_name}</strong>
                                {type_warning}
                                {f"<br><small style='color: #dc3545;'>{action_error}</small>" if action_error else ""}
                            </div>
                            <div class="exec-time">{action_time:.1f}ms</div>
                        </div>
                """
            
            html += """
                    </div>
            """
        
        html += """
                </div>
            </div>
        """
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate HTML validation report")
    parser.add_argument("--input", required=True, help="Input JSON report file")
    parser.add_argument("--output", required=True, help="Output HTML file")
    
    args = parser.parse_args()
    
    try:
        # Load JSON report
        with open(args.input, 'r') as f:
            report_data = json.load(f)
        
        # Generate HTML
        html_content = generate_html_report(report_data)
        
        # Save HTML report
        with open(args.output, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {args.output}")
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())