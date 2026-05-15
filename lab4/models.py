from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey,
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=False)
    rooms = relationship("Room", back_populates="hotel")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id", ondelete="RESTRICT"), nullable=False)
    room_number = Column(String, nullable=False)
    type = Column(String, nullable=False)
    price = Column(Float, CheckConstraint("price > 0"), nullable=False)
    __table_args__ = (UniqueConstraint("hotel_id", "room_number"),)
    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    bookings = relationship("Booking", back_populates="client")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)

    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)

    status = Column(String, default="active", nullable=False)

    __table_args__ = (
        CheckConstraint("check_out > check_in"),
        CheckConstraint(
            "status IN ('active','cancelled','completed')"
        ),
    )

    client = relationship("Client", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")

    services = relationship(
        "Service",
        secondary="booking_services",
        back_populates="bookings"
    )

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, CheckConstraint("price >= 0"), nullable=False)
    bookings = relationship("Booking", secondary="booking_services", back_populates="services")

class BookingService(Base):
    __tablename__ = "booking_services"
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    __table_args__ = (UniqueConstraint("booking_id", "service_id"),)