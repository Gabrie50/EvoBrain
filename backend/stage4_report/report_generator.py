"""
Gerador de relatórios - produz relatórios detalhados com LLM local
"""

import json
from typing import Dict, Any
from datetime import datetime

from ..llm.local_llm import LocalLLM
from utils.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """Gera relatórios detalhados usando LLM local"""
    
    def __init__(self, llm: LocalLLM):
        self.llm = llm
    
    def generate_report(self, stats: Dict[str, Any]) -> str:
        """Gera relatório completo da simulação"""
        logger.info("📊 Gerando relatório...")
        
        prompt = self._build_report_prompt(stats)
        report = self.llm.generate(prompt)
        
        # Adiciona cabeçalho com informações básicas
        header = self._build_report_header(stats)
        
        return f"{header}\n\n{report}"
    
    def generate_summary(self, stats: Dict[str, Any]) -> str:
        """Gera resumo executivo"""
        prompt = f"""
        Gere um resumo executivo conciso (3-5 frases) sobre a simulação:
        
        - Precisão: {stats.get('simulation', {}).get('accuracy', 0):.1f}%
        - Agentes ativos: {stats.get('simulation', {}).get('active_agents', 0)}
        - Previsões feitas: {stats.get('simulation', {}).get('predictions_made', 0)}
        
        Destaque os principais insights e recomendações.
        """
        
        return self.llm.generate(prompt)
    
    def generate_detailed_analysis(self, stats: Dict[str, Any]) -> str:
        """Gera análise detalhada"""
        prompt = self._build_detailed_analysis_prompt(stats)
        return self.llm.generate(prompt)
    
    def _build_report_prompt(self, stats: Dict[str, Any]) -> str:
        """Constrói prompt para o relatório"""
        sim = stats.get('simulation', {})
        gen = stats.get('generation', {})
        neuro = sim.get('neuroevolution', {})
        
        return f"""
        Você é um analista de dados especializado em sistemas de previsão.
        Gere um relatório profissional com base nas estatísticas abaixo.
        
        ## ESTATÍSTICAS DA SIMULAÇÃO
        
        ### Previsões
        - Total de previsões: {sim.get('predictions_made', 0)}
        - Acertos: {sim.get('correct_predictions', 0)}
        - Precisão: {sim.get('accuracy', 0):.1f}%
        
        ### Agentes
        - Agentes ativos: {sim.get('active_agents', 0)}
        - Total de agentes criados: {gen.get('total_agents', 0)}
        - Agentes pendentes: {gen.get('pending', 0)}
        
        ### Neuroevolução
        - Geração atual: {neuro.get('generation', 0)}
        - Melhor fitness: {neuro.get('best_fitness', 0):.2f}%
        - Tamanho da população: {neuro.get('population_size', 0)}
        
        ### Sistema
        - Uptime: {stats.get('uptime', 0) / 3600:.1f} horas
        - LLM conectado: {stats.get('llm_connected', False)}
        
        ## FORMATO DO RELATÓRIO
        
        1. **Resumo Executivo** (2-3 frases)
        2. **Análise de Performance** (precisão, tendências)
        3. **Análise dos Agentes** (evolução, especializações)
        4. **Recomendações** (como melhorar)
        5. **Próximos Passos**
        
        Seja objetivo e use linguagem profissional.
        """
    
    def _build_detailed_analysis_prompt(self, stats: Dict[str, Any]) -> str:
        """Constrói prompt para análise detalhada"""
        sim = stats.get('simulation', {})
        recent_predictions = sim.get('recent_predictions', [])
        
        return f"""
        Realize uma análise detalhada da simulação com base nos dados:
        
        ## DADOS RECENTES
        Últimas 10 previsões:
        {json.dumps(recent_predictions[-10:], indent=2)}
        
        ## ANÁLISE REQUERIDA
        
        1. **Análise de Erros**: Identifique padrões nos erros
        2. **Análise de Acertos**: O que funcionou bem?
        3. **Tendências**: Há mudanças na performance ao longo do tempo?
        4. **Recomendações**: 3-5 ações concretas para melhorar
        
        Forneça insights acionáveis e baseados em evidências.
        """
    
    def _build_report_header(self, stats: Dict[str, Any]) -> str:
        """Constrói cabeçalho do relatório"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                     RELATÓRIO EVOBRAIN                           ║
║                     Gerado em: {now}                             ║
╠══════════════════════════════════════════════════════════════════╣
║  Precisão: {stats.get('simulation', {}).get('accuracy', 0):>5.1f}%                                          ║
║  Agentes:  {stats.get('simulation', {}).get('active_agents', 0):>5d} ativos / {stats.get('generation', {}).get('total_agents', 0):>5d} total     ║
║  Previsões: {stats.get('simulation', {}).get('predictions_made', 0):>5d}                                     ║
╚══════════════════════════════════════════════════════════════════╝
"""
