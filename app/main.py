import asyncio
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.mqtt_client import connection_status, connection_status_lock
from app.routers.community_routes import community_router
from app.routers.user_routes import user_router
from app.routers.devices_routes import devices_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def check_inactive_devices():
        timeout = 15
        while True:
            print("Verificando dispositivos inativos...")
            current_time = time.time()
            with connection_status_lock:
                for device_id, status in list(connection_status.items()):
                    if status.get("connected") and (current_time - status.get("last_seen", 0) > timeout):
                        connection_status[device_id]["connected"] = False
                        print(f"Dispositivo {device_id} desconectado por inatividade.")
            await asyncio.sleep(10)
    task = asyncio.create_task(check_inactive_devices())
    try:
        yield
    finally:
        task.cancel()
        await task

app = FastAPI(
    title="Ohmni",
    description='API para conectar a plataforma <a href="https://github.com/Ohmni-GS">OHMNI</a>, os dispositivos de medição de energia e o Banco de Dados PostgreSQL <a href="https://github.com/Ohmni-GS/API">Link do GitHub</a><br><h2><b>Criado por <a href="https://www.linkedin.com/in/matheus-zanutin" target="_BLANK">Matheus Queiroz Zanutin</a></b></h3>',
    version="1.0",
    docs_url="/",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Origens permitidas
    allow_credentials=True,  # Permitir envio de cookies e cabeçalhos de autenticação
    allow_methods=["*"],  # Métodos HTTP permitidos (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Cabeçalhos permitidos
)

app.include_router(user_router)
app.include_router(devices_router)
app.include_router(community_router)
