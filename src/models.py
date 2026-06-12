from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL nao configurada no .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Animal(Base):
    __tablename__ = "animais"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    especie = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=True)
    raca = Column(String(100), nullable=True)
    observacoes = Column(Text, nullable=True)
    status = Column(String(50), default="Disponível")
    temperamento = Column(String(255), nullable=True)
    life_span = Column(String(100), nullable=True)
    peso = Column(String(100), nullable=True)
    origem = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
