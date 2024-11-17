import paho.mqtt.client as mqtt
import json
import time
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

BROKER = "e89dd3b4d73248a29def221deeafac4c.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "ohmni"
PASSWORD = "Ohmni2024"
TOPIC = "iot/+/data"

devices_data: Dict[str, List[Dict]] = {}
connection_status: Dict[str, bool] = {}

def send_connect_message(device_id: str):
    global connection_status
    connection_status[device_id] = False
    result = mqtt_client.publish(f"iot/{device_id}/connect", "connect", qos=1)
    print(f"Mensagem de conexão enviada para {device_id}, resultado: {result}")

    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        start_time = time.time()
        while time.time() - start_time < 5:
            if connection_status.get(device_id, False):
                print(f"Dispositivo {device_id} conectado com sucesso!")
                return "connected"
            time.sleep(0.1)
        print(f"Tempo esgotado. Dispositivo {device_id} não respondeu.")
        connection_status[device_id] = False
        return "timeout"
    else:
        return f"Erro ao conectar dispositivo {device_id} ao Broker MQTT"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conectado ao Broker MQTT!")
        client.subscribe(TOPIC)
        client.subscribe("iot/+/connect")
    else:
        print(f"Erro ao conectar ao Broker MQTT: Código {rc}")

def on_message(client, userdata, msg, properties=None):
    print(f"Mensagem recebida no tópico {msg.topic}")
    try:
        payload = msg.payload.decode()
        if msg.topic.endswith("/connect") and payload == "Conectado!":
            device_id = msg.topic.split("/")[1]
            print(f"Confirmação recebida para o dispositivo {device_id}")
            connection_status[device_id] = True
        else:
            payload = json.loads(payload)
            device_id = payload["id"]
            corrente = payload["corrente"]
            tensao = payload["tensao"]
            timestamp = datetime.utcnow()

            if device_id not in devices_data:
                devices_data[device_id] = []

            devices_data[device_id].append({
                "corrente": corrente,
                "tensao": tensao,
                "timestamp": timestamp.isoformat()
            })

            print(f"Dados armazenados para o dispositivo {device_id}: {payload}")

    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")


mqtt_client = mqtt.Client(transport="tcp", protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.tls_set()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_start()
    print("Loop MQTT iniciado")
except Exception as e:
    print(f"Erro ao conectar ao broker MQTT: {e}")
    raise