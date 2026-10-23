from enum import Enum

class PaymentStatus(str, Enum):
    APPROVED = "approved"
    DECLINED = "declined"