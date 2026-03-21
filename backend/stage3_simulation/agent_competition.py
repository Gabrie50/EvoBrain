"""Competição entre agentes com torneio e ranking Elo."""

from __future__ import annotations

import random
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from config import settings
from stage3_simulation.memory_enhanced_agent import MemoryEnhancedAgent
from stage3_simulation.memory_ranking import MemoryRanker
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class TournamentResult:
    winner: MemoryEnhancedAgent
    loser: MemoryEnhancedAgent
    winner_score: float
    loser_score: float
    tournament_id: int
    round: int


class AgentCompetition:
    def __init__(self, memory_ranker: MemoryRanker, elo_k: int = 32):
        self.memory_ranker = memory_ranker
        self.elo_k = elo_k
        self.elo_ratings: Dict[int, float] = defaultdict(lambda: 1200.0)
        self.tournament_history: List[TournamentResult] = []
        self.tournament_counter = 0
        logger.info("🏆 AgentCompetition inicializado")

    def compete(
        self,
        agent1: MemoryEnhancedAgent,
        agent2: MemoryEnhancedAgent,
        test_episodes: int = 100,
    ) -> Tuple[MemoryEnhancedAgent, float, float]:
        score1, score2 = 0, 0
        for _ in range(test_episodes):
            action1, _ = agent1.decide(np.random.randn(settings.agents.state_size).astype(np.float32))
            action2, _ = agent2.decide(np.random.randn(settings.agents.state_size).astype(np.float32))
            possible_outcomes = [action["id"] for action in settings.get_domain_actions()[:2]] or [0, 1]
            outcome = random.choice(possible_outcomes)
            if action1 == outcome:
                score1 += 1
            if action2 == outcome:
                score2 += 1
        winner = agent1 if score1 >= score2 else agent2
        return winner, score1 / test_episodes, score2 / test_episodes

    def tournament(self, agents: List[MemoryEnhancedAgent], rounds: int = 3) -> List[MemoryEnhancedAgent]:
        logger.info(f"🏆 TORNEIO - {len(agents)} agentes")
        survivors = list(agents)
        for round_num in range(rounds):
            random.shuffle(survivors)
            next_round = []
            for index in range(0, len(survivors) - 1, 2):
                agent1, agent2 = survivors[index], survivors[index + 1]
                winner, score1, score2 = self.compete(agent1, agent2)
                next_round.append(winner)
                self._update_elo(agent1.profile.id, agent2.profile.id, winner == agent1)
                self.tournament_history.append(
                    TournamentResult(
                        winner=winner,
                        loser=agent2 if winner == agent1 else agent1,
                        winner_score=score1 if winner == agent1 else score2,
                        loser_score=score2 if winner == agent1 else score1,
                        tournament_id=self.tournament_counter,
                        round=round_num,
                    )
                )
            if len(survivors) % 2 == 1:
                next_round.append(survivors[-1])
            survivors = next_round
        self.tournament_counter += 1
        logger.info(f"   ✅ Torneio finalizado: {len(survivors)} sobreviventes")
        return survivors

    def _update_elo(self, agent_id1: int, agent_id2: int, agent1_won: bool):
        rating1, rating2 = self.elo_ratings[agent_id1], self.elo_ratings[agent_id2]
        expected1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
        expected2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))
        if agent1_won:
            self.elo_ratings[agent_id1] = rating1 + self.elo_k * (1 - expected1)
            self.elo_ratings[agent_id2] = rating2 + self.elo_k * (0 - expected2)
        else:
            self.elo_ratings[agent_id1] = rating1 + self.elo_k * (0 - expected1)
            self.elo_ratings[agent_id2] = rating2 + self.elo_k * (1 - expected2)

    def eliminate_weak(self, agents: List[MemoryEnhancedAgent], keep_ratio: float = 0.3) -> List[MemoryEnhancedAgent]:
        if not agents:
            return []
        scored_agents = []
        for agent in agents:
            perf_score = agent.profile.accuracy / 100
            elo_score = (self.elo_ratings[agent.profile.id] - 800) / 800
            top_memories = self.memory_ranker.get_top_memories(agent.profile.id, 5)
            memory_score = sum(memory.total_score for memory in top_memories) / 5 if top_memories else 0
            total_score = 0.5 * perf_score + 0.3 * max(0, min(1, elo_score)) + 0.2 * memory_score
            scored_agents.append((agent, total_score))
        scored_agents.sort(key=lambda item: item[1], reverse=True)
        keep_count = max(1, int(len(agents) * keep_ratio))
        survivors = [agent for agent, _ in scored_agents[:keep_count]]
        logger.info(f"⚔️ Eliminação: {len(agents) - keep_count} eliminados, {keep_count} sobrevivem")
        return survivors

    def get_ranking(self, agents: List[MemoryEnhancedAgent]) -> List[Tuple[str, float]]:
        ranking = [(agent.profile.name, self.elo_ratings[agent.profile.id]) for agent in agents]
        ranking.sort(key=lambda item: item[1], reverse=True)
        return ranking

    def get_statistics(self) -> dict:
        ratings = list(self.elo_ratings.values())
        return {
            "total_tournaments": self.tournament_counter,
            "total_matches": len(self.tournament_history),
            "avg_elo": float(np.mean(ratings)) if ratings else 1200,
            "max_elo": float(np.max(ratings)) if ratings else 1200,
        }
