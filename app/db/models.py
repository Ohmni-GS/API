from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    community_id = Column(Integer, ForeignKey('communities.id'), nullable=False)
    is_manager = Column(Boolean, default=False)

    community = relationship("CommunityModel", back_populates="users")
    devices = relationship("DeviceModel", back_populates="owner_user")

class CommunityModel(Base):
    __tablename__ = 'communities'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    users = relationship("UserModel", back_populates="community")

class DeviceModel(Base):
    __tablename__ = 'devices'
    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String, nullable=False)
    is_collective = Column(Boolean, default=False)
    connected = Column(Boolean, default=False)
    last_seen = Column(String, nullable=False)

    owner_user = relationship("UserModel", back_populates="devices")
    data = relationship("DeviceDataModel", back_populates="device", cascade="all, delete-orphan")

class DeviceDataModel(Base):
    __tablename__ = 'device_data'
    id = Column(String, primary_key=True, index=True)
    device_id = Column(String, ForeignKey('devices.id'), nullable=False)
    corrente = Column(String, nullable=False)
    tensao = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)

    device = relationship("DeviceModel", back_populates="data")
