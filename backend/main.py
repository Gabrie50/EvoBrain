"""EvoBrain - Sistema de Previsão 24/7 com 5 Etapas."""

import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import agents, chat, health, predict, report, stats, upload
from api.websocket import router as websocket_router
from config import settings
from data_collector.bacbo_api import BacBoDataAPI
from llm.local_llm import LocalLLM
from stage1_extraction.graph_extractor import GraphExtractor
from stage2_generation.dynamic_generator import DynamicAgentGenerator
from stage3_simulation.simulation_engine import DynamicSimulationEngine
from stage4_report.report_generator import ReportGenerator
from stage5_interaction.chat_engine import ChatEngine
from storage.checkpoint_manager import CheckpointManager
from storage.database import init_db
from utils.logger import setup_logger

logger = setup_logger()


class EvoBrain:
    def __init__(self):
        self.llm = None
        self.extractor = None
        self.generator = None
        self.simulation = None
        self.reporter = None
        self.chat_engine = None
        self.data_api = None
        self.checkpoint_manager = None
        self._initialized = False
        self._simulation_thread = None
        self._start_time = None

    def initialize(self):
        init_db()
        self.llm = LocalLLM(model=settings.LLM_MODEL, host=settings.LLM_HOST, timeout=settings.LLM_TIMEOUT)
        self.llm.connect()
        self.extractor = GraphExtractor(self.llm)
        self.generator = DynamicAgentGenerator(self.llm, max_agents=settings.MAX_AGENTS, creation_delay=settings.AGENT_CREATION_DELAY)
        self.generator.start_generation_thread()
        self.simulation = DynamicSimulationEngine(self.generator, state_size=settings.STATE_SIZE, history_size=settings.HISTORY_SIZE)
        self.reporter = ReportGenerator(self.llm)
        self.chat_engine = ChatEngine(self.generator, self.llm)
        self.data_api = BacBoDataAPI()
        self.checkpoint_manager = CheckpointManager()
        self.checkpoint_manager.load(self)
        self._initialized = True

    def start_simulation_24_7(self):
        if not self._initialized:
            raise RuntimeError("Sistema não inicializado")
        self.simulation.run_continuously(self.data_api)

    def start_background_simulation(self):
        if self._simulation_thread is None:
            self._simulation_thread = threading.Thread(target=self.start_simulation_24_7, daemon=True)
            self._simulation_thread.start()

    def process_pdf(self, pdf_content: bytes, filename: str) -> dict:
        knowledge_graph = self.extractor.extract_from_pdf(pdf_content, filename)
        for entity in knowledge_graph.get("entities", []):
            self.generator.request_agent(entity_name=entity["name"], context=entity.get("description", ""), priority=entity.get("priority", 1))
        return {"filename": filename, "entities_found": len(knowledge_graph.get("entities", [])), "relations_found": len(knowledge_graph.get("relations", [])), "agents_requested": len(knowledge_graph.get("entities", [])), "status": "processing"}

    def get_stats(self) -> dict:
        if not self._initialized:
            return {"status": "not_initialized"}
        return {"status": "running", "simulation": self.simulation.get_stats() if self.simulation else {}, "generation": self.generator.get_stats() if self.generator else {}, "llm_connected": self.llm.is_connected() if self.llm else False, "uptime": time.time() - self._start_time if self._start_time else 0}

    def get_prediction(self) -> dict:
        return self.simulation.get_current_prediction() if self.simulation else {}

    def list_agents(self) -> list:
        return [agent.to_dict() for agent in self.generator.get_all_agents()] if self.generator else []

    def chat_with_agent(self, agent_name: str, question: str) -> str:
        return self.chat_engine.chat(agent_name, question) if self.chat_engine else "Chat não disponível"

    def generate_report(self) -> str:
        return self.reporter.generate_report(self.get_stats()) if self.reporter else "Relatório não disponível"

    def stop(self):
        if self.generator:
            self.generator.stop()
        if self.simulation:
            self.simulation.stop()
        if self.checkpoint_manager:
            self.checkpoint_manager.save(self)


evobrain = EvoBrain()


@asynccontextmanager
async def lifespan(app: FastAPI):
    evobrain.initialize()
    evobrain._start_time = time.time()
    yield
    evobrain.stop()


app = FastAPI(title="EvoBrain API", description="Sistema de Previsão 24/7 com RL + Neuroevolution", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(stats.router, prefix="/api", tags=["Stats"])
app.include_router(predict.router, prefix="/api", tags=["Predict"])
app.include_router(agents.router, prefix="/api", tags=["Agents"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(report.router, prefix="/api", tags=["Report"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(websocket_router, prefix="/api", tags=["WebSocket"])


@app.get("/")
async def root():
    return {"name": "EvoBrain", "version": "1.0.0", "stages": [{"name": "Extração", "status": "active", "llm": "local"}, {"name": "Geração", "status": "active", "dynamic": True}, {"name": "Simulação", "status": "active", "engine": "RL + Neuroevolution"}, {"name": "Relatório", "status": "active", "llm": "local"}, {"name": "Interação", "status": "active", "llm": "local"}]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.API_HOST, port=settings.API_PORT, workers=settings.API_WORKERS, reload=True)
