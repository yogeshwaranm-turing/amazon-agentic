from .access_logs import AccessLogs
from .administer_audit_logs import AdministerAuditLogs
from .administer_entity import AdministerEntity
from .administer_relationships import AdministerRelationships
from .administer_routine_ops import AdministerRoutineOps
from .administer_skill import AdministerSkill
from .administer_skill_linking import AdministerSkillLinking
from .administer_system_backup import AdministerSystemBackup
from .administer_user_sessions import AdministerUserSessions
from .adjust_routine_config import AdjustRoutineConfig
from .archive_device_config import ArchiveDeviceConfig
from .check_entity_status import CheckEntityStatus
from .configure_alerts import ConfigureAlerts
from .configure_permissions import ConfigurePermissions
from .construct_report import ConstructReport
from .control_entity_batch import ControlEntityBatch
from .control_firmware import ControlFirmware
from .coordinate_user_operation import CoordinateUserOperation
from .derive_metrics import DeriveMetrics
from .determine_schedule import DetermineSchedule
from .evaluate_device import EvaluateDevice
from .examine_patterns import ExaminePatterns
from .generate_access_tokens import GenerateAccessTokens
from .group_data import GroupData
from .inspect_device import InspectDevice
from .inspect_input import InspectInput
from .inspect_system_status import InspectSystemStatus
from .observe_system import ObserveSystem
from .process_authentication import ProcessAuthentication
from .refine_data import RefineData
from .route_to_human import RouteToHuman
from .search_entities import SearchEntities
from .store_data import StoreData
from .tag_entity import TagEntity
from .tune_device import TuneDevice
from .validate_auth import ValidateAuth

ALL_TOOLS_INTERFACE_5 = [
    AccessLogs,
    AdministerAuditLogs,
    AdministerEntity,
    AdministerRelationships,
    AdministerRoutineOps,
    AdministerSkill,
    AdministerSkillLinking,
    AdministerSystemBackup,
    AdministerUserSessions,
    AdjustRoutineConfig,
    ArchiveDeviceConfig,
    CheckEntityStatus,
    ConfigureAlerts,
    ConfigurePermissions,
    ConstructReport,
    ControlEntityBatch,
    ControlFirmware,
    CoordinateUserOperation,
    DeriveMetrics,
    DetermineSchedule,
    EvaluateDevice,
    ExaminePatterns,
    GenerateAccessTokens,
    GroupData,
    InspectDevice,
    InspectInput,
    InspectSystemStatus,
    ObserveSystem,
    ProcessAuthentication,
    RefineData,
    RouteToHuman,
    SearchEntities,
    StoreData,
    TagEntity,
    TuneDevice,
    ValidateAuth,
]
