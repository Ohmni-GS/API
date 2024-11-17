from fastapi import FastAPI, HTTPException
from app.mqtt_client import mqtt_client, devices_data, connection_status, send_connect_message

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API para dados de dispositivos IoT"}

@app.get("/devices")
def get_all_devices():
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


@app.get("/devices/{device_id}")
def get_device_data(device_id: str):
    if device_id not in devices_data:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return {
        "device_id": device_id,
        "connected": connection_status.get(device_id, False),
        "data": devices_data[device_id]
    }


@app.get("/devices/{device_id}/connect")
async def connect_device(device_id: str):
    result = send_connect_message(device_id)
    if result == "connected":
        return {"message": f"Dispositivo {device_id} conectado com sucesso!"}
    if result == "timeout":
        raise HTTPException(status_code=408, detail=f"Tempo esgotado. Dispositivo {device_id} não respondeu.")
    raise HTTPException(status_code=500, detail=result)

@app.get("/devices/{device_id}/latest")
def get_latest_device_data(device_id: str):
    if device_id not in devices_data or len(devices_data[device_id]) == 0:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado ou sem dados")
    return {
        "device_id": device_id,
        "connected": connection_status.get(device_id, False),
        "latest_data": devices_data[device_id][-1]
    }
    

