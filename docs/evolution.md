# Sistema de Evolução do EvoBrain

## Visão Geral

O EvoBrain possui um sistema de evolução baseado em memória que permite que os agentes:
- Herdem conhecimento de agentes bem-sucedidos
- Combinem estratégias via crossover
- Sofram mutações para explorar novas estratégias
- Competem em torneios eliminatórios

## Componentes

### 1. Seleção por Fitness
- Baseado em performance e qualidade das memórias
- Mantém os melhores agentes para próxima geração

### 2. Crossover Genético
- Combina pesos das redes neurais (60% pai1, 40% pai2)
- Herda memórias importantes de ambos os pais
- Cria novos agentes com conhecimento combinado

### 3. Mutação
- Adiciona ruído aos pesos da rede neural
- Taxa de mutação configurável (padrão 10%)
- Permite exploração de novas estratégias

### 4. Competição (Torneios)
- Agentes competem em pares
- Sistema de ranking Elo
- Eliminação dos agentes mais fracos

## Ciclo de Evolução

1. **Avaliação**: Calcula fitness de cada agente
2. **Seleção**: Mantém os melhores (elite)
3. **Crossover**: Cria novos agentes a partir dos melhores
4. **Mutação**: Aplica mutações aleatórias
5. **Competição**: Torneio entre agentes
6. **Eliminação**: Remove os piores agentes

## Parâmetros Configuráveis

| Parâmetro | Padrão | Descrição |
|-----------|--------|-----------|
| mutation_rate | 0.1 | Taxa de mutação |
| elite_percent | 0.2 | Porcentagem mantida |
| crossover_rate | 0.7 | Taxa de crossover |
| population_size | 1000 | Tamanho da população |
| elo_k | 32 | Fator K do Elo |
| keep_ratio | 0.3 | Proporção mantida após eliminação |
| tournament_rounds | 3 | Número de rodadas do torneio |
