# API Documentation

## Base URL

`http://localhost:8000/api`

## Endpoints

### Health
- `GET /health`
- `GET /health/detailed`

### Stats
- `GET /stats`
- `GET /stats/summary`
- `GET /stats/agents`
- `GET /stats/simulation`

### Predict
- `GET /predict/current`
- `GET /predict/history?limit=100`

### Agents
- `GET /agents`
- `GET /agents/{name}`
- `GET /agents/{name}/stats`

### Chat
- `POST /chat/agent`
- `GET /chat/agents`
- `POST /chat/agent/{name}/reset`

### Report
- `GET /report/generate?type=full`
- `GET /report/summary`

### Upload
- `POST /upload/pdf`
- `POST /upload/text`
- `GET /upload/status/{task_id}`

## WebSocket

`ws://localhost:8000/api/ws`
