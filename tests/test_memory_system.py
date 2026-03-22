"""Testes do sistema de memória."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from stage2_generation.memory_system import MemoryImportance, MemorySystem, MemoryType


def test_memory_system():
    ms = MemorySystem(agent_id=1)
    ms.remember("Teste de memória", MemoryType.EPISODIC, MemoryImportance.HIGH)
    memories = ms.recall("teste", limit=5)
    assert len(memories) > 0
    assert "Teste" in memories[0].content


def test_episodic_memory_limit():
    ms = MemorySystem(agent_id=1)
    for index in range(150):
        ms.remember(f"Memória {index}", MemoryType.EPISODIC)
    assert len(ms.episodic.memories) <= 100


def test_long_term_memory():
    ms = MemorySystem(agent_id=1)
    ms.remember("Memória importante", MemoryType.SEMANTIC, MemoryImportance.CRITICAL)
    ms.remember("Memória menos importante", MemoryType.SEMANTIC, MemoryImportance.LOW)
    important = ms.recall("importante")
    assert len(important) > 0


if __name__ == "__main__":
    pytest.main([__file__])
