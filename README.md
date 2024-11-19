# TODO
- Melhorar a lógica de dispositivo conectado
- Implementar rota de verificar tokens e form do usuário igual do login no cadastro
- Criar rotas de criação/edição/exclusão de usuários
- Implementar salvamento no Banco de Dados
- Atualizar os schemas para os devices e devices_data terem id
- Criar rotas de criação/edição/exclusão de comunidades
- Fazer documentação de Python e Edge
- Gravar vídeo de explicação Python e Edge

## Modelo de ```.env```:

```POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=main
DB_URL="postgresql+psycopg2://localhost/main?user=admin&password=admin"
SECRET_KEY=secretkey
ALGORITHM=HS256```