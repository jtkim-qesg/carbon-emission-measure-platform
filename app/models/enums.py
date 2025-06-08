import enum

class UserRoleEnum(enum.Enum):
    GENERAL = "일반"
    SUPER = "슈퍼"

class CycleStatusEnum(enum.Enum):
    NOT_STARTED = "산정 미시작"
    STARTED = "산정 시작"
    UPLOADING = "업로드 중"
    PENDING_REQUEST = "평가 미신청"
    SUBMITTING = "제출 중"
    FEEDBACK = "피드백 중"
    DONE = "완료"

class AttachmentTypeEnum(enum.Enum):
    SCOPE12 = "scope12"
    WASTE = "waste"
    MATERIAL = "material"
    TRANSPORT = "transport"

class ReviewStatusEnum(enum.Enum):
    REQUEST_CHANGE = "수정 요청"
    APPROVED = "승인"
