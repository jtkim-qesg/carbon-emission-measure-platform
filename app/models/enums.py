import enum

class UserRoleEnum(enum.Enum):
    GENERAL = "GENERAL"
    SUPER = "SUPER"

class ProjectCodeStatusEnum(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    DONE = "DONE"

class CycleStatusEnum(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    UPLOADING = "UPLOADING"
    PENDING_REQUEST = "PENDING_REQUEST"
    SUBMITTING = "SUBMITTING"
    FEEDBACK = "FEEDBACK"
    DONE = "DONE"

class AttachmentTypeEnum(enum.Enum):
    SCOPE12 = "scope12"
    WASTE = "waste"
    MATERIAL = "material"
    TRANSPORT = "transport"

class ReviewStatusEnum(enum.Enum):
    REQUEST_CHANGE = "REQUEST_CHANGE"
    APPROVED = "APPROVED"
