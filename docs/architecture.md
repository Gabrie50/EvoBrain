# Arquitetura do EvoBrain

## Estrutura base

- `backend/`: pipeline principal dividido por estágios, coleta de dados, persistência, LLM local, API e utilitários.
- `frontend/`: aplicação React/TypeScript com componentes, páginas, hooks, serviços, tipos e utilitários.
- `scripts/`: automações para modelo local, treino e avaliação.
- `tests/`: suíte inicial de testes para estágios do backend e API.
- `docs/`: documentação de arquitetura, API e deploy.
