import re
from sqlite3 import connect
from typing import Optional
from pydantic import BaseModel, field_validator

class User(BaseModel):
    full_name: str
    email: str
    password: str
    community_id: int
    is_manager: bool

    @field_validator('email')
    def email_must_be_valid(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('invalid email address')
        return v
    
    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('password is too short')
        return v
    
    @field_validator('community_id')
    def community_id_must_be_valid(cls, v):
        if not isinstance(v, int):
            raise ValueError('community_id must be an integer')
        return v
    
    @field_validator('is_manager')
    def is_manager_must_be_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError('is_manager must be a boolean')
        return v
    
class UserWithoutPassword(BaseModel):
    id: int
    full_name: str
    email: str
    community_id: int
    is_manager: bool

    @field_validator('email')
    def email_must_be_valid(cls, v):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('invalid email address')
        return v
    
    @field_validator('community_id')
    def community_id_must_be_valid(cls, v):
        if not isinstance(v, int):
            raise ValueError('community_id must be an integer')
        return v
    
    @field_validator('is_manager')
    def is_manager_must_be_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError('is_manager must be a boolean')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    community_id: Optional[int] = None
    is_manager: Optional[bool] = None

    @field_validator('email')
    def email_must_be_valid(cls, v):
        if v and not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError('invalid email address')
        return v
    
    @field_validator('password')
    def password_must_be_strong(cls, v):
        if v and len(v) < 8:
            raise ValueError('password is too short')
        return v
    
class Community(BaseModel):
    id: int
    name: str

    @field_validator('name')
    def name_must_be_valid(cls, v):
        if not re.match(r"[a-zA-Z0-9_]+", v):
            raise ValueError('invalid community name')
        return v

class Devices(BaseModel):
    devices: list[dict]
    total: int

    @field_validator('devices')
    def devices_must_be_valid(cls, v):
        if not isinstance(v, list) or not all(isinstance(i, dict) for i in v):
            raise ValueError('data must be a list of dictionaries')
        return v
    
    @field_validator('total')
    def total_must_be_valid(cls, v):
        if not isinstance(v, int):
            raise ValueError('total must be an integer')
        return v

class Device(BaseModel):
    id: str
    name: str
    owner: int
    type: str
    is_collective: bool
    is_active: bool

    @field_validator('name')
    def name_must_be_valid(cls, v):
        if not re.match(r"[a-zA-Z0-9_]+", v):
            raise ValueError('invalid device name')
        return v
    
    @field_validator('type')
    def type_must_be_valid(cls, v):
        if not re.match(r"[a-zA-Z0-9_]+", v):
            raise ValueError('invalid device type')
        return v
    
    @field_validator('is_collective')
    def is_collective_must_be_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError('is_collective must be a boolean')
        return v
    
    @field_validator('is_active')
    def is_active_must_be_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError('is_active must be a boolean')
        return v
    
class DeviceData(BaseModel):
    #id: int
    device_id: str
    connected: bool
    data: list[dict]

    @field_validator('device_id')
    def device_id_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('device_id must be an integer')
        return v
    
    @field_validator('connected')
    def connected_must_be_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError('connected must be a boolean')
        return v
    
    @field_validator('data')
    def data_must_be_valid(cls, v):
        if not isinstance(v, list) or not all(isinstance(i, dict) for i in v):
            raise ValueError('data must be a list of dictionaries')
        return v
    
class DeviceLatestData(BaseModel):
    # id: int
    device_id: str
    connected: bool
    latest_data: dict
    timestamp: str

    @field_validator('device_id')
    def device_id_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('device_id must be an integer')
        return v
    
    @field_validator('connected')
    def connected_must_be_valid(cls, v):
        if not isinstance(v, bool):
            raise ValueError('connected must be a boolean')
        return v
    
    @field_validator('latest_data')
    def data_must_be_valid(cls, v):
        if not isinstance(v, dict):
            raise ValueError('data must be a dictionary')
        return v
    
    @field_validator('timestamp')
    def timestamp_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('timestamp must be a string')
        return v

class DefaultResponse(BaseModel):
    msg: str

    @field_validator('msg')
    def detail_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('detail must be a string')
        return v
    
class HTTPErrorRequest(BaseModel):
    detail: str

    @field_validator('detail')
    def detail_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('detail must be a string')
        return v
    
class LoginResponse(BaseModel):
    access_token: str
    expires_in: str

    @field_validator('access_token')
    def access_token_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('access_token must be a string')
        return v
    
    @field_validator('expires_in')
    def expires_in_must_be_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError('expires_in must be a string')
        return v