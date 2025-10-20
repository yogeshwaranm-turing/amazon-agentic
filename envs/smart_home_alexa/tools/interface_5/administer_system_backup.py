import json
import hashlib
from typing import Any, Dict
from datetime import datetime
from tau_bench.envs.tool import Tool

class AdministerSystemBackup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], operation: str, backup_id: str = None, backup_location_type: str = None, operation_data: Dict[str, Any] = None) -> str:
        """
        Create and manage system backups in the smart home management system.
        Handles backup file creation, storage operations, checksum calculation,
        and backup record management for disaster recovery purposes.
        """

        # Validate operation type
        valid_operations = ["create_file", "save_to_storage", "create_record", "calculate_size", "calculate_checksum"]
        if operation not in valid_operations:
            return json.dumps({
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be one of: {', '.join(valid_operations)}"
            })

        if not isinstance(data, dict):
            return json.dumps({
                "success": False,
                "error": "Invalid data format"
            })

        if not operation_data:
            operation_data = {}

        # Get backups table from schema
        backups = data.get("backups", {})

        if operation == "create_file":
            # Create backup file from system data
            if not backup_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_id required for create_file operation"
                })

            # Get included tables from operation_data
            included_tables = operation_data.get("included_tables", ["all"])

            if "all" in included_tables:
                # Backup all core tables
                included_tables = [
                    "devices", "users", "routines", "groups", "skills",
                    "voice_profiles", "access_logs", "user_device_permissions",
                    "user_group_permissions", "skill_device_permissions", "routine_devices"
                ]

            # Create backup manifest
            backup_data = {}
            total_records = 0

            for table_name in included_tables:
                if table_name in data:
                    table_data = data.get(table_name, {})
                    backup_data[table_name] = table_data
                    total_records += len(table_data) if isinstance(table_data, dict) else 0

            # Serialize backup data
            backup_content = json.dumps(backup_data, indent=2)
            file_size = len(backup_content.encode('utf-8'))

            # Store temporarily (in real implementation, would write to file)
            backup_file_path = f"/tmp/smart_home_backup_{backup_id}.json"

            return json.dumps({
                "success": True,
                "operation": "create_file",
                "backup_id": backup_id,
                "file_path": backup_file_path,
                "file_size": file_size,
                "included_tables": included_tables,
                "total_records": total_records,
                "timestamp": "2025-10-16T14:30:00",
                "message": f"Backup file created successfully: {file_size} bytes, {total_records} records"
            })

        elif operation == "save_to_storage":
            # Save backup file to storage location
            if not backup_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_id required for save_to_storage operation"
                })

            if not backup_location_type:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_location_type required for save_to_storage operation"
                })

            # Validate backup_location_type
            valid_locations = ["cloud", "local"]
            if backup_location_type not in valid_locations:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid backup_location_type '{backup_location_type}'. Must be one of: {', '.join(valid_locations)}"
                })

            # Get source file path
            source_file_path = operation_data.get("source_file_path")
            if not source_file_path:
                return json.dumps({
                    "success": False,
                    "error": "Halt: source_file_path required in operation_data for save_to_storage"
                })

            # Determine storage location
            if backup_location_type == "cloud":
                storage_location = f"s3://smart-home-backups/{backup_id}.json"
                storage_provider = "Amazon S3"
            else:  # local
                storage_location = f"/var/backups/smart_home/{backup_id}.json"
                storage_provider = "Local Filesystem"

            # Simulate upload (in real implementation, would perform actual upload)
            upload_status = "completed"
            upload_duration_seconds = 2.5

            return json.dumps({
                "success": True,
                "operation": "save_to_storage",
                "backup_id": backup_id,
                "backup_location_type": backup_location_type,
                "storage_location": storage_location,
                "storage_provider": storage_provider,
                "upload_status": upload_status,
                "upload_duration_seconds": upload_duration_seconds,
                "timestamp": "2025-10-16T14:30:00",
                "message": f"Backup saved successfully to {backup_location_type} storage"
            })

        elif operation == "create_record":
            # Create backup metadata record in database
            if not backup_id:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_id required for create_record operation"
                })

            # Validate backup doesn't already exist
            if backup_id in backups:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Backup record already exists for backup_id '{backup_id}'"
                })

            # Get required fields from operation_data
            file_size = operation_data.get("file_size")
            storage_location = operation_data.get("storage_location")
            backup_location_type = operation_data.get("backup_location_type")
            checksum = operation_data.get("checksum")
            created_by_user_id = operation_data.get("created_by_user_id")
            backup_manifest = operation_data.get("backup_manifest", {})

            if not all([file_size, storage_location, backup_location_type, checksum, created_by_user_id]):
                return json.dumps({
                    "success": False,
                    "error": "Halt: file_size, storage_location, backup_location_type, checksum, and created_by_user_id required in operation_data"
                })

            # Validate backup_location_type
            valid_locations = ["cloud", "local"]
            if backup_location_type not in valid_locations:
                return json.dumps({
                    "success": False,
                    "error": f"Halt: Invalid backup_location_type '{backup_location_type}'. Must be one of: {', '.join(valid_locations)}"
                })

            # Create backup record
            timestamp = "2025-10-16T14:30:00"
            backup_record = {
                "backup_id": backup_id,
                "timestamp": timestamp,
                "file_size": file_size,
                "storage_location": storage_location,
                "backup_location_type": backup_location_type,
                "checksum": checksum,
                "status": "completed",
                "backup_data": json.dumps(backup_manifest) if backup_manifest else None,
                "created_by_user_id": created_by_user_id,
                "created_date": timestamp
            }

            backups[backup_id] = backup_record

            return json.dumps({
                "success": True,
                "operation": "create_record",
                "backup_id": backup_id,
                "backup_record": backup_record,
                "message": f"Backup record created successfully for backup '{backup_id}'"
            })

        elif operation == "calculate_size":
            # Calculate size of backup data
            tables_to_backup = operation_data.get("tables", ["all"])

            if "all" in tables_to_backup:
                tables_to_backup = list(data.keys())

            total_size = 0
            table_sizes = {}

            for table_name in tables_to_backup:
                if table_name in data:
                    table_data = data.get(table_name, {})
                    table_json = json.dumps(table_data)
                    table_size = len(table_json.encode('utf-8'))
                    table_sizes[table_name] = table_size
                    total_size += table_size

            return json.dumps({
                "success": True,
                "operation": "calculate_size",
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "table_count": len(table_sizes),
                "table_sizes": table_sizes,
                "message": f"Backup size calculated: {total_size} bytes across {len(table_sizes)} tables"
            })

        elif operation == "calculate_checksum":
            # Calculate SHA-256 checksum of backup data
            backup_data_content = operation_data.get("backup_content")

            if not backup_data_content:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_content required in operation_data for calculate_checksum"
                })

            # Calculate SHA-256 checksum
            if isinstance(backup_data_content, str):
                backup_bytes = backup_data_content.encode('utf-8')
            elif isinstance(backup_data_content, dict):
                backup_bytes = json.dumps(backup_data_content).encode('utf-8')
            else:
                return json.dumps({
                    "success": False,
                    "error": "Halt: backup_content must be string or dict"
                })

            checksum = hashlib.sha256(backup_bytes).hexdigest()

            return json.dumps({
                "success": True,
                "operation": "calculate_checksum",
                "checksum": checksum,
                "checksum_algorithm": "SHA-256",
                "data_size": len(backup_bytes),
                "message": f"Checksum calculated: {checksum}"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "administer_system_backup",
                "description": "Create and manage system backups in the smart home management system. Creates backup files by serializing system data including devices, users, routines, groups, skills, and configurations (SOP 6.7.3), saves backup files to cloud (Amazon S3) or local storage with upload verification, creates backup metadata records with file size, location, checksum, and manifest information for backup tracking, calculates backup file size across selected tables to assess storage requirements, and computes SHA-256 checksums for backup integrity verification and corruption detection. Essential for disaster recovery, system migration, and data protection.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Backup operation to perform",
                            "enum": ["create_file", "save_to_storage", "create_record", "calculate_size", "calculate_checksum"]
                        },
                        "backup_id": {
                            "type": "string",
                            "description": "Unique identifier for the backup (required for create_file, save_to_storage, create_record)"
                        },
                        "backup_location_type": {
                            "type": "string",
                            "description": "Storage location type: cloud or local (required for save_to_storage, create_record)",
                            "enum": ["cloud", "local"]
                        },
                        "operation_data": {
                            "type": "object",
                            "description": "Operation-specific parameters. For create_file: {included_tables}. For save_to_storage: {source_file_path}. For create_record: {file_size, storage_location, backup_location_type, checksum, created_by_user_id, backup_manifest}. For calculate_size: {tables}. For calculate_checksum: {backup_content}",
                            "properties": {
                                "included_tables": {
                                    "type": "array",
                                    "description": "List of table names to include in backup (or ['all'] for all tables)"
                                },
                                "source_file_path": {
                                    "type": "string",
                                    "description": "Path to backup file to upload"
                                },
                                "file_size": {
                                    "type": "number",
                                    "description": "Size of backup file in bytes"
                                },
                                "storage_location": {
                                    "type": "string",
                                    "description": "Full path to stored backup (URL or filesystem path)"
                                },
                                "checksum": {
                                    "type": "string",
                                    "description": "SHA-256 checksum of backup file"
                                },
                                "created_by_user_id": {
                                    "type": "string",
                                    "description": "User ID who created the backup"
                                },
                                "backup_manifest": {
                                    "type": "object",
                                    "description": "Backup manifest with included tables and metadata"
                                },
                                "tables": {
                                    "type": "array",
                                    "description": "List of tables to calculate size for"
                                },
                                "backup_content": {
                                    "description": "Backup content (string or dict) for checksum calculation"
                                }
                            }
                        }
                    },
                    "required": ["operation"]
                }
            }
        }
