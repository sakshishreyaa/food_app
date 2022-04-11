from typing import Type
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import func
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    JSON,
    Boolean,
    Float,
)
from sqlalchemy_utils.types.choice import ChoiceType
from app import db


class User(db.Model):
    TYPES = [("admin", "Admin"), ("customer", "Customer"), ("staff", "Staff")]

    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email = Column(String(80), unique=True)
    phone = Column(String(10), index=True, unique=True, nullable=False)
    role = Column(ChoiceType(TYPES), default=u"customer")
    password = Column(String(150), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name


class Customer(db.Model):
    __tablename__ = "Customer"
    user_id = Column(Integer, ForeignKey("User.id"), primary_key=True)
    name = Column(String(20), nullable=False)
    occupation = Column(String(80), nullable=False)
    dob = Column(DateTime)
    location = Column(Integer, ForeignKey("Location.id"))


class Restaurant(db.Model):
    __tablename__ = "Restaurant"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    owner = Column(Integer, ForeignKey("User.id"), nullable=False)
    no_of_staff = Column(Integer, nullable=False)
    seats = Column(Integer, nullable=True)
    extra_seats = Column(Integer, nullable=True)
    location_id = Column(Integer, ForeignKey("Location.id"))
    menu = Column(JSON, nullable=False)


class Location(db.Model):

    """Note: to avoid duplicating of locations and for sharding purpose ?"""

    __tablename__ = "Location"
    id = Column(Integer, primary_key=True)
    zip = Column(Integer, index=True)
    state = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    block_street = Column(String(50), nullable=False)
    # is this convinient for sharding??
    # restaurant_id = Column(Integer, ForeignKey("Restaurant.id"), nullable=False)


class Booking(db.Model):

    __tablename__ = "Booking"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("Restaurant.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), index=True)
    from_time = Column(DateTime)
    to_time = Column(DateTime)
    no_of_guests = Column(Integer, nullable=False)

    @staticmethod
    def get_available_seats(from_time, to_time, restaurant_id):
        return Restaurant.query.filter(
            Restaurant.id == restaurant_id
        ).no_of_seats - len(
            Booking.query.filter(
                Booking.from_time == from_time, Booking.to_time == to_time
            ).all()
        )


class Order(db.Model):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    price = Column(Float)
    paid_status = Column(Boolean, default=False)
    payment_id = Column(Integer, ForeignKey("Payment.id"))
    order_details = Column(JSON)
    items = Column(Integer)


class Payment(db.Model):
    __tablename__ = "Payment"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    source = Column(String(200))  # in case of online transactions
    online_payment = Column(Boolean, nullable=False)
    amount = Column(Float)


def init_db():
    db.create_all()
