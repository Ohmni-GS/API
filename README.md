# TODO
- Melhorar a lógica de dispositivo conectado
- Atualizar os schemas para os devices e devices_data terem id
- Implementar salvamento no Banco de Dados (já funciona: usuários, comunidades)
- Criar chaves estrangeiras do db
- Fazer documentação de Python e Edge
- Gravar vídeo de explicação Python e Edge

# API - OHMNI

## Modelo de ```.env```:

```POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=main
DB_URL="postgresql+psycopg2://localhost/main?user=admin&password=admin"
SECRET_KEY=secretkey
ALGORITHM=HS256```