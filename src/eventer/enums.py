from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    JUDGE = "judge"
    ORGANIZER = "organizer"
    TRAINER = "trainer"
    USER = "user"


class Status(str, Enum):
    VALIDATED = "validated"
    REJECTED = "rejected"
    ACTIVE = "active"
    WAITING = "waiting"
    CLOSED = "closed"


class StageType(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class UserStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


class EventFormat(str, Enum):
    OPEN = "open"
    OFFLINE = "offline"
    HYBRID = "hybrid"


class CertificateType(str, Enum):
    PARTICIPATION = "participation"
    WINNER = "winner"
    SPECIAL_MENTION = "special_mention"
