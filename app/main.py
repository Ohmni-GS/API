from fastapi import FastAPI, HTTPException
from app.routers.community_routes import community_router
from app.routers.user_routes import user_router
from app.routers.devices_routes import devices_router

app = FastAPI(title="Ohmni", description='API para conectar a plataforma <a href="https://github.com/Ohmni-GS">OHMNI</a>, os dispositivos de medição de energia e o Banco de Dados PostgreSQL <a href="https://github.com/Ohmni-GS/API">Link do GitHub</a><br><h2><b>Criado por <a href="https://www.linkedin.com/in/matheus-zanutin" target="_BLANK">Matheus Queiroz Zanutin</a></b></h3>', version="1.0", docs_url="/", )


app.include_router(user_router)
app.include_router(devices_router)
app.include_router(community_router)

