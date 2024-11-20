from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.depends import get_db_session
from app.utils.device import DeviceService
from app.schemas import (
    AllDeviceData,
    DefaultResponse,
    Device,
    DeviceAdd,
    DeviceData,
    Devices,
    HTTPErrorRequest,
)

devices_router = APIRouter(prefix="/devices", tags=["Devices"])


def get_device_service(db: Session = Depends(get_db_session)) -> DeviceService:
    return DeviceService(db=db)

@devices_router.get(
    "/",
    response_model=Devices,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"description": "Erro interno do servidor", "model": HTTPErrorRequest},
    },
)
def get_devices(device_service: DeviceService = Depends(get_device_service)) -> Devices:
    return device_service.get_all_devices()

@devices_router.get(
    "/{device_id}",
    response_model=AllDeviceData,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Dispositivo não encontrado", "model": HTTPErrorRequest},
        500: {"description": "Erro interno do servidor", "model": HTTPErrorRequest},
    },
)
def get_device_data(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
) -> AllDeviceData:
    return device_service.get_device_data(device_id)

@devices_router.get(
    "/{device_id}/latest",
    response_model=DeviceData,
    status_code=status.HTTP_200_OK,
    responses={
        404: {
            "description": "Dispositivo não encontrado ou sem dados",
            "model": HTTPErrorRequest,
        },
        500: {"description": "Erro interno do servidor", "model": HTTPErrorRequest},
    },
)
def get_latest_device_data(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
) -> DeviceData:
    return device_service.get_latest_data(device_id)

@devices_router.post(
    "/",
    response_model=DefaultResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Erro ao cadastrar dispositivo", "model": HTTPErrorRequest},
        500: {"description": "Erro interno do servidor", "model": HTTPErrorRequest},
    },
)
def add_device(
    device: DeviceAdd, device_service: DeviceService = Depends(get_device_service)
) -> DefaultResponse:
    return device_service.add_device(device)

@devices_router.post(
    "/{device_id}/connect",
    response_model=DefaultResponse,
    status_code=status.HTTP_200_OK,
    responses={
        408: {
            "description": "O dispositivo não respondeu no tempo estipulado.",
            "model": HTTPErrorRequest,
        },
        500: {
            "description": "Erro ao se conectar no Broker MQTT",
            "model": HTTPErrorRequest,
        },
    },
)
async def connect_device(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
) -> DefaultResponse:
    return await device_service.connect_device(device_id)

@devices_router.post(
    "/{device_id}/disconnect",
    response_model=DefaultResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Dispositivo não encontrado", "model": HTTPErrorRequest},
        500: {"description": "Erro interno do servidor", "model": HTTPErrorRequest},
    },
)
async def disconnect_device(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
) -> DefaultResponse:
    return await device_service.disconnect_device(device_id)


@devices_router.delete(
    "/{device_id}",
    response_model=DefaultResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "Dispositivo não encontrado", "model": HTTPErrorRequest},
        500: {"description": "Erro interno do servidor", "model": HTTPErrorRequest},
    },
)
def delete_device(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
) -> DefaultResponse:
    return device_service.delete_device(device_id)

