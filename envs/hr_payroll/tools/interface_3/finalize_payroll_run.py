from tau_bench.envs.tool import Tool
from typing import Any, Dict
from datetime import datetime

class FinalizePayrollRun(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_run_id: str) -> str:
        run = data["payroll_runs"].get(payroll_run_id)
        if not run:
            raise ValueError(f"Payroll run {payroll_run_id} not found.")
        run["status"] = "finalized"
        run["finalized_at"] = datetime.utcnow().isoformat()
        return payroll_run_id

    @staticmethod
    def get_info():
        return {
            "name": "finalize_payroll_run",
            "description": "Finalizes a payroll run after all items are processed.",
            "parameters": {
                "payroll_run_id": "str"
            },
            "returns": "str"
        }