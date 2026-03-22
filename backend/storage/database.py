"""
Conexão com banco de dados
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = None
        self.Session = None
        if settings.database.enabled:
            self._init_db()

    def _init_db(self):
        try:
            self.engine = create_engine(settings.database.url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("✅ Banco de dados inicializado")
        except Exception as exc:
            logger.error(f"Erro ao inicializar banco: {exc}")

    def get_session(self):
        if self.Session:
            return self.Session()
        return None


db = Database()


def init_db():
    return db
