from fastapi import HTTPException, status
from app.mqtt_client import mqtt_client, devices_data, connection_status, send_connect_message
from app.schemas import DefaultResponse, DeviceData, DeviceLatestData, Devices

class DeviceService:
    def get_all_devices(self) -> Devices:
        devices = []
        for device_id in devices_data.keys():
            devices.append({
                "device_id": device_id,
                "connected": connection_status.get(device_id, False)
            })
        return {
            "devices": devices,
            "total": len(devices)
        }

    def get_device_data(self, device_id: str) -> DeviceData:
        if device_id not in devices_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
        return {
            "device_id": device_id,
            "connected": connection_status.get(device_id, False),
            "data": devices_data[device_id]
        }

    async def connect_device(self, device_id: str) -> DefaultResponse:
        result = send_connect_message(device_id)
        if result == "connected":
            return {"msg": f"Dispositivo {device_id} conectado"}
        if result == "timeout":
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=f"Tempo esgotado. Dispositivo {device_id} não respondeu.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result)

    def get_latest_data(self, device_id: str) -> DeviceLatestData:
        if device_id not in devices_data or len(devices_data[device_id]) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado ou sem dados")
        latest_data = devices_data[device_id][-1].copy()
        latest_data.pop('timestamp', None)
        return {
            "device_id": device_id,
            "connected": connection_status.get(device_id, False),
            "latest_data": latest_data,
            "timestamp": devices_data[device_id][-1]["timestamp"]
        }
