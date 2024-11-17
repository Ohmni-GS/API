from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    community = Column(String, nullable=False)
    is_manager = Column(Boolean, default=False)

class CommunityModel(Base):
    __tablename__ = 'communities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=False)

class DeviceModel(Base):
    __tablename__ = 'devices'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    owner = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    is_collective = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

class DeviceDataModel(Base):
    __tablename__ = 'device_data'
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=False)
    data = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)