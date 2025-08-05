from enum import Enum
class Subscription(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
