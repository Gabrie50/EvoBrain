"""Ciclo infinito de aprendizado com ingestão contínua de PDFs e texto."""

from __future__ import annotations

import hashlib
import shutil
import threading
import time
from pathlib import Path
from typing import Callable, Dict

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import settings
from stage1_extraction.graph_extractor import GraphExtractor
from stage2_generation.dynamic_generator import DynamicAgentGenerator
from stage3_simulation.simulation_engine import DynamicSimulationEngine
from storage.knowledge_base import KnowledgeBase
from utils.logger import get_logger

logger = get_logger(__name__)


class PDFHandler(FileSystemEventHandler):
    """Monitora novos PDFs na pasta de upload."""

    def __init__(self, callback: Callable[[str], None]):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            logger.info(f"📄 Novo PDF detectado: {event.src_path}")
            self.callback(event.src_path)


class ContinuousLearning:
    """Sistema de aprendizado contínuo baseado em documentos e texto."""

    def __init__(
        self,
        extractor: GraphExtractor,
        generator: DynamicAgentGenerator,
        simulation: DynamicSimulationEngine,
        knowledge_base: KnowledgeBase,
    ):
        self.extractor = extractor
        self.generator = generator
        self.simulation = simulation
        self.knowledge_base = knowledge_base
        self.processed_files: Dict[str, str] = {}
        self.observer: Observer | None = None
        self._running = False
        self._thread: threading.Thread | None = None

        self.upload_dir = Path(settings.continuous_learning.upload_dir)
        self.upload_dir.mkdir(exist_ok=True)

        self.processed_dir = self.upload_dir / "processed"
        self.processed_dir.mkdir(exist_ok=True)

        logger.info("🔄 ContinuousLearning inicializado")

    def start(self):
        if not settings.continuous_learning.enabled:
            logger.info("Aprendizado contínuo desabilitado")
            return
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
        self._process_existing_files()
        logger.info("✅ Ciclo infinito de aprendizado iniciado")

    def stop(self):
        self._running = False
        if self.observer:
            self.observer.stop()
            self.observer.join()
        logger.info("🛑 Ciclo de aprendizado parado")

    def _watch_loop(self):
        self.observer = Observer()
        self.observer.schedule(PDFHandler(self._process_new_file), str(self.upload_dir), recursive=False)
        self.observer.start()

        try:
            while self._running:
                time.sleep(settings.continuous_learning.interval)
        finally:
            if self.observer:
                self.observer.stop()
                self.observer.join()

    def _process_existing_files(self):
        for file_path in self.upload_dir.glob("*.pdf"):
            self._process_new_file(str(file_path))

    def _process_new_file(self, file_path: str):
        try:
            source_path = Path(file_path)
            with source_path.open("rb") as handle:
                file_hash = hashlib.md5(handle.read()).hexdigest()

            if self.processed_files.get(file_path) == file_hash:
                logger.debug(f"Arquivo já processado: {file_path}")
                return

            logger.info(f"📚 Processando novo documento: {file_path}")
            with source_path.open("rb") as handle:
                pdf_content = handle.read()

            knowledge = self.extractor.extract_from_pdf(pdf_content, source_path.name)
            self.knowledge_base.add_document(source_path.name, knowledge)

            new_agents = self._create_agents_from_knowledge(knowledge)
            self.processed_files[file_path] = file_hash
            destination = self.processed_dir / source_path.name
            if source_path.exists():
                shutil.move(str(source_path), destination)

            logger.info(f"✅ Documento processado: {len(new_agents)} novos agentes criados")
        except Exception as exc:
            logger.error(f"❌ Erro ao processar {file_path}: {exc}")

    def _create_agents_from_knowledge(self, knowledge: Dict) -> list[str]:
        new_agents: list[str] = []
        for entity in knowledge.get("entities", []):
            agent_name = self.generator.request_agent(
                entity_name=entity["name"],
                context=entity.get("description", ""),
                priority=2,
            )
            if agent_name:
                new_agents.append(agent_name)
                if hasattr(self.simulation, "add_agent_to_simulation"):
                    self.simulation.add_agent_to_simulation(agent_name)
        return new_agents

    def process_pdf(self, pdf_content: bytes, filename: str) -> dict:
        logger.info(f"📄 Processando PDF: {filename}")
        knowledge = self.extractor.extract_from_pdf(pdf_content, filename)
        self.knowledge_base.add_document(filename, knowledge)
        new_agents = self._create_agents_from_knowledge(knowledge)
        return {
            "filename": filename,
            "entities_found": len(knowledge.get("entities", [])),
            "relations_found": len(knowledge.get("relations", [])),
            "new_agents": len(new_agents),
            "status": "processed",
        }

    def process_text(self, text: str, source: str = "web") -> dict:
        logger.info(f"📝 Processando texto de {source}: {len(text)} caracteres")
        knowledge = self.extractor.extract_from_text(text)
        self.knowledge_base.add_text(source, knowledge, text)
        new_agents = self._create_agents_from_knowledge(knowledge)
        return {
            "source": source,
            "entities_found": len(knowledge.get("entities", [])),
            "relations_found": len(knowledge.get("relations", [])),
            "new_agents": len(new_agents),
            "text_length": len(text),
        }

    def get_statistics(self) -> dict:
        return {
            "processed_files": len(self.processed_files),
            "upload_dir": str(self.upload_dir),
            "running": self._running,
            "knowledge_base_size": self.knowledge_base.get_size() if self.knowledge_base else 0,
        }
