import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class DiscoverPayrollDeduction(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover payroll deduction records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll deductions"
            })
        
        results = []
        payroll_deductions = data.get("payroll_deductions", {})
        
        for deduction_id, deduction_data in payroll_deductions.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    deduction_value = deduction_data.get(filter_key)
                    if deduction_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**deduction_data, "deduction_id": deduction_id})
            else:
                results.append({**deduction_data, "deduction_id": deduction_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "payroll_deductions",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_payroll_deduction",
                "description": "Discover payroll deduction records. Filterable by deduction_id (string), payroll_id (string), deduction_type (enum: 'tax', 'insurance', 'retirement', 'garnishment', 'equipment', 'other'), amount (decimal), created_by (string), created_at (timestamp).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filters": {
                            "type": "object",
                            "description": "Optional filters as JSON object with key-value pairs. SYNTAX: {\"key\": \"value\"} for single filter, {\"key1\": \"value1\", \"key2\": \"value2\"} for multiple filters (AND logic). RULES: Exact matches only, dates as YYYY-MM-DD and booleans as True/False."
                        }
                    }
                }
            }
        }