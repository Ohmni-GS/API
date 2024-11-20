import asyncio
from fastapi import HTTPException, status
from app.db.models import DeviceDataModel, DeviceModel
from app.utils.mqtt_client import publish_disconnect_message, send_connect_message, update_connection_status
from app.schemas import AllDeviceData, DefaultResponse, Device, DeviceData, Devices
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from psycopg2.errors import ForeignKeyViolation

class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_devices(self) -> Devices:
        devices = self.db.query(DeviceModel).all()
        return {
            "devices": [{"device_id": d.id, "connected": d.connected} for d in devices] if devices else [],
            "total": len(devices),
        }
    
    def add_device(self, device: Device) -> Device:
        existing_device = self.db.query(DeviceModel).filter(DeviceModel.id == device.id).first()
        if existing_device:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dispositivo {device.id} já cadastrado."
            )

        db_device = DeviceModel(
            id=device.id,
            name=device.name,
            owner=device.owner,
            type=device.type,
            is_collective=device.is_collective,
            connected=False,
            last_seen=0,
        )
        try:
            self.db.add(db_device)
            self.db.commit()
            self.db.refresh(db_device)
            print(f"Dispositivo {device.id} adicionado com sucesso.")
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.orig.diag.message_detail
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao adicionar dispositivo: {str(e)}"
            )

        return DefaultResponse(msg="Dispositivo adicionado com sucesso")

    
    def get_device_data(self, device_id: str) -> AllDeviceData:
        device = self.db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
        
        try:
            data = self.db.query(DeviceDataModel).filter(DeviceDataModel.device_id == device_id).all()
        except IntegrityError as e:
            if isinstance(e.orig, ForeignKeyViolation):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Erro de chave estrangeira ao buscar dados do dispositivo"
                )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao buscar dados do dispositivo"
            )

        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sem dados disponíveis para o dispositivo")
        
        return {
            "device_id": device_id,
            "connected": device.connected,
            "name": device.name,
            "owner": device.owner,
            "type": device.type,
            "is_collective": device.is_collective,
            "data": [{"corrente": d.corrente, "tensao": d.tensao, "timestamp": d.timestamp} for d in data],
            "total": len(data),
        }
    
    def get_latest_data(self, device_id: str) -> DeviceData:
        device = self.db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado")
        
        latest_data = (
            self.db.query(DeviceDataModel)
            .filter(DeviceDataModel.device_id == device_id)
            .order_by(DeviceDataModel.timestamp.desc())
            .first()
        )
        if not latest_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sem dados recentes para o dispositivo")
        
        return {
            "id": latest_data.id,
            "device_id": device_id,
            "connected": device.connected,
            "corrente": latest_data.corrente,
            "tensao": latest_data.tensao,
            "timestamp": latest_data.timestamp,
        }
    

    def delete_device(self, device_id: str) -> DefaultResponse:
        device = self.db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado"
            )
        try:
            self.db.delete(device)
            self.db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao excluir dispositivo: {str(e)}",
            )
        
        return DefaultResponse(msg="Dispositivo excluído com sucesso")
    
    async def connect_device(self, device_id: str) -> DefaultResponse:
        device = self.db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dispositivo {device_id} não encontrado."
            )
        update_connection_status(self.db, device_id, connected=False)

        try:
            result = await asyncio.get_running_loop().run_in_executor(
                None, send_connect_message, self.db, device_id
            )

            if result == "connected":
                update_connection_status(self.db, device_id, connected=True)
                return {"msg": f"Dispositivo {device_id} conectado com sucesso!"}

            if result == "timeout":
                raise HTTPException(
                    status_code=status.HTTP_408_REQUEST_TIMEOUT,
                    detail=f"Tempo esgotado ao conectar o dispositivo {device_id}."
                )

        except Exception as e:
            print(f"Erro ao conectar o dispositivo {device_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao conectar dispositivo: {e}"
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro desconhecido ao conectar dispositivo."
        )

    async def disconnect_device(self, device_id: str) -> DefaultResponse:
        device = self.db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo não encontrado"
            )
        device.connected = False
        try:
            self.db.commit()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao desconectar dispositivo: {str(e)}",
            )
        try:
            print(f"Publicando desconexão para {device_id}")
            await publish_disconnect_message(device_id)
        except Exception as e:
            print(f"Erro ao publicar desconexão no MQTT: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao publicar desconexão no MQTT: {e}"
            )

        return DefaultResponse(msg="Dispositivo desconectado com sucesso")
