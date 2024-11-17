from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.utils.device import DeviceService
from app.schemas import ConnectResponse, Device, DeviceData, DeviceLatestData, Devices, HTTPErrorRequest

devices_router = APIRouter(prefix="/devices", tags=["Devices"])

@devices_router.get("/", response_model=Devices, status_code=status.HTTP_200_OK)
def get_devices(device_service: DeviceService = Depends(DeviceService)):
    return device_service.get_all_devices()

@devices_router.get("/{device_id}", response_model=DeviceData, status_code=status.HTTP_200_OK, responses={404: {"description": "Dispositivo não encontrado", "model": HTTPErrorRequest}})
def get_device_data(device_id: str, device_service: DeviceService = Depends(DeviceService)) -> DeviceData:
    return device_service.get_device_data(device_id)

@devices_router.get("/{device_id}/connect", response_model=ConnectResponse, status_code=status.HTTP_200_OK, responses={408: {"description": "O dispositivo não respondeu no tempo estipulado.", "model": HTTPErrorRequest}, 500: {"description": "Erro ao se conectar no Broker MQTT", "model": HTTPErrorRequest}})
async def connect_device(device_id: str, device_service: DeviceService = Depends(DeviceService)) -> ConnectResponse:
    return await device_service.connect_device(device_id)

@devices_router.get("/{device_id}/latest", response_model=DeviceLatestData, status_code=status.HTTP_200_OK, responses={404: {"description": "Dispositivo não encontrado ou sem dados", "model": HTTPErrorRequest}})
def get_latest_device_data(device_id: str, device_service: DeviceService = Depends(DeviceService)) -> DeviceLatestData:
    return device_service.get_latest_data(device_id)
