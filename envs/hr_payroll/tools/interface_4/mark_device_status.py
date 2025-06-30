from tau_bench.envs.tool import Tool
from typing import Any, Dict

class MarkDeviceStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], device_id: str, status: str) -> str:
        device = data["devices"].get(device_id)
        if not device:
            raise ValueError("Device not found.")
        device["status"] = status
        return device_id

    @staticmethod
    def get_info():
        return {
            "name": "mark_device_status",
            "description": "Updates the status of a device (e.g., return_pending, returned).",
            "parameters": {
                "device_id": "str",
                "status": "str"
            },
            "returns": "str"
        }