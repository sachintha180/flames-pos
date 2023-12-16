import datetime
import json
from typing import List
from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column,
    Table,
    DateTime,
    Integer,
    String,
    Numeric,
    func,
    ForeignKey,
    UniqueConstraint,
    Enum,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import model_enums as me


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flames.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String)
    mobile_no: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    role: Mapped[me.UserRole] = mapped_column(
        Enum(me.UserRole), nullable=False, server_default=me.UserRole.cashier.value
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    last_logged: Mapped[datetime.datetime] = mapped_column(DateTime)
    # foreign key constraints for user-order (1:M) - ON DELETE NO CHANGE
    order: Mapped[List["Order"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Customer(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    mobile_no: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True)
    registered_at: Mapped[str] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    # foreign key constraints for customer-order (1:M) - ON DELETE CASCADE
    order: Mapped[List["Order"]] = relationship(
        back_populates="customer", cascade="all, delete", passive_deletes=True
    )

    def __repr__(self):
        return f"<Customer {self.name}>"


class Staff(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[me.StaffRole] = mapped_column(
        Enum(me.StaffRole), nullable=False, server_default=me.StaffRole.waiter.value
    )
    mobile_no: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)

    def __repr__(self):
        return f"<Staff {self.name}>"


class Payment(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Numeric, nullable=False)
    ptype: Mapped[me.PaymentType] = mapped_column(
        Enum(me.PaymentType), nullable=False, server_default=me.PaymentType.cash.value
    )
    paid: Mapped[float] = mapped_column(Numeric, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric)
    paid_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    discount: Mapped[float] = mapped_column(Numeric)

    def __repr__(self):
        return f"<Payment {self.amount}>"


# SQLAlchemy.Core associative table for resolving order-product (M:M) relationship
OrderProduct = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("order.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("quantity", Integer, nullable=False),
)


class Order(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    otype: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[me.OrderStatus] = mapped_column(
        Enum(me.OrderStatus),
        nullable=False,
        server_default=me.OrderStatus.pending.value,
    )
    ordered_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime)
    table_no: Mapped[int] = mapped_column(Integer)
    # foreign key constraints for order-customer (M:1) - ON DELETE CASCADE
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id", ondelete="CASCADE")
    )
    customer: Mapped["Customer"] = relationship(back_populates="order")
    # foreign key constraints for order-user (M:1) - ON DELETE NO CHANGE
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="order")
    # foreign key constraint for order-payment (1:1) - ON DELETE NO CHANGE
    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"))
    payment: Mapped["Payment"] = relationship(back_populates="order")
    # foreign key constraint for order-staff (1:1) - ON DELETE NO CHANGE
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.id"))
    staff: Mapped["Staff"] = relationship(back_populates="order")
    # foreign key constraint for order-product (1:M) - ON DELETE NO CHANGE
    product: Mapped[List["Product"]] = relationship(
        secondary=OrderProduct, back_populates="order"
    )
    # setup unique constraints for 1:1 relationships
    __table_args__ = (UniqueConstraint("payment_id"), UniqueConstraint("staff_id"))

    def __repr__(self):
        return f"<Order {self.id}>"


# SQLAlchemy.Core model for product


class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Numeric, nullable=False)
    # foreign key constraint for order-product (1:M) - ON DELETE NO CHANGE
    order: Mapped[List["Order"]] = relationship(
        secondary=OrderProduct, back_populates="product"
    )

    def __repr__(self):
        return f"<Product {self.name}>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username, password = request.json["username"], request.json["password"]
        response = {"authenticated": True}
        return Response(
            response=json.dumps(response), status=200, mimetype="application/json"
        )


with app.app_context():
    db.create_all()
