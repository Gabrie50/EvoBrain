"""
Conexão com banco de dados PostgreSQL
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

import asyncpg
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

Base = declarative_base()


class Rodada(Base):
    """Modelo de rodada"""
    __tablename__ = 'rodadas'
    
    id = Column(String, primary_key=True)
    data_hora = Column(DateTime)
    player_score = Column(Integer)
    banker_score = Column(Integer)
    resultado = Column(String)
    fonte = Column(String)
    dados_json = Column(JSON)


class Previsao(Base):
    """Modelo de previsão"""
    __tablename__ = 'historico_previsoes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, default=datetime.now)
    previsao = Column(String)
    simbolo = Column(String)
    confianca = Column(Integer)
    resultado_real = Column(String)
    acertou = Column(Boolean)
    modo = Column(String)
    indice_confianca = Column(Integer, default=50)


class AgenteNeuro(Base):
    """Modelo de agente neuroevolução"""
    __tablename__ = 'neuroevolucao_agentes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agente_nome = Column(String)
    geracao = Column(Integer)
    dna_json = Column(JSON)
    especialidades = Column(JSON)
    fitness = Column(Float)
    created_at = Column(DateTime, default=datetime.now)


class Database:
    """Gerenciador do banco de dados"""
    
    def __init__(self):
        self.engine = None
        self.Session = None
        self.pool = None
        
        if settings.DATABASE_URL:
            self._init_sqlalchemy()
    
    def _init_sqlalchemy(self):
        """Inicializa SQLAlchemy"""
        try:
            self.engine = create_engine(settings.DATABASE_URL)
            self.Session = sessionmaker(bind=self.engine)
            
            # Cria tabelas
            Base.metadata.create_all(self.engine)
            logger.info("✅ Banco de dados inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar banco: {e}")
    
    async def init_asyncpg(self):
        """Inicializa asyncpg para operações assíncronas"""
        if settings.DATABASE_URL:
            try:
                self.pool = await asyncpg.create_pool(settings.DATABASE_URL)
                logger.info("✅ Pool asyncpg criado")
            except Exception as e:
                logger.error(f"Erro ao criar pool: {e}")
    
    def save_rodada(self, rodada: Dict) -> bool:
        """Salva uma rodada no banco"""
        if not self.Session:
            return False
        
        session = self.Session()
        try:
            existing = session.query(Rodada).filter_by(id=rodada['id']).first()
            if existing:
                return False
            
            nova_rodada = Rodada(
                id=rodada['id'],
                data_hora=rodada.get('timestamp', datetime.now()),
                player_score=rodada['player_score'],
                banker_score=rodada['banker_score'],
                resultado=rodada['resultado'],
                fonte=rodada.get('source', 'api'),
                dados_json=rodada
            )
            session.add(nova_rodada)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar rodada: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def save_previsao(self, previsao: Dict, resultado: str, acertou: bool) -> bool:
        """Salva uma previsão no banco"""
        if not self.Session:
            return False
        
        session = self.Session()
        try:
            nova_previsao = Previsao(
                previsao=previsao.get('prediction', previsao.get('previsao')),
                simbolo=previsao.get('simbolo', '🔴'),
                confianca=int(previsao.get('confidence', 50)),
                resultado_real=resultado,
                acertou=acertou,
                modo=previsao.get('modo', 'RL'),
                indice_confianca=previsao.get('indice_confianca', 50)
            )
            session.add(nova_previsao)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar previsão: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def save_agente_neuro(self, nome: str, geracao: int, dna: Dict, fitness: float) -> bool:
        """Salva agente neuroevolução"""
        if not self.Session:
            return False
        
        session = self.Session()
        try:
            agente = AgenteNeuro(
                agente_nome=nome,
                geracao=geracao,
                dna_json=dna,
                fitness=fitness
            )
            session.add(agente)
            session.commit()
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar agente: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    def get_ultimas_rodadas(self, limit: int = 50) -> List[Dict]:
        """Retorna últimas rodadas"""
        if not self.Session:
            return []
        
        session = self.Session()
        try:
            rodadas = session.query(Rodada).order_by(Rodada.data_hora.desc()).limit(limit).all()
            return [
                {
                    'id': r.id,
                    'resultado': r.resultado,
                    'player_score': r.player_score,
                    'banker_score': r.banker_score,
                    'timestamp': r.data_hora.isoformat()
                }
                for r in rodadas
            ]
        except Exception as e:
            logger.error(f"Erro ao buscar rodadas: {e}")
            return []
        finally:
            session.close()
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do banco"""
        if not self.Session:
            return {}
        
        session = self.Session()
        try:
            total_rodadas = session.query(Rodada).count()
            total_previsoes = session.query(Previsao).count()
            acertos = session.query(Previsao).filter_by(acertou=True).count()
            
            return {
                'total_rodadas': total_rodadas,
                'total_previsoes': total_previsoes,
                'acertos': acertos,
                'precisao': (acertos / total_previsoes * 100) if total_previsoes > 0 else 0
            }
        except Exception as e:
            logger.error(f"Erro ao buscar stats: {e}")
            return {}
        finally:
            session.close()


# Instância global
db = Database()


def init_db():
    """Inicializa banco de dados"""
    db._init_sqlalchemy()
    return db
