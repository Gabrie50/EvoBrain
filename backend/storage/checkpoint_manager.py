"""
Gerenciador de checkpoints - salva e carrega estado do sistema
"""

import os
import json
import torch
import pickle
from pathlib import Path
from typing import Optional, Any
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)


class CheckpointManager:
    """Gerencia checkpoints do sistema"""
    
    def __init__(self, checkpoint_dir: str = "storage/checkpoints"):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"💾 CheckpointManager: {self.checkpoint_dir}")
    
    def save(self, system: Any) -> bool:
        """Salva checkpoint completo do sistema"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Salva estado do gerador
            if hasattr(system, 'generator'):
                self._save_generator(system.generator, timestamp)
            
            # Salva estado da simulação
            if hasattr(system, 'simulation'):
                self._save_simulation(system.simulation, timestamp)
            
            # Salva estado da neuroevolução
            if hasattr(system, 'simulation') and hasattr(system.simulation, 'neuroevolution'):
                self._save_neuroevolution(system.simulation.neuroevolution, timestamp)
            
            # Salva metadados
            metadata = {
                'timestamp': timestamp,
                'uptime': getattr(system, '_start_time', 0),
                'version': '1.0.0'
            }
            self._save_metadata(metadata, timestamp)
            
            logger.info(f"✅ Checkpoint salvo: {timestamp}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar checkpoint: {e}")
            return False
    
    def load(self, system: Any) -> bool:
        """Carrega último checkpoint"""
        try:
            # Encontra checkpoint mais recente
            checkpoints = sorted(self.checkpoint_dir.glob("metadata_*.json"))
            if not checkpoints:
                logger.info("Nenhum checkpoint encontrado")
                return False
            
            latest = checkpoints[-1]
            timestamp = latest.stem.replace("metadata_", "")
            
            # Carrega estado do gerador
            if hasattr(system, 'generator'):
                self._load_generator(system.generator, timestamp)
            
            # Carrega estado da simulação
            if hasattr(system, 'simulation'):
                self._load_simulation(system.simulation, timestamp)
            
            # Carrega estado da neuroevolução
            if hasattr(system, 'simulation') and hasattr(system.simulation, 'neuroevolution'):
                self._load_neuroevolution(system.simulation.neuroevolution, timestamp)
            
            logger.info(f"✅ Checkpoint carregado: {timestamp}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar checkpoint: {e}")
            return False
    
    def _save_generator(self, generator, timestamp: str):
        """Salva estado do gerador dinâmico"""
        path = self.checkpoint_dir / f"generator_{timestamp}.pkl"
        
        with open(path, 'wb') as f:
            pickle.dump({
                'agents': generator.agents,
                'agent_counter': generator.agent_counter,
                'pending': list(generator.pending_generation)
            }, f)
    
    def _load_generator(self, generator, timestamp: str):
        """Carrega estado do gerador"""
        path = self.checkpoint_dir / f"generator_{timestamp}.pkl"
        if not path.exists():
            return
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
            
        generator.agents = data['agents']
        generator.agent_counter = data['agent_counter']
        generator.pending_generation = data['pending']
    
    def _save_simulation(self, simulation, timestamp: str):
        """Salva estado da simulação"""
        path = self.checkpoint_dir / f"simulation_{timestamp}.pt"
        
        # Salva pesos dos agentes
        agent_weights = {}
        for name, agent in simulation.rl_agents.items():
            agent_weights[name] = agent.model.state_dict()
        
        torch.save({
            'history': list(simulation.history),
            'predictions': list(simulation.predictions),
            'total_predictions': simulation.total_predictions,
            'correct_predictions': simulation.correct_predictions,
            'agent_weights': agent_weights
        }, path)
    
    def _load_simulation(self, simulation, timestamp: str):
        """Carrega estado da simulação"""
        path = self.checkpoint_dir / f"simulation_{timestamp}.pt"
        if not path.exists():
            return
        
        data = torch.load(path, map_location='cpu')
        
        simulation.history = data['history']
        simulation.predictions = data['predictions']
        simulation.total_predictions = data['total_predictions']
        simulation.correct_predictions = data['correct_predictions']
        
        # Carrega pesos dos agentes
        for name, weights in data.get('agent_weights', {}).items():
            if name in simulation.rl_agents:
                simulation.rl_agents[name].model.load_state_dict(weights)
    
    def _save_neuroevolution(self, neuro, timestamp: str):
        """Salva estado da neuroevolução"""
        path = self.checkpoint_dir / f"neuro_{timestamp}.pt"
        
        torch.save({
            'generation': neuro.generation,
            'best_fitness': neuro.best_fitness,
            'fitness_history': list(neuro.fitness_history)
        }, path)
    
    def _load_neuroevolution(self, neuro, timestamp: str):
        """Carrega estado da neuroevolução"""
        path = self.checkpoint_dir / f"neuro_{timestamp}.pt"
        if not path.exists():
            return
        
        data = torch.load(path, map_location='cpu')
        
        neuro.generation = data['generation']
        neuro.best_fitness = data['best_fitness']
        neuro.fitness_history = data['fitness_history']
    
    def _save_metadata(self, metadata: dict, timestamp: str):
        """Salva metadados"""
        path = self.checkpoint_dir / f"metadata_{timestamp}.json"
        
        with open(path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def list_checkpoints(self) -> list:
        """Lista checkpoints disponíveis"""
        checkpoints = []
        for path in self.checkpoint_dir.glob("metadata_*.json"):
            timestamp = path.stem.replace("metadata_", "")
            with open(path, 'r') as f:
                metadata = json.load(f)
            checkpoints.append({
                'timestamp': timestamp,
                'metadata': metadata
            })
        return sorted(checkpoints, key=lambda x: x['timestamp'], reverse=True)
