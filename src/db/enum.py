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
    IDENTIFIER = "IDENTIFIER"
    UNKNOWN = "UNKNOWN"