from sqlalchemy import (MetaData, Table, Integer, String,
                        Column, Text, DateTime, Boolean,
                        ForeignKey, create_engine)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timedelta, timezone
from enum import Enum
from config_data.config import TIME_ZONE

engine = create_engine('sqlite:///users_sqlite.db')
metadata = MetaData()

Base = declarative_base()

delta_time = timedelta(hours=int(TIME_ZONE))
time_zone = timezone(delta_time)


class OrderStatus(Enum):
    FIND = 'find'
    DRIVE = 'drive'
    END = 'end'


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_user_id = Column(Integer, unique=True)
    username = Column(String, nullable=False, unique=True)
    permission = Column(Boolean, default=True)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    location_id = Column(Integer)


class Drivers(Base):
    __tablename__ = 'drivers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    driver_id = Column(Integer, unique=True)
    is_available = Column(Boolean, default=False)


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.id'),nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.driver_id'))
    date_create = Column(DateTime, default=datetime.now(time_zone))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    username = Column(String, nullable=False)
    status_drive = Column(String, default=OrderStatus.FIND.value)

    location = relationship("Locations", back_populates="orders")


class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    location_name = Column(String, nullable=True)

    orders = relationship("Orders", back_populates="location")


class BannedUsers(Base):
    __tablename__ = 'banned_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))


Base.metadata.create_all(engine)
