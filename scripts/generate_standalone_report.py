#!/usr/bin/env python3
"""
Generate a standalone HTML validation report that can be viewed without any dependencies.
"""

import argparse
import json
from datetime import datetime

def generate_standalone_html_report(report_data: dict, run_number: str) -> str:
    """Generate a standalone HTML report with embedded JSON data"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Task Validation Report - Run {run_number}</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .download-btn {{ background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; text-decoration: none; display: inline-block; }}
        .download-btn:hover {{ background: #005a87; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .summary-item {{ text-align: center; }}
        .summary-value {{ font-size: 2em; font-weight: bold; }}
        .failed {{ color: #d73a49; }}
        .passed {{ color: #28a745; }}
        .warning {{ color: #f66a0a; }}
        .task-detail {{ margin: 20px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #ddd; }}
        .task-failed {{ border-left-color: #d73a49; background: #ffeef0; }}
        .task-passed {{ border-left-color: #28a745; background: #f0fff4; }}
        .action-detail {{ margin: 15px 0; padding: 10px; background: #f8f9fa; border-radius: 3px; }}
        .comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 10px 0; }}
        .expected, .actual {{ padding: 10px; border-radius: 5px; }}
        .expected {{ background: #f0fff4; border-left: 3px solid #28a745; }}
        .actual {{ background: #ffeef0; border-left: 3px solid #d73a49; }}
        pre {{ background: #f6f8fa; padding: 10px; border-radius: 3px; overflow-x: auto; font-size: 0.9em; }}
        .collapsible {{ cursor: pointer; user-select: none; }}
        .collapsible:hover {{ background: #e9ecef; }}
        .content {{ display: none; }}
        .content.show {{ display: block; }}
        .badge {{ padding: 2px 8px; border-radius: 12px; font-size: 0.8em; font-weight: bold; }}
        .badge-success {{ background: #d4edda; color: #155724; }}
        .badge-danger {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Task Validation Report</h1>
            <p><strong>Run:</strong> {run_number} | <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <button class="download-btn" onclick="downloadJson()">📁 Download JSON Report</button>
            <button class="download-btn" onclick="toggleAll()">🔽 Expand All</button>
        </div>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-value">{report_data['summary']['total']}</div>
                <div>Total Tasks</div>
            </div>
            <div class="summary-item">
                <div class="summary-value passed">{report_data['summary']['passed']}</div>
                <div>Passed</div>
            </div>
            <div class="summary-item">
                <div class="summary-value failed">{report_data['summary']['failed']}</div>
                <div>Failed</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{report_data['summary']['success_rate']:.1f}%</div>
                <div>Success Rate</div>
            </div>
        </div>
"""

    # Add detailed results
    for i, result in enumerate(report_data['results']):
        status = '✅' if result['success'] else '❌'
        css_class = 'task-passed' if result['success'] else 'task-failed'
        badge_class = 'badge-success' if result['success'] else 'badge-danger'
        
        html += f"""
        <div class="task-detail {css_class}">
            <div class="collapsible" onclick="toggleContent('task-{i}')">
                <h3>{status} {result['task_file']} <span class="badge {badge_class}">{result['actions_validated']} actions</span></h3>
                <p><strong>Environment:</strong> {result['environment']} | <strong>Execution Time:</strong> {result['execution_time_ms']:.2f}ms</p>
            </div>
            <div id="task-{i}" class="content">
"""
        
        if result.get('error'):
            html += f'<div class="action-detail"><strong>Task Error:</strong> <span class="failed">{result["error"]}</span></div>'
        
        # Add action details
        for j, action in enumerate(result.get('action_results', [])):
            action_status = '✅' if action['success'] else '❌'
            action_badge = 'badge-success' if action['success'] else 'badge-danger'
            
            html += f"""
            <div class="action-detail">
                <h4>{action_status} Action: {action['action_name']} <span class="badge {action_badge}">{action.get('execution_time_ms', 0):.2f}ms</span></h4>
"""
            
            if action.get('error'):
                html += f'<p><strong>Error:</strong> <span class="failed">{action["error"]}</span></p>'
            
            # Add expected vs actual comparison if available
            if 'expected_output' in action and 'actual_output' in action:
                html += """
                <div class="comparison">
                    <div class="expected">
                        <h5>Expected Output</h5>
                        <pre>{}</pre>
                    </div>
                    <div class="actual">
                        <h5>Actual Output</h5>
                        <pre>{}</pre>
                    </div>
                </div>
                """.format(
                    json.dumps(action['expected_output'], indent=2) if action['expected_output'] else 'None',
                    json.dumps(action['actual_output'], indent=2) if action['actual_output'] else 'None'
                )
            
            html += '</div>'
        
        html += '</div></div>'

    # Add JavaScript functionality
    html += f"""
    </div>
    
    <script>
        const reportData = {json.dumps(report_data, indent=2)};
        let allExpanded = false;
        
        function downloadJson() {{
            const blob = new Blob([JSON.stringify(reportData, null, 2)], {{type: 'application/json'}});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'validation-report-{run_number}.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
        
        function toggleContent(id) {{
            const content = document.getElementById(id);
            content.classList.toggle('show');
        }}
        
        function toggleAll() {{
            const contents = document.querySelectorAll('.content');
            const button = document.querySelector('.download-btn:nth-child(3)');
            
            allExpanded = !allExpanded;
            
            contents.forEach(content => {{
                if (allExpanded) {{
                    content.classList.add('show');
                }} else {{
                    content.classList.remove('show');
                }}
            }});
            
            button.textContent = allExpanded ? '🔼 Collapse All' : '🔽 Expand All';
        }}
    </script>
</body>
</html>"""
    
    return html

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate standalone HTML validation report")
    parser.add_argument("--input", required=True, help="Input JSON report file")
    parser.add_argument("--output", required=True, help="Output HTML file")
    parser.add_argument("--run-number", required=True, help="GitHub run number")
    
    args = parser.parse_args()
    
    try:
        # Load JSON report
        with open(args.input, 'r') as f:
            report_data = json.load(f)
        
        # Generate standalone HTML
        html_content = generate_standalone_html_report(report_data, args.run_number)
        
        # Save HTML report
        with open(args.output, 'w') as f:
            f.write(html_content)
        
        print(f"Standalone HTML report generated: {args.output}")
        
    except Exception as e:
        print(f"Error generating standalone report: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())