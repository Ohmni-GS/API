import threading
from collections import deque
import paho.mqtt.client as mqtt
import json
import time
from typing import Dict
from datetime import datetime, timezone
from app.schemas import MqttPayload

BROKER = "e89dd3b4d73248a29def221deeafac4c.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "ohmni"
PASSWORD = "Ohmni2024"
TOPIC = "iot/+/data"

devices_data: Dict[str, deque] = {}
connection_status: Dict[str, Dict[str, float]] = {}

devices_data_lock = threading.Lock()
connection_status_lock = threading.Lock()

def store_device_data(device_id: str, data: Dict, max_size=100):
    with devices_data_lock:
        if device_id not in devices_data:
            devices_data[device_id] = deque(maxlen=max_size)
        devices_data[device_id].append(data)
    print(f"Dados armazenados para {device_id}: {data}")

def update_connection_status(device_id: str, connected: bool, last_seen: float = 0):
    with connection_status_lock:
        connection_status[device_id] = {"connected": connected, "last_seen": last_seen}
        print(f"Estado atualizado para {device_id}: {connection_status[device_id]}")

def on_message_handler(msg):
    try:
        print(f"Mensagem recebida no tópico {msg.topic}")
        payload = msg.payload.decode().strip()
        if not payload:
            print(f"Payload vazio recebido no tópico {msg.topic}")
            return

        if msg.topic.endswith("/connect"):
            if payload == "Conectado!":
                device_id = msg.topic.split("/")[1]
                print(f"Confirmação recebida para o dispositivo {device_id}")
                update_connection_status(device_id, connected=True, last_seen=time.time())
            else:
                print(f"Payload inválido no tópico /connect: {payload}")
        else:
            payload_dict = json.loads(payload)
            print(f"Processando dados para o tópico {msg.topic}: {payload_dict}")
            store_device_data(
                device_id=payload_dict["id"],
                data={
                    "corrente": payload_dict["corrente"],
                    "tensao": payload_dict["tensao"],
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
            update_connection_status(payload_dict["id"], connected=True, last_seen=time.time())
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

def callbackMQTT(client, userdata, msg):
    on_message_handler(msg)

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

def send_connect_message(device_id: str, timeout: int = 5):
    update_connection_status(device_id, connected=False, last_seen=0)
    try:
        result = mqtt_client.publish(f"iot/{device_id}/connect", "connect", qos=1)
        print(f"Mensagem de conexão enviada para {device_id}, resultado: {result}")
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            return f"Erro ao publicar mensagem MQTT: Código {result.rc}"
    except Exception as e:
        print(f"Erro ao publicar mensagem MQTT: {e}")
        return f"Erro ao conectar dispositivo {device_id} ao Broker MQTT: {e}"

    start_time = time.time()
    while time.time() - start_time < timeout:
        with connection_status_lock:
            status = connection_status.get(device_id, {"connected": False, "last_seen": 0})
            if status["connected"]:
                print(f"Dispositivo {device_id} conectado com sucesso!")
                return "connected"
        time.sleep(0.5)
    print(f"Tempo esgotado. Dispositivo {device_id} não respondeu.")
    update_connection_status(device_id, connected=False)
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
