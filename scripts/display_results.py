#!/usr/bin/env python3
"""
Display detailed validation results in the terminal.
"""

import argparse
import json
import sys

def display_validation_results(report_data: dict):
    """Display detailed validation results with action-by-action comparison"""
    
    print('\n' + '='*80)
    print('🧪 DETAILED VALIDATION RESULTS')
    print('='*80)
    
    summary = report_data['summary']
    print(f'📊 SUMMARY: {summary["passed"]}/{summary["total"]} tasks passed ({summary["success_rate"]:.1f}%)')
    print()
    
    for result in report_data['results']:
        status = '✅' if result['success'] else '❌'
        print(f'{status} TASK: {result["task_file"]}')
        print(f'   Environment: {result["environment"]}')
        print(f'   Actions: {result["actions_validated"]}')
        print(f'   Time: {result["execution_time_ms"]:.2f}ms')
        
        if result.get('error'):
            print(f'   ❌ Task Error: {result["error"]}')
        
        print()
        
        for i, action in enumerate(result.get('action_results', []), 1):
            action_status = '✅' if action['success'] else '❌'
            print(f'   {action_status} ACTION {i}: {action["action_name"]}')
            print(f'      Time: {action.get("execution_time_ms", 0):.2f}ms')
            
            if action.get('error'):
                print(f'      ❌ Error: {action["error"]}')
            
            # Show expected vs actual comparison
            if 'expected_output' in action and 'actual_output' in action:
                print(f'      📋 EXPECTED OUTPUT:')
                expected = json.dumps(action['expected_output'], indent=8) if action['expected_output'] else 'None'
                for line in expected.split('\n'):
                    print(f'        {line}')
                
                print(f'      📋 ACTUAL OUTPUT:')
                actual = json.dumps(action['actual_output'], indent=8) if action['actual_output'] else 'None'
                for line in actual.split('\n'):
                    print(f'        {line}')
                
                # Simple comparison
                if action['expected_output'] == action['actual_output']:
                    print(f'      ✅ MATCH: Outputs are identical')
                else:
                    print(f'      ❌ MISMATCH: Outputs differ')
                    
                    # Show specific differences for better debugging
                    if isinstance(action['expected_output'], dict) and isinstance(action['actual_output'], dict):
                        expected_keys = set(action['expected_output'].keys()) if action['expected_output'] else set()
                        actual_keys = set(action['actual_output'].keys()) if action['actual_output'] else set()
                        
                        missing_keys = expected_keys - actual_keys
                        extra_keys = actual_keys - expected_keys
                        
                        if missing_keys:
                            print(f'      🔍 Missing keys: {", ".join(missing_keys)}')
                        if extra_keys:
                            print(f'      🔍 Extra keys: {", ".join(extra_keys)}')
                        
                        # Check value differences for common keys
                        common_keys = expected_keys & actual_keys
                        for key in common_keys:
                            if action['expected_output'][key] != action['actual_output'][key]:
                                print(f'      🔍 Different value for "{key}": {action["expected_output"][key]} → {action["actual_output"][key]}')
            
            print()
        
        print('-' * 60)
        print()
    
    print('='*80)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Display validation results")
    parser.add_argument("--input", required=True, help="Input JSON report file")
    
    args = parser.parse_args()
    
    try:
        # Load JSON report
        with open(args.input, 'r') as f:
            report_data = json.load(f)
        
        # Display results
        display_validation_results(report_data)
        
    except Exception as e:
        print(f"Error displaying results: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())