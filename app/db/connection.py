from sqlalchemy.exc import OperationalError
from decouple import config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_URL = config('DB_URL')

print(f"Conectando com a URL: {DB_URL}")
engine = create_engine(DB_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

try:
    with engine.connect() as connection:
        print("Conexão bem-sucedida com o banco!")
        result = connection.execute(text("SELECT NOW();"))
        print(f"Hora atual no banco: {result.fetchone()}")
except OperationalError as e:
    print(f"Erro ao conectar no banco: {e}")
