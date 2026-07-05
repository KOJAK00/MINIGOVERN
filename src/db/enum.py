from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

class DatasetState(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"

class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class SemanticType(str, Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    COUNTRY = "COUNTRY"
    CURRENCY = "CURRENCY"
    DATE = "DATE"
    UUID = "UUID"
    PERSON_NAME = "PERSON_NAME"
    PASSWORD = "PASSWORD"
    IDENTIFIER = "IDENTIFIER"
    UNKNOWN = "UNKNOWN"

class AuditAction(str, Enum):
    CREATE_DATASOURCE = "create_datasource"
    UPDATE_DATASOURCE = "update_datasource"
    DELETE_DATASOURCE = "delete_datasource"

    START_SCAN = "start_scan"

    SUBMIT_DATASET = "submit_dataset"
    APPROVE_DATASET = "approve_dataset"
    REJECT_DATASET = "reject_dataset"

    ASSIGN_TAG = "assign_tag"
    REMOVE_TAG = "remove_tag"