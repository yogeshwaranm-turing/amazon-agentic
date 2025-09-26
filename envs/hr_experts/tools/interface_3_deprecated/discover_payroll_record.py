import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool



class DiscoverPayrollRecord(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], filters: Dict[str, Any] = None) -> str:
        """
        Discover payroll record records.
        """
        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format for payroll records"
            })
        
        results = []
        payroll_records = data.get("payroll_records", {})
        
        for payroll_id, payroll_data in payroll_records.items():
            if filters:
                match = True
                for filter_key, filter_value in filters.items():
                    payroll_value = payroll_data.get(filter_key)
                    if payroll_value != filter_value:
                        match = False
                        break
                if match:
                    results.append({**payroll_data, "payroll_id": payroll_id})
            else:
                results.append({**payroll_data, "payroll_id": payroll_id})
        
        return json.dumps({
            "success": True,
            "entity_type": "payroll_records",
            "count": len(results),
            "results": results
        })
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "discover_payroll_record",
                "description": "Discover payroll record records. Filterable by payroll_id (string), employee_id (string), pay_period_start (date), pay_period_end (date), hours_worked (decimal), hourly_rate (decimal), payment_date (date), status (enum: 'draft', 'approved', 'paid', 'cancelled'), approved_by (string), created_at (timestamp), updated_at (timestamp).",
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