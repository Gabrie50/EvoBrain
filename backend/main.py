"""
EvoBrain - Sistema Principal Completo
"""

import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import agents, chat, config, health, predict, report, stats, upload
from config import settings
from data_collector.factory import create_data_collector
from llm.factory import create_llm
from stage1_extraction.continuous_learning import ContinuousLearning
from stage1_extraction.graph_extractor import GraphExtractor
from stage2_generation.dynamic_generator import DynamicAgentGenerator
from stage3_simulation.agent_competition import AgentCompetition
from stage3_simulation.evolutionary_memory import EvolutionaryMemory
from stage3_simulation.memory_ranking import MemoryRanker
from stage3_simulation.prioritized_replay import PrioritizedReplayBuffer
from stage3_simulation.simulation_engine import DynamicSimulationEngine
from stage4_report.report_generator import ReportGenerator
from stage5_interaction.chat_engine import ChatEngine
from storage.checkpoint_manager import CheckpointManager
from storage.database import init_db
from storage.knowledge_base import KnowledgeBase
from utils.logger import get_logger

logger = get_logger(__name__)


class EvoBrain:
    def __init__(self):
        self.llm = None
        self.extractor = None
        self.generator = None
        self.simulation = None
        self.reporter = None
        self.chat_engine = None
        self.data_collector = None
        self.checkpoint_manager = None
        self.knowledge_base = None
        self.replay_buffer = None
        self.memory_ranker = None
        self.evolutionary_memory = None
        self.agent_competition = None
        self.continuous_learning = None
        self._initialized = False
        self._simulation_thread = None
        self._evolution_thread = None
        self._start_time = None

    def initialize(self):
        logger.info("=" * 60)
        logger.info("🧠 EVOBRAIN - Inicializando Sistema Completo")
        logger.info(f"   Domínio: {settings.domain.name}")
        logger.info(f"   LLM: {settings.llm.type} ({settings.llm.model})")
        logger.info("=" * 60)

        init_db()
        self.llm = create_llm()
        if self.llm:
            self.llm.connect()

        self.knowledge_base = KnowledgeBase()
        self.extractor = GraphExtractor(self.llm)
        self.generator = DynamicAgentGenerator(self.llm, settings.agents.max_agents)
        self.generator.start_generation_thread()
        self.simulation = DynamicSimulationEngine(self.generator)
        self.replay_buffer = PrioritizedReplayBuffer(settings.replay.capacity)
        self.memory_ranker = MemoryRanker()
        self.evolutionary_memory = EvolutionaryMemory(self.memory_ranker)
        self.agent_competition = AgentCompetition(self.memory_ranker)
        self.reporter = ReportGenerator(self.llm)
        self.chat_engine = ChatEngine(self.generator, self.llm)
        self.data_collector = create_data_collector()
        self.continuous_learning = ContinuousLearning(self.extractor, self.generator, self.simulation, self.knowledge_base)
        self.checkpoint_manager = CheckpointManager()
        self.checkpoint_manager.load(self)

        self._initialized = True
        logger.info("✅ EvoBrain inicializado com sucesso!")

    def start(self):
        if not self._initialized:
            raise Exception("Sistema não inicializado")
        if self.data_collector:
            self._simulation_thread = threading.Thread(
                target=self.simulation.run_continuously,
                args=(self.data_collector,),
                daemon=True,
            )
            self._simulation_thread.start()
        if settings.continuous_learning.enabled:
            self.continuous_learning.start()
        self._evolution_thread = threading.Thread(target=self._evolution_loop, daemon=True)
        self._evolution_thread.start()
        self._start_time = time.time()

    def _evolution_loop(self):
        while True:
            time.sleep(3600)
            try:
                agents = list(self.simulation.rl_agents.values())
                if len(agents) < 10:
                    continue
                survivors = self.agent_competition.tournament(agents, rounds=settings.competition.tournament_rounds)
                strong = self.agent_competition.eliminate_weak(survivors, keep_ratio=settings.competition.keep_ratio)
                evolved = self.evolutionary_memory.evolve_generation(
                    strong,
                    keep_best=10,
                    offspring_count=max(0, len(agents) - 10),
                )
                self.simulation.rl_agents = {agent.profile.name: agent for agent in evolved}
                self.checkpoint_manager.save(self)
            except Exception as exc:
                logger.error(f"Erro na evolução: {exc}")

    def process_pdf(self, pdf_content: bytes, filename: str) -> dict:
        return self.continuous_learning.process_pdf(pdf_content, filename)

    def process_text(self, text: str, source: str = "web") -> dict:
        return self.continuous_learning.process_text(text, source)

    def get_stats(self) -> dict:
        if not self._initialized:
            return {"status": "not_initialized"}
        return {
            "status": "running",
            "domain": settings.domain.name,
            "simulation": self.simulation.get_stats(),
            "generation": self.generator.get_stats(),
            "memory": {
                "replay_buffer": len(self.replay_buffer.buffer) if self.replay_buffer else 0,
                "knowledge_base": self.knowledge_base.get_statistics() if self.knowledge_base else {},
                "evolutionary_generation": self.evolutionary_memory.generation if self.evolutionary_memory else 0,
            },
            "uptime": time.time() - self._start_time if self._start_time else 0,
        }

    def get_prediction(self) -> dict:
        return self.simulation.get_current_prediction() if self.simulation else {}

    def list_agents(self) -> list:
        return self.generator.get_all_agents() if self.generator else []

    def chat_with_agent(self, agent_name: str, question: str) -> str:
        return self.chat_engine.chat(agent_name, question) if self.chat_engine else "Chat não disponível"

    def generate_report(self) -> str:
        return self.reporter.generate_report(self.get_stats()) if self.reporter else "Relatório não disponível"

    def stop(self):
        if self.generator:
            self.generator.stop()
        if self.simulation:
            self.simulation.stop()
        if self.continuous_learning:
            self.continuous_learning.stop()
        if self.checkpoint_manager:
            self.checkpoint_manager.save(self)


evobrain = EvoBrain()


@asynccontextmanager
async def lifespan(app: FastAPI):
    evobrain.initialize()
    evobrain.start()
    yield
    evobrain.stop()


app = FastAPI(title="EvoBrain API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(stats.router, prefix="/api", tags=["Stats"])
app.include_router(predict.router, prefix="/api", tags=["Predict"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(report.router, prefix="/api", tags=["Report"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(config.router, prefix="/api", tags=["Config"])


@app.get("/")
async def root():
    return {
        "name": "EvoBrain",
        "version": "1.0.0",
        "domain": settings.domain.name,
        "stages": [
            {"name": "Extração", "status": "active"},
            {"name": "Geração", "status": "active"},
            {"name": "Simulação", "status": "active", "engine": "RL + Neuroevolution + Memória"},
            {"name": "Relatório", "status": "active"},
            {"name": "Interação", "status": "active"},
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.api.host, port=settings.api.port, workers=settings.api.workers, reload=True)
