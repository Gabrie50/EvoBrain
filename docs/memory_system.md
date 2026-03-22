# Sistema de Memória do EvoBrain

## Visão Geral

O EvoBrain possui um sistema de memória completo que permite que os agentes:
- Lembrem de experiências passadas (episódica)
- Acumulem conhecimento (semântica)
- Aprendam estratégias (procedural)
- Mantenham relacionamentos sociais (social)
- Associem emoções às memórias (emocional)

## Tipos de Memória

### 1. Memória Episódica
- Armazena experiências recentes
- Capacidade: 100 memórias (FIFO)
- Usada para decisões imediatas

### 2. Memória de Longo Prazo (LTM)
- Armazena conhecimento permanente
- Capacidade: 10.000 memórias
- Busca por conteúdo (palavras-chave)

### 3. Memória Social
- Registra interações entre agentes
- Mantém afinidade entre agentes
- Influencia decisões baseadas em relacionamentos

### 4. Memória de Trabalho
- Combinação de estado atual + memórias recuperadas
- Capacidade: 10 itens
- Usada para decisão imediata

## Ranking de Memórias

As memórias são rankeadas por:
- **Importância emocional**: baseada na recompensa
- **Utilidade**: quantas vezes foi usada com sucesso
- **Social**: impacto em outros agentes
- **Recência**: quão recente é a memória

## Consolidação e Esquecimento

- Memórias frequentemente acessadas são consolidadas
- Memórias não acessadas por muito tempo enfraquecem
- Memórias com baixa consolidação são esquecidas

## Uso em Decisões

O agente recupera memórias relevantes baseadas no contexto atual e as utiliza na decisão, combinando estado atual com experiências passadas.
