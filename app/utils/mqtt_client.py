import asyncio
import threading
from collections import deque
import paho.mqtt.client as mqtt
import json
import time
from typing import Dict
from datetime import datetime, timezone
from app.db.models import DeviceDataModel, DeviceModel
from app.depends import get_db_session
from app.schemas import MqttPayload
from sqlalchemy.orm import Session

BROKER = "e89dd3b4d73248a29def221deeafac4c.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "ohmni"
PASSWORD = "Ohmni2024"
TOPIC = "iot/+/data"

devices_data: Dict[str, deque] = {}
connection_status: Dict[str, Dict[str, float]] = {}
connection_events: Dict[str, threading.Event] = {}

devices_data_lock = threading.Lock()
connection_status_lock = threading.Lock()

async def publish_disconnect_message(device_id: str):
    try:
        result = await asyncio.to_thread(mqtt_client.publish, f"iot/{device_id}/connect", "disconnect", qos=1)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise Exception(f"Erro ao publicar mensagem MQTT: Código {result.rc}")
        print(f"Mensagem de desconexão enviada para {device_id}, resultado: {result}")
    except Exception as e:
        print(f"Erro ao publicar mensagem de disconexão: {e}")
        raise

def store_device_data(db: Session, device_id: str, data: Dict):
    try:
        device = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            device = DeviceModel(id=device_id, connected=True, last_seen=time.time())
            db.add(device)

        device_data = DeviceDataModel(
            id=f"{device_id}-{int(time.time())}",
            device_id=device_id,
            corrente=data["corrente"],
            tensao=data["tensao"],
            timestamp=datetime.now(timezone.utc)
        )
        db.add(device_data)
        db.commit()
        print(f"Dados armazenados para {device_id}: {data}")
    except Exception as e:
        db.rollback()
        print(f"Erro ao salvar dados para {device_id}: {e}")
        raise

def update_connection_status(db: Session, device_id: str, connected: bool, last_seen: float = 0):
    try:
        device = db.query(DeviceModel).filter(DeviceModel.id == device_id).first()
        if not device:
            device = DeviceModel(id=device_id, connected=connected, last_seen=last_seen)
            db.add(device)
        else:
            device.connected = connected
            device.last_seen = last_seen
        db.commit()
        print(f"Estado atualizado para {device_id}: conectado={connected}, visto={last_seen}")
    except Exception as e:
        db.rollback()
        print(f"Erro ao atualizar estado do dispositivo {device_id}: {e}")
        raise

def on_message_handler(db: Session, msg):
    try:
        payload = msg.payload.decode().strip()
        if not payload:
            return

        if msg.topic.endswith("/connect"):
            device_id = msg.topic.split("/")[1]
            update_connection_status(db, device_id, connected=True, last_seen=time.time())
            
            if device_id in connection_events:
                connection_events[device_id].set()
        else:
            payload_dict = json.loads(payload)
            store_device_data(
                db,
                device_id=payload_dict["id"],
                data={
                    "corrente": payload_dict["corrente"],
                    "tensao": payload_dict["tensao"],
                },
            )
            update_connection_status(db, payload_dict["id"], connected=True, last_seen=time.time())
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")


def callbackMQTT(client, userdata, msg):
    db_gen = get_db_session()
    db = next(db_gen)
    try:
        on_message_handler(db, msg)
    finally:
        next(db_gen, None)



def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conectado ao Broker MQTT!")
        client.subscribe(TOPIC)
        client.subscribe("iot/+/connect")
    else:
        print(f"Erro ao conectar ao Broker MQTT: Código {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    if rc != 0:
        print("Desconectado do broker MQTT. Tentando reconectar...")
        while True:
            try:
                client.reconnect()
                print("Reconectado ao broker MQTT!")
                break
            except Exception as e:
                print(f"Erro ao reconectar: {e}")
                time.sleep(5)

def send_connect_message(db: Session, device_id: str, timeout: int = 10):
    update_connection_status(db, device_id, connected=False)
    if device_id not in connection_events:
        connection_events[device_id] = threading.Event()
    else:
        connection_events[device_id].clear()

    try:
        result = mqtt_client.publish(f"iot/{device_id}/connect", "connect", qos=1)
        print(f"Mensagem de conexão enviada para {device_id}, resultado: {result}")
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            return f"Erro ao publicar mensagem MQTT: Código {result.rc}"
    except Exception as e:
        print(f"Erro ao publicar mensagem MQTT: {e}")
        return f"Erro ao conectar dispositivo {device_id} ao Broker MQTT: {e}"
    event_triggered = connection_events[device_id].wait(timeout)
    if event_triggered:
        print(f"Dispositivo {device_id} conectado com sucesso!")
        return "connected"
    
    print(f"Tempo esgotado. Dispositivo {device_id} não respondeu.")
    update_connection_status(db, device_id, connected=False)
    return "timeout"

def start_mqtt():
    try:
        mqtt_client.connect(BROKER, PORT, 60)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"Erro ao conectar ao broker MQTT: {e}")
        raise

mqtt_client = mqtt.Client(transport="tcp", protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.tls_set()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = callbackMQTT
mqtt_client.on_disconnect = on_disconnect

mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

print("Loop MQTT iniciado")
