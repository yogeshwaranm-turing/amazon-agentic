from .arrange_user_operation import ArrangeUserOperation
from .backup_data import BackupData
from .build_report import BuildReport
from .confirm_system_state import ConfirmSystemState
from .control_notifications import ControlNotifications
from .control_user_sessions import ControlUserSessions
from .create_access_codes import CreateAccessCodes
from .evaluate_device import EvaluateDevice
from .evaluate_metrics import EvaluateMetrics
from .evaluate_patterns import EvaluatePatterns
from .fetch_logs import FetchLogs
from .generate_schedule import GenerateSchedule
from .handle_authentication import HandleAuthentication
from .handle_entity_links import HandleEntityLinks
from .handle_routine_tasks import HandleRoutineTasks
from .handover_to_human import HandOverToHuman
from .initialize_device import InitializeDevice
from .maintain_audit_logs import MaintainAuditLogs
from .maintain_skill import MaintainSkill
from .maintain_skill_linking import MaintainSkillLinking
from .maintain_system_backup import MaintainSystemBackup
from .mark_entity import MarkEntity
from .process_entities_batch import ProcessEntitiesBatch
from .process_entity import ProcessEntity
from .retrieve_entities import RetrieveEntities
from .retrieve_entity_status import RetrieveEntityStatus
from .screen_data import ScreenData
from .set_permissions import SetPermissions
from .set_routine_settings import SetRoutineSettings
from .snapshot_device_config import SnapshotDeviceConfig
from .sort_data import SortData
from .track_firmware import TrackFirmware
from .track_system import TrackSystem
from .troubleshoot_device import TroubleshootDevice
from .verify_authorization import VerifyAuthorization
from .verify_input import VerifyInput

ALL_TOOLS_INTERFACE_4 = [
    ArrangeUserOperation,
    BackupData,
    BuildReport,
    ConfirmSystemState,
    ControlNotifications,
    ControlUserSessions,
    CreateAccessCodes,
    EvaluateDevice,
    EvaluateMetrics,
    EvaluatePatterns,
    FetchLogs,
    GenerateSchedule,
    HandleAuthentication,
    HandleEntityLinks,
    HandleRoutineTasks,
    HandOverToHuman,
    InitializeDevice,
    MaintainAuditLogs,
    MaintainSkill,
    MaintainSkillLinking,
    MaintainSystemBackup,
    MarkEntity,
    ProcessEntitiesBatch,
    ProcessEntity,
    RetrieveEntities,
    RetrieveEntityStatus,
    ScreenData,
    SetPermissions,
    SetRoutineSettings,
    SnapshotDeviceConfig,
    SortData,
    TrackFirmware,
    TrackSystem,
    TroubleshootDevice,
    VerifyAuthorization,
    VerifyInput,
]
