import enum
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    create_engine,
    Table,
    Enum,
    func,
)

# lazy-intialize SQLAlchemy engine
engine = create_engine("sqlite+pysqlite:///db/flames.db")

# initialize SQLAlchemy metadata object
metadata_obj = MetaData()

# initialize enum for User roles
user_roles = enum.Enum("user_roles", ["admin", "cashier"])

# initialize enum for Staff roles
staff_roles = enum.Enum("staff_roles", ["manager", "chef", "cook", "driver", "waiter"])

# initialize enum for Payment type
payment_types = enum.Enum(
    "payment_types", ["cash", "card", "online", "cash-on-delivery"]
)

# initialize enum for Order status
order_status = enum.Enum(
    "order_status",
    [
        "pending",
        "confirmed",
        "in-progress",
        "out-for-delivery",
        "delivered",
        "cancelled",
        "completed",
        "on-hold",
        "returned",
        "refunded",
        "awaiting-pickup",
    ],
)

# initialize "User" object
user_table = Table(
    "user",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("name", String),
    Column("mobile_no", String(10), nullable=False, unique=True),
    Column("role", Enum(user_roles), nullable=False, server_default="cashier"),
    Column("created_at", DateTime, nullable=False, server_default=func.now()),
    Column("last_logged", DateTime),
)

# initialize "Customer" object
customer_table = Table(
    "customer",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("mobile_no", String(10), nullable=False, unique=True),
    Column("address", String, nullable=False),
    Column("city", String, nullable=False),
    Column("email", String, unique=True),
    Column("registered_at", DateTime, nullable=False, server_default=func.now()),
)

# initialize "Staff" object
staff_table = Table(
    "staff",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("role", Enum(staff_roles), nullable=False, server_default="waiter"),
    Column("mobile_no", String(10), nullable=False, unique=True),
    Column("email", String, unique=True),
)

# initialize "Payment" object
payment_table = Table(
    "payment",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("amount", Numeric, nullable=False),
    Column("type", Enum(payment_types), nullable=False, server_default="cash"),
    Column("paid", Numeric, nullable=False),
    Column("balance", Numeric),
    Column("paid_at", DateTime, nullable=False),
    Column("discount", Numeric),
)

# initialize "Order" object
order_table = Table(
    "order",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("type", String, nullable=False),
    Column("description", String),
    Column("status", Enum(order_status), nullable=False, server_default="pending"),
    Column("ordered_at", DateTime, nullable=False, server_default=func.now()),
    Column("completed_at", DateTime),
    Column("table_no", Integer),
    Column("customer_id", ForeignKey("customer.id"), nullable=False),
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("payment_id", ForeignKey("payment.id"), nullable=False),
    Column("staff_id", ForeignKey("staff.id"), nullable=False),
)

# initialize "Product" object
product_table = Table(
    "product",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("price", Numeric, nullable=False),
)

# initialize "Order_Product" object
order_product_table = Table(
    "order_product",
    metadata_obj,
    Column("order_id", ForeignKey("order.id"), nullable=False),
    Column("product_id", ForeignKey("product.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
)

# apply objects to database
metadata_obj.create_all(engine)