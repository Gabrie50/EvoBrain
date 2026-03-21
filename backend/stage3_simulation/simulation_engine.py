import time
from collections import deque
from typing import Any, Dict, List, Optional

from stage2_generation.dynamic_generator import DynamicAgentGenerator
from stage3_simulation.feedback_loop import FeedbackLoop
from stage3_simulation.neuroevolution import NeuroEvolution
from stage3_simulation.pattern_detector import PatternDetector
from stage3_simulation.rl_agent import RLAgent
from stage3_simulation.state_extractor import StateExtractor
from utils.logger import get_logger

logger = get_logger(__name__)


class DynamicSimulationEngine:
    def __init__(self, generator: DynamicAgentGenerator, state_size: int = 150, history_size: int = 5000):
        self.generator = generator
        self.state_size = state_size
        self.history_size = history_size
        self.rl_agents: Dict[str, RLAgent] = {}
        self.neuroevolution = NeuroEvolution(population_size=1000)
        self.history: deque = deque(maxlen=history_size)
        self.predictions: deque = deque(maxlen=1000)
        self.state_extractor = StateExtractor(state_size)
        self.feedback_loop = FeedbackLoop()
        self.pattern_detector = PatternDetector()
        self.total_predictions = 0
        self.correct_predictions = 0
        self._running = False

    def run_continuously(self, data_api):
        self._running = True
        while self._running:
            try:
                new_data = data_api.fetch_latest()
                if new_data:
                    self.history.append(new_data)
                    self._sync_agents()
                    if len(self.history) >= 30:
                        self._predict()
                    if self.predictions:
                        self._learn()
                time.sleep(0.5)
            except Exception as exc:
                logger.error(f"Erro na simulação: {exc}")
                time.sleep(1)

    def _sync_agents(self):
        for name in list(self.generator.agents.keys()):
            if name not in self.rl_agents:
                profile = self.generator.get_agent(name)
                if profile:
                    self.rl_agents[name] = RLAgent(profile, self.state_size)

    def _predict(self):
        state = self.state_extractor.extract(list(self.history)[-30:])
        votes = {"BANKER": 0.0, "PLAYER": 0.0}
        agent_votes = []
        for name, agent in self.rl_agents.items():
            action, confidence = agent.decide(state)
            prediction = "BANKER" if action == 0 else "PLAYER"
            weight = 1.0 + agent.profile.accuracy / 100
            votes[prediction] += weight * confidence
            agent_votes.append({"name": name, "prediction": prediction, "confidence": confidence, "weight": weight})
        if not any(votes.values()):
            return
        prediction = max(votes, key=votes.get)
        confidence = (votes[prediction] / max(sum(votes.values()), 1e-8)) * 100
        self.predictions.append({"prediction": prediction, "confidence": confidence, "votes": votes, "agent_votes": agent_votes[:10], "state": state.copy(), "timestamp": time.time(), "agents_active": len(self.rl_agents)})

    def _learn(self):
        if not self.predictions or len(self.history) < 2:
            return
        pred = self.predictions.popleft()
        real_result = self.history[-1]["resultado"]
        acertou = pred["prediction"] == real_result
        self.total_predictions += 1
        if acertou:
            self.correct_predictions += 1
        next_state = self.state_extractor.extract(list(self.history)[-30:])
        for agent in self.rl_agents.values():
            action = 0 if pred["prediction"] == "BANKER" else 1
            agent.learn(action, real_result, next_state)
        self.feedback_loop.process(pred, real_result, acertou)

    def stop(self):
        self._running = False

    def get_current_prediction(self) -> dict:
        if not self.predictions:
            return {"status": "no_prediction"}
        last = self.predictions[-1]
        return {"prediction": last["prediction"], "confidence": round(last["confidence"], 1), "votes": last["votes"], "agents_active": last["agents_active"], "timestamp": last["timestamp"]}

    def get_prediction_history(self, limit: int = 100) -> List[dict]:
        return [{"prediction": item["prediction"], "confidence": item["confidence"], "timestamp": item["timestamp"]} for item in list(self.predictions)[-limit:]]

    @property
    def accuracy(self) -> float:
        return (self.correct_predictions / self.total_predictions) * 100 if self.total_predictions else 0.0

    def get_stats(self) -> dict:
        return {"active_agents": len(self.rl_agents), "total_agents_ever": len(self.generator.agents), "pending_agents": len(self.generator.pending_generation), "predictions_made": self.total_predictions, "correct_predictions": self.correct_predictions, "accuracy": self.accuracy, "history_size": len(self.history), "neuroevolution": self.neuroevolution.get_stats(), "recent_predictions": self.get_prediction_history(10)}
