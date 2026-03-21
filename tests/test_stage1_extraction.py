import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from stage1_extraction.graph_extractor import GraphExtractor
from stage1_extraction.knowledge_graph import KnowledgeGraph


class MockLLM:
    def generate(self, prompt: str) -> str:
        if 'rela' in prompt.lower():
            return '{"relations": []}'
        return '{"entities": [{"name": "Teste", "type": "conceito", "description": "Entidade de teste"}]}'


def test_knowledge_graph():
    kg = KnowledgeGraph()
    kg.add_entity('Entidade1', 'pessoa', 'Descrição 1')
    kg.add_entity('Entidade2', 'organizacao', 'Descrição 2')
    kg.add_relation('Entidade1', 'Entidade2', 'trabalha_para')
    assert len(kg.nodes) == 2
    assert len(kg.edges) == 1
    assert kg.get_entity('Entidade1') is not None
    assert len(kg.get_relations('Entidade1')) == 1
    assert len(kg.get_neighbors('Entidade1')) == 1


def test_graph_extractor():
    extractor = GraphExtractor(MockLLM())
    result = extractor.extract_from_text('Texto de teste')
    assert 'entities' in result
    assert 'relations' in result
