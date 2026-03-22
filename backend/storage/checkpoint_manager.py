"""
Gerenciador de checkpoints
"""

import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Any

import torch

from utils.logger import get_logger

logger = get_logger(__name__)


class CheckpointManager:
    def __init__(self, checkpoint_dir: str = "storage/checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"💾 CheckpointManager: {self.checkpoint_dir}")

    def save(self, system: Any) -> bool:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if hasattr(system, "generator"):
                self._save_generator(system.generator, timestamp)
            if hasattr(system, "simulation"):
                self._save_simulation(system.simulation, timestamp)
            if hasattr(system, "evolutionary_memory"):
                self._save_neuroevolution(system.evolutionary_memory, timestamp)
            self._save_metadata({"timestamp": timestamp, "version": "1.0.0"}, timestamp)
            logger.info(f"✅ Checkpoint salvo: {timestamp}")
            return True
        except Exception as exc:
            logger.error(f"Erro ao salvar checkpoint: {exc}")
            return False

    def load(self, system: Any) -> bool:
        checkpoints = sorted(self.checkpoint_dir.glob("metadata_*.json"))
        if not checkpoints:
            return False
        latest = checkpoints[-1]
        timestamp = latest.stem.replace("metadata_", "")
        if hasattr(system, "generator"):
            self._load_generator(system.generator, timestamp)
        if hasattr(system, "simulation"):
            self._load_simulation(system.simulation, timestamp)
        logger.info(f"✅ Checkpoint carregado: {timestamp}")
        return True

    def _save_generator(self, generator, timestamp):
        path = self.checkpoint_dir / f"generator_{timestamp}.pkl"
        with path.open("wb") as handle:
            pickle.dump({"agents": generator.agents, "agent_counter": generator.agent_counter}, handle)

    def _load_generator(self, generator, timestamp):
        path = self.checkpoint_dir / f"generator_{timestamp}.pkl"
        if path.exists():
            with path.open("rb") as handle:
                data = pickle.load(handle)
                generator.agents = data["agents"]
                generator.agent_counter = data["agent_counter"]

    def _save_simulation(self, simulation, timestamp):
        path = self.checkpoint_dir / f"simulation_{timestamp}.pt"
        agent_weights = {name: agent.model.state_dict() for name, agent in simulation.rl_agents.items()}
        torch.save({"history": list(simulation.history), "predictions": list(simulation.predictions), "agent_weights": agent_weights}, path)

    def _load_simulation(self, simulation, timestamp):
        path = self.checkpoint_dir / f"simulation_{timestamp}.pt"
        if path.exists():
            data = torch.load(path, map_location="cpu")
            simulation.history = data["history"]
            simulation.predictions = data["predictions"]
            for name, weights in data.get("agent_weights", {}).items():
                if name in simulation.rl_agents:
                    simulation.rl_agents[name].model.load_state_dict(weights)

    def _save_neuroevolution(self, neuro, timestamp):
        path = self.checkpoint_dir / f"neuro_{timestamp}.pt"
        torch.save({"generation": neuro.generation, "best_fitness": getattr(neuro, "best_fitness", 0)}, path)

    def _save_metadata(self, metadata: dict, timestamp: str):
        path = self.checkpoint_dir / f"metadata_{timestamp}.json"
        with path.open("w") as handle:
            json.dump(metadata, handle, indent=2)
