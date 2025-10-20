from .handle_entity import HandleEntity
from .fetch_entities import FetchEntities
from .bulk_entity_operations import BulkEntityOperations
from .map_entities import MapEntities
from .control_access import ControlAccess
from .fetch_entity_status import FetchEntityStatus
from .check_input import CheckInput
from .check_system_integrity import CheckSystemIntegrity
from .validate_access import ValidateAccess
from .setup_device import SetupDevice
from .check_device_performance import CheckDevicePerformance
from .run_device_diagnostics import RunDeviceDiagnostics
from .firmware_controller import FirmwareController
from .config_backup_manager import ConfigBackupManager
from .execute_routine import ExecuteRoutine
from .configure_routine import ConfigureRoutine
from .compute_schedule import ComputeSchedule
from .handle_user_sessions import HandleUserSessions
from .control_authentication import ControlAuthentication
from .organize_user_operation import OrganizeUserOperation
from .issue_access_codes import IssueAccessCodes
from .handle_skill import HandleSkill
from .handle_skill_association import HandleSkillAssociation
from .handle_system_backup import HandleSystemBackup
from .supervise_system import SuperviseSystem
from .switch_to_human import SwitchToHuman
from .compile_report import CompileReport
from .handle_notifications import HandleNotifications
from .handle_audit_logs import HandleAuditLogs
from .data_selection import DataSelection
from .classify_data import ClassifyData
from .compute_metrics import ComputeMetrics
from .detect_patterns import DetectPatterns
from .data_retention import DataRetention
from .view_logs import ViewLogs
from .highlight_entity import HighlightEntity

ALL_TOOLS_INTERFACE_2 = [
    HandleEntity,
    FetchEntities,
    BulkEntityOperations,
    MapEntities,
    ControlAccess,
    FetchEntityStatus,
    CheckInput,
    CheckSystemIntegrity,
    ValidateAccess,
    SetupDevice,
    CheckDevicePerformance,
    RunDeviceDiagnostics,
    FirmwareController,
    ConfigBackupManager,
    ExecuteRoutine,
    ConfigureRoutine,
    ComputeSchedule,
    HandleUserSessions,
    ControlAuthentication,
    OrganizeUserOperation,
    IssueAccessCodes,
    HandleSkill,
    HandleSkillAssociation,
    HandleSystemBackup,
    SuperviseSystem,
    SwitchToHuman,
    CompileReport,
    HandleNotifications,
    HandleAuditLogs,
    DataSelection,
    ClassifyData,
    ComputeMetrics,
    DetectPatterns,
    DataRetention,
    ViewLogs,
    HighlightEntity,
]

