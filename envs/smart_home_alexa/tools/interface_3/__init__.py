from .analyze_device import AnalyzeDevice
from .apply_device_config import ApplyDeviceConfig
from .associate_skill import AssociateSkill
from .auth_manager import AuthManager
from .batch_control_entities import BatchControlEntities
from .configure_firmware import ConfigureFirmware
from .control_alerts import ControlAlerts
from .control_audit_logs import ControlAuditLogs
from .control_entity import ControlEntity
from .control_routine_configurations import ControlRoutineConfigurations
from .control_routine_operations import ControlRoutineOperations
from .control_skill import ControlSkill
from .control_system_backup import ControlSystemBackup
from .create_access_tokens import CreateAccessTokens
from .create_report import CreateReport
from .escalate_to_human import EscalateToHuman
from .generate_metrics import GenerateMetrics
from .handle_config_backup import HandleConfigBackup
from .has_auth_access import HasAuthAccess
from .identify_patterns import IdentifyPatterns
from .inspect_entity_status import InspectEntityStatus
from .label_entity import LabelEntity
from .lookup_entities import LookupEntities
from .maintain_user_sessions import MaintainUserSessions
from .manage_access_rights import ManageAccessRights
from .manage_entity_links import ManageEntityLinks
from .plan_schedule import PlanSchedule
from .plan_user_operation import PlanUserOperation
from .preserve_data import PreserveData
from .read_logs import ReadLogs
from .run_device_tests import RunDeviceTests
from .sanitize_input import SanitizeInput
from .select_data import SelectData
from .tag_data import TagData
from .verify_system_condition import VerifySystemCondition
from .watch_system import WatchSystem

ALL_TOOLS_INTERFACE_3 = [
    AnalyzeDevice,
    ApplyDeviceConfig,
    AssociateSkill,
    AuthManager,
    BatchControlEntities,
    ConfigureFirmware,
    ControlAlerts,
    ControlAuditLogs,
    ControlEntity,
    ControlRoutineConfigurations,
    ControlRoutineOperations,
    ControlSkill,
    ControlSystemBackup,
    CreateAccessTokens,
    CreateReport,
    EscalateToHuman,
    GenerateMetrics,
    HandleConfigBackup,
    HasAuthAccess,
    IdentifyPatterns,
    InspectEntityStatus,
    LabelEntity,
    LookupEntities,
    MaintainUserSessions,
    ManageAccessRights,
    ManageEntityLinks,
    PlanSchedule,
    PlanUserOperation,
    PreserveData,
    ReadLogs,
    RunDeviceTests,
    SanitizeInput,
    SelectData,
    TagData,
    VerifySystemCondition,
    WatchSystem,
]
