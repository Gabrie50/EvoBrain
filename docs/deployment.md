# Guia de Deploy

## Docker

```bash
cp .env.example .env
docker-compose up -d
```

Frontend em `http://localhost:3000` e API em `http://localhost:8000/docs`.

## Manual

```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
cd frontend
npm install
npm run dev
```
