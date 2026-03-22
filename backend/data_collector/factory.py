"""Fábrica de coletores de dados."""

from __future__ import annotations

from typing import Optional

from config import settings
from data_collector.bacbo_collector import BacBoCollector
from data_collector.base import BaseDataCollector
from data_collector.custom_collector import CustomDataCollector
from data_collector.rest_api_collector import RESTAPICollector
from data_collector.websocket_collector import WebSocketCollector
from utils.logger import get_logger

logger = get_logger(__name__)


def create_data_collector() -> Optional[BaseDataCollector]:
    source_type = settings.data_source.type.lower()
    if source_type == "bacbo":
        logger.info("📡 Usando coletor Bac Bo")
        return BacBoCollector()
    if source_type == "websocket":
        logger.info(f"📡 Usando coletor WebSocket: {settings.data_source.ws_url}")
        return WebSocketCollector(url=settings.data_source.ws_url, headers=settings.data_source.ws_headers)
    if source_type == "rest_api":
        logger.info(f"📡 Usando coletor REST API: {settings.data_source.rest_url}")
        return RESTAPICollector(
            url=settings.data_source.rest_url,
            headers=settings.data_source.rest_headers,
            params=settings.data_source.rest_params,
            interval=settings.data_source.interval,
        )
    if source_type == "custom":
        logger.info("📡 Usando coletor customizado")
        return CustomDataCollector({})
    logger.warning(f"⚠️ Tipo de data source desconhecido: {source_type}")
    return None
