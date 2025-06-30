from tau_bench.envs.tool import Tool
from typing import Any, Dict
import uuid
from datetime import datetime

class AddToPayrollRun(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payroll_run_id: str, payroll_item: Dict[str, Any]) -> str:
        run = data["payroll_runs"].get(payroll_run_id)
        if not run:
            raise ValueError(f"Payroll run {payroll_run_id} not found.")
        payroll_item_id = f"payitem_{uuid.uuid4().hex[:8]}"
        data["payroll_items"][payroll_item_id] = {
            "payroll_item_id": payroll_item_id,
            "payroll_run_id": payroll_run_id,
            **payroll_item,
            "created_at": datetime.utcnow().isoformat()
        }
        run.setdefault("payroll_items", []).append(payroll_item_id)
        return payroll_item_id

    @staticmethod
    def get_info():
        return {
            "name": "add_to_payroll_run",
            "description": "Adds a calculated payroll item to an existing payroll run.",
            "parameters": {
                "payroll_run_id": "str",
                "payroll_item": "Dict[str, Any]"
            },
            "returns": "str"
        }