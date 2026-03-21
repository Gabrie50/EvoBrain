# 🧠 EvoBrain - RL + Neuroevolution 24/7

> Sistema de previsão contínua com 5 etapas (MiroFish + RL + LLM Local)
> **Aprendizado contínuo | Custo ZERO | Evolução genética | 24/7**

---

## 🚀 O que é o EvoBrain?

O EvoBrain é um sistema híbrido que combina:

1. **As 5 etapas do MiroFish** (extração, geração, simulação, relatório, interação)
2. **RL + Neuroevolution** no motor de simulação (substitui o gargalo da LLM)
3. **LLM Local (Ollama)** para extração, geração, relatórios e interação
4. **API externa em tempo real** para dados 24/7

---

## 🆚 Comparação com MiroFish

| Etapa | MiroFish | EvoBrain |
|-------|----------|----------|
| 1. Extração | LLM API (cara) | LLM LOCAL (Ollama) |
| 2. Geração | LLM API (cara) | LLM LOCAL + DINÂMICA |
| 3. Simulação | LLM API (GARGALO) | **RL + Neuroevolution (GRÁTIS)** |
| 4. Relatório | LLM API | LLM LOCAL (opcional) |
| 5. Interação | LLM API | LLM LOCAL |
| **Custo** | $$$ por simulação | **$0** (inferência local) |
| **Aprendizado 24/7** | ❌ | ✅ |
| **Evolução contínua** | ❌ | ✅ |

---

## 📦 Instalação

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker (opcional)
- Ollama (para LLM local)

### Via Docker (recomendado)

```bash
# Clone o repositório
git clone https://github.com/Gabrie50/EvoBrain.git
cd EvoBrain

# Inicie com Docker Compose
docker-compose up -d

# Baixe o modelo LLM
docker exec -it evobrain_ollama_1 ollama pull llama3.2

# Acesse:
# Frontend: http://localhost:3000
# API: http://localhost:8000/docs
```

### Manual

```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend (outro terminal)
cd frontend
npm install
npm run dev

# LLM Local (outro terminal)
ollama serve
ollama pull llama3.2
```

---

## 🎯 Como Usar

### 1. Upload de PDF (Etapas 1 e 2)

```bash
curl -X POST http://localhost:8000/api/upload/pdf \
  -F "file=@relatorio.pdf"
```

O sistema irá:

- Extrair entidades e relações
- Criar agentes dinamicamente (sob demanda)

### 2. Simulação 24/7 (Etapa 3)

A simulação começa automaticamente e:

- Coleta dados da API do Bac Bo
- Agentes RL decidem com base no histórico
- Neuroevolution evolui os agentes
- Feedback loop aprende com erros

### 3. Gerar Relatório (Etapa 4)

```bash
curl http://localhost:8000/api/report/generate
```

### 4. Conversar com Agentes (Etapa 5)

```bash
curl -X POST http://localhost:8000/api/chat/agent \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "Banco_Central", "question": "Por que você previu BANKER?"}'
```

---

## 📊 Arquitetura

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EVOBRAIN - 5 ETAPAS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ETAPA 1: EXTRACAO                                                          │
│  📄 PDF/TEXT → GraphRAG → Entidades e relações                              │
│  🖥️ LLM LOCAL (Ollama)                                                      │
│                                                                             │
│  ETAPA 2: GERACAO DINAMICA                                                  │
│  🤖 Cria agentes sob demanda (não todos de uma vez)                         │
│  🖥️ LLM LOCAL + Fila de geração                                             │
│                                                                             │
│  ETAPA 3: SIMULACAO ← CORAÇÃO DO SISTEMA                                    │
│  ⚡ GARGALO ELIMINADO!                                                       │
│  🧠 Agentes RL (1000+ evoluindo)                                            │
│  🧬 Neuroevolution + crossover genético                                     │
│  📡 API externa (Bac Bo) em tempo real                                      │
│  🔄 Feedback loop aprende com erros                                         │
│                                                                             │
│  ETAPA 4: RELATORIO                                                         │
│  📊 ReportAgent analisa simulação                                           │
│  🖥️ LLM LOCAL (opcional)                                                    │
│                                                                             │
│  ETAPA 5: INTERACAO                                                         │
│  💬 Conversa com agentes, pergunta sobre decisões                           │
│  🖥️ LLM LOCAL                                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧬 Neuroevolution

- **População:** Até 10.000 agentes (crescimento orgânico)
- **Seleção:** Top 20% (elite)
- **Crossover:** Média ponderada dos pesos
- **Mutação:** Ruído gaussiano (2%)
- **Fitness:** Precisão + especialização

---

## 📈 Métricas

| Métrica | Descrição |
|---------|-----------|
| Precisão | Acertos / Total de previsões |
| Agentes ativos | Quantos agentes estão na simulação |
| Taxa de criação | Agentes criados por minuto |
| Geração | Número de evoluções |
| Tempo de resposta | Latência das previsões (<10ms) |

---

## 🔧 Configuração

Edite `.env`:

```env
# LLM
LLM_MODEL=llama3.2
LLM_HOST=http://localhost:11434

# Agentes
MAX_AGENTS=10000
STATE_SIZE=150

# RL
LEARNING_RATE=0.001
GAMMA=0.99
EPSILON_START=0.3
EPSILON_MIN=0.05

# Neuroevolution
MUTATION_RATE=0.1
ELITE_PERCENT=0.2

# API
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 📝 Licença

MIT

---

## 👨‍💻 Autor

@Gabrie50
