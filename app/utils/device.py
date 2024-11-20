from fastapi import HTTPException, status
from app.utils.mqtt_client import mqtt_client, devices_data, connection_status, send_connect_message, devices_data_lock, connection_status_lock
from app.schemas import DefaultResponse, DeviceData, DeviceLatestData, Devices

import asyncio

class DeviceService:
    def get_all_devices(self) -> Devices:
        with connection_status_lock:
            devices = []
            for device_id, status in connection_status.items():
                devices.append({
                    "device_id": device_id,
                    "connected": status["connected"]
                })
        return {
            "devices": devices,
            "total": len(devices)
        }
    
    def get_device_data(self, device_id: str) -> DeviceData:
        with devices_data_lock:
            print(f"Dados armazenados no servidor: {devices_data}")
            if device_id not in devices_data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
            data = list(devices_data[device_id])
            if not data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo encontrado, mas sem dados.")
        
        print(f"Consultando dados do dispositivo {device_id}: {data}")
        return {
            "device_id": device_id,
            "connected": connection_status.get(device_id, {}).get("connected", False),
            "data": data
        }

    async def connect_device(self, device_id: str) -> DefaultResponse:
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, send_connect_message, device_id)
        if result == "connected":
            return {"msg": f"Dispositivo {device_id} conectado"}
        if result == "timeout":
            raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=f"Tempo esgotado. Dispositivo {device_id} não respondeu.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result)

    def get_latest_data(self, device_id: str) -> DeviceLatestData:
        with devices_data_lock:
            if device_id not in devices_data or len(devices_data[device_id]) == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado ou sem dados")
            latest_data = devices_data[device_id][-1].copy()
        latest_data.pop('timestamp', None)
        return {
            "device_id": device_id,
            "connected": connection_status.get(device_id, {}).get("connected", False),
            "latest_data": latest_data,
            "timestamp": devices_data[device_id][-1]["timestamp"]
        }
