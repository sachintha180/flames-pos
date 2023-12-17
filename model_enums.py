import enum


# declare enum for user role
class UserRole(enum.Enum):
    admin = "admin"
    cashier = "cashier"


# declare enum for staff role
class StaffRole(enum.Enum):
    manager = "manager"
    chef = "chef"
    cook = "cook"
    driver = "driver"
    waiter = "waiter"


# declare enum for payment type
class PaymentType(enum.Enum):
    cash = "cash"
    card = "card"
    online = "online"
    cash_on_delivery = "cash_on_delivery"


# declare enum for order status
class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    in_progress = "in_progress"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"
    completed = "completed"
    on_hold = "on_hold"
    returned = "returned"
    refunded = "refunded"
    awaiting_pickup = "awaiting_pickup"