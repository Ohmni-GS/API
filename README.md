# OHMNI - Plataforma de Gerenciamento Energético Sustentável  

## Índice  
1. [Descrição do Projeto](#descrição-do-projeto)  
2. [Por que Criamos essa API?](#por-que-criamos-essa-api)  
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)  
4. [Configuração e Uso](#configuração-e-uso)  
   - [Pré-requisitos](#pré-requisitos)  
   - [Clonando o Repositório](#clonando-o-repositório)  
   - [Instalando Dependências](#instalando-dependências)  
   - [Configurando o Banco de Dados](#configurando-o-banco-de-dados)  
   - [Configurando o Arquivo .env](#configurando-o-arquivo-env)  
   - [Executando a API](#executando-a-api)  
   - [Acessando a Documentação](#acessando-a-documentação)  
5. [Sobre os Desenvolvedores](#sobre-os-desenvolvedores)  

---

## Descrição do Projeto  
**OHMNI** é um ecossistema inovador que busca otimizar o gerenciamento de placas solares e o consumo energético de comunidades remotas ou carentes.  

Por meio de uma plataforma Web integrada a um dispositivo IoT, os usuários podem monitorar o consumo energético de maneira centralizada, tanto para comunidades inteiras quanto para moradores individuais. Isso promove o uso eficiente de energia sustentável e facilita o acesso a essa tecnologia em regiões vulneráveis.  

Nosso objetivo é promover soluções sustentáveis e acessíveis, unindo inovação e impacto social.    

---

## Por que Criamos essa API?  
Essa API foi projetada para conectar o [dispositivo de medição de energia](https://github.com/Ohmni-GS/IoT) ao sistema Web [OHMNI](https://github.com/Ohmni-GS/Web-dev).  

Ela fornece suporte para:  
- Integração com um banco de dados PostgreSQL que armazena usuários, comunidades, dispositivos e dados coletados.  
- Processamento de informações em tempo real, utilizando bibliotecas como **FastAPI**, **Alembic**, **Uvicorn** e **Paho-MQTT**.  

---

## Tecnologias Utilizadas  
- **Python** 
- **JWT** 
- **FastAPI**  
- **Alembic**  
- **Uvicorn**  
- **Paho-MQTT**  
- **Docker**  
- **PostgreSQL**  

---

## Configuração e Uso  

### Pré-requisitos  
- Python 3.9 ou superior  
- Docker e Docker Compose instalados  
- Git instalado  

---

### Clonando o Repositório  
Para clonar o repositório localmente, use:  
```bash
git clone https://github.com/Ohmni-GS/API.git
```  

---

### Instalando Dependências  
Após clonar o repositório, entre na pasta do projeto e instale as dependências:  
```bash
pip install -r requirements.txt
```  

---

### Configurando o Banco de Dados  

#### 1. Configurar o Docker  
Certifique-se de que o Docker esteja instalado e configurado em sua máquina.  

#### 2. Iniciar o Banco de Dados  
No diretório raiz do projeto, use o Docker Compose para montar o banco de dados:  
```bash
docker-compose up -d
```  

---

### Configurando o Arquivo `.env`  
Crie um arquivo chamado `.env` na raiz do projeto e configure-o conforme o modelo abaixo:  

```plaintext
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=main
DB_URL="postgresql+psycopg2://localhost/main?user=admin&password=admin"
SECRET_KEY=secretkey
ALGORITHM=HS256
```  

---

### Criando Tabelas no Banco de Dados  
Use o Alembic para criar as tabelas:  
```bash
alembic upgrade head
```  

---

### Executando a API  

Inicie o servidor localmente com o Uvicorn:  
```bash
uvicorn app.main:app --reload
```  

---

### Acessando a Documentação  

- **Local**: Acesse a documentação Swagger padrão em:  
  [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- **Online**: Veja a documentação hospedada em:  
  [https://ohmni-api.onrender.com](https://ohmni-api.onrender.com)  

Na documentação, você encontrará:  
- Todos os **endpoints** da API.  
- Detalhes das **respostas**, **corpo da requisição** e tipos de métodos suportados.  

---

## Integrantes do Grupo 

- **Matheus Queiroz Zanutin** - RM558801  
- **Marcela Torro** - RM557658  
- **Matheus Vinícius** - RM555177  


