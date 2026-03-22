"""Armazenamento persistente de memórias."""

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

Base = declarative_base()


class MemoryRecord(Base):
    __tablename__ = "agent_memories"
    id = Column(String, primary_key=True)
    agent_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    memory_type = Column(String, nullable=False)
    importance = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    related_agents = Column(JSON, default=list)
    access_count = Column(Integer, default=0)
    last_accessed = Column(DateTime)
    consolidation_strength = Column(Float, default=0.5)


class RelationshipRecord(Base):
    __tablename__ = "agent_relationships"
    id = Column(String, primary_key=True)
    agent_a = Column(Integer, nullable=False)
    agent_b = Column(Integer, nullable=False)
    affinity = Column(Float, default=0.5)
    interaction_count = Column(Integer, default=0)
    last_interaction = Column(DateTime)
    interaction_history = Column(JSON, default=list)


class MemoryStore:
    def __init__(self):
        self.engine = None
        self.Session = None
        if settings.database.enabled and settings.database.url:
            self._init_db()

    def _init_db(self):
        try:
            self.engine = create_engine(settings.database.url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("✅ MemoryStore inicializado")
        except Exception as exc:
            logger.error(f"Erro ao inicializar MemoryStore: {exc}")

    def save_memory(self, memory: dict) -> bool:
        if not self.Session:
            return False
        session = self.Session()
        try:
            record = MemoryRecord(
                id=memory["id"],
                agent_id=memory["agent_id"],
                content=memory["content"],
                memory_type=memory["memory_type"],
                importance=memory["importance"],
                timestamp=datetime.fromtimestamp(memory["timestamp"]),
                related_agents=memory.get("related_agents", []),
                access_count=memory.get("access_count", 0),
                last_accessed=datetime.fromtimestamp(memory["last_accessed"]) if memory.get("last_accessed") else None,
                consolidation_strength=memory.get("consolidation_strength", 0.5),
            )
            session.merge(record)
            session.commit()
            return True
        except Exception as exc:
            logger.error(f"Erro ao salvar memória: {exc}")
            session.rollback()
            return False
        finally:
            session.close()

    def load_memories(self, agent_id: int, limit: int = 1000) -> List[dict]:
        if not self.Session:
            return []
        session = self.Session()
        try:
            records = (
                session.query(MemoryRecord)
                .filter(MemoryRecord.agent_id == agent_id)
                .order_by(MemoryRecord.timestamp.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": record.id,
                    "agent_id": record.agent_id,
                    "content": record.content,
                    "memory_type": record.memory_type,
                    "importance": record.importance,
                    "timestamp": record.timestamp.timestamp(),
                    "related_agents": record.related_agents,
                    "access_count": record.access_count,
                    "last_accessed": record.last_accessed.timestamp() if record.last_accessed else 0,
                    "consolidation_strength": record.consolidation_strength,
                }
                for record in records
            ]
        except Exception as exc:
            logger.error(f"Erro ao carregar memórias: {exc}")
            return []
        finally:
            session.close()
