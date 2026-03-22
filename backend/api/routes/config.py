"""Rotas para configuração via API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


class UpdateConfigRequest(BaseModel):
    path: str
    value: Any


class DomainConfigRequest(BaseModel):
    type: str
    name: str
    description: str
    actions: List[Dict[str, Any]]


class LLMConfigRequest(BaseModel):
    type: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    host: Optional[str] = None
    api_key: Optional[str] = None


class DataSourceConfigRequest(BaseModel):
    type: str
    enabled: bool = True
    interval: float = 0.5
    rest_url: Optional[str] = None
    ws_url: Optional[str] = None


class SaveConfigRequest(BaseModel):
    domain: Optional[Dict[str, Any]] = None
    llm: Optional[Dict[str, Any]] = None
    data_source: Optional[Dict[str, Any]] = None
    agents: Optional[Dict[str, Any]] = None
    neuroevolution: Optional[Dict[str, Any]] = None
    competition: Optional[Dict[str, Any]] = None


@router.get("/config")
async def get_config():
    return settings.to_dict()


@router.get("/config/{path}")
async def get_config_value(path: str):
    value: Any = settings.to_dict()
    for key in path.split("."):
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            raise HTTPException(status_code=404, detail=f"Configuração '{path}' não encontrada")
    return {"path": path, "value": value}


@router.post("/config")
async def update_config(request: UpdateConfigRequest):
    try:
        parts = request.path.split(".")
        target = settings
        for part in parts[:-1]:
            target = getattr(target, part)
        setattr(target, parts[-1], request.value)
        return {"success": True, "path": request.path, "value": request.value}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/config/save")
async def save_config(request: SaveConfigRequest):
    try:
        payload = request.model_dump(exclude_none=True)
        for section, values in payload.items():
            target = getattr(settings, section)
            for key, value in values.items():
                setattr(target, key, value)
        return {"success": True, "config": settings.to_dict()}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/config/domain")
async def configure_domain(request: DomainConfigRequest):
    try:
        settings.domain.type = request.type
        settings.domain.name = request.name
        settings.domain.description = request.description
        settings.domain.actions = request.actions
        return {"success": True, "domain": request.model_dump()}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/config/llm")
async def configure_llm(request: LLMConfigRequest):
    try:
        settings.llm.type = request.type
        settings.llm.model = request.model
        settings.llm.temperature = request.temperature
        settings.llm.max_tokens = request.max_tokens
        if request.host:
            settings.llm.host = request.host
        if request.api_key:
            settings.llm.api_key = request.api_key
        return {"success": True, "llm": request.model_dump()}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/config/data_source")
async def configure_data_source(request: DataSourceConfigRequest):
    try:
        settings.data_source.type = request.type
        settings.data_source.enabled = request.enabled
        settings.data_source.interval = request.interval
        if request.rest_url:
            settings.data_source.rest_url = request.rest_url
        if request.ws_url:
            settings.data_source.ws_url = request.ws_url
        return {"success": True, "data_source": request.model_dump()}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/config/domains")
async def list_domains():
    return [
        {"id": "bacbo", "name": "Bac Bo", "description": "Jogo de dados Bac Bo", "actions": [{"id": 0, "name": "BANKER", "color": "🔴", "emoji": "🔴"}, {"id": 1, "name": "PLAYER", "color": "🔵", "emoji": "🔵"}, {"id": 2, "name": "TIE", "color": "🟡", "emoji": "🟡"}], "preset": True},
        {"id": "stock_market", "name": "Mercado Financeiro", "description": "Previsão de ações", "actions": [{"id": 0, "name": "BUY", "color": "🟢", "emoji": "🟢"}, {"id": 1, "name": "SELL", "color": "🔴", "emoji": "🔴"}], "preset": True},
        {"id": "sports", "name": "Esportes", "description": "Previsão esportiva", "actions": [{"id": 0, "name": "HOME", "color": "🏠", "emoji": "🏠"}, {"id": 1, "name": "AWAY", "color": "✈️", "emoji": "✈️"}, {"id": 2, "name": "DRAW", "color": "⚪", "emoji": "⚪"}], "preset": True},
        {"id": "politics", "name": "Política", "description": "Previsão política", "actions": [{"id": 0, "name": "CANDIDATO_A", "color": "🔵", "emoji": "🔵"}, {"id": 1, "name": "CANDIDATO_B", "color": "🔴", "emoji": "🔴"}], "preset": True},
        {"id": "custom", "name": "Customizado", "description": "Configure suas próprias ações", "actions": [], "preset": False},
    ]


@router.get("/config/llm_types")
async def list_llm_types():
    return [
        {"id": "ollama", "name": "Ollama", "description": "LLM local via Ollama", "requires_api_key": False, "requires_model": True, "default_model": "llama3.2", "config_fields": [{"name": "host", "type": "string", "default": "http://localhost:11434", "label": "Host"}]},
        {"id": "llama_cpp", "name": "Llama.cpp", "description": "LLM local via Llama.cpp", "requires_api_key": False, "requires_model": True, "default_model": "./models/llama-2-7b.gguf", "config_fields": [{"name": "model_path", "type": "string", "label": "Caminho do modelo"}]},
        {"id": "openai", "name": "OpenAI API", "description": "API da OpenAI", "requires_api_key": True, "requires_model": True, "default_model": "gpt-4", "config_fields": [{"name": "api_key", "type": "password", "label": "API Key"}]},
    ]


@router.get("/config/data_source_types")
async def list_data_source_types():
    return [
        {"id": "bacbo", "name": "Bac Bo", "description": "API oficial do Bac Bo", "requires_config": False},
        {"id": "rest_api", "name": "API REST", "description": "API REST genérica", "requires_config": True, "config_fields": [{"name": "url", "type": "string", "label": "URL da API"}]},
        {"id": "websocket", "name": "WebSocket", "description": "WebSocket em tempo real", "requires_config": True, "config_fields": [{"name": "url", "type": "string", "label": "URL do WebSocket"}]},
        {"id": "custom", "name": "Customizado", "description": "Implemente seu próprio coletor", "requires_config": True, "config_fields": []},
    ]


@router.post("/config/reset")
async def reset_config():
    try:
        settings.__init__()
        return {"success": True, "message": "Configuração resetada para padrão"}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/config/validate")
async def validate_config():
    errors = []
    if not settings.llm.model:
        errors.append("Modelo LLM não configurado")
    if settings.data_source.enabled:
        if settings.data_source.type == "rest_api" and not settings.data_source.rest_url:
            errors.append("URL da API REST não configurada")
        if settings.data_source.type == "websocket" and not settings.data_source.ws_url:
            errors.append("URL do WebSocket não configurada")
    return {"valid": len(errors) == 0, "errors": errors, "warnings": []}
