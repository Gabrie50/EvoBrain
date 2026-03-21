from html.parser import HTMLParser
from urllib.request import Request, urlopen

from fastapi import APIRouter, Body, File, HTTPException, UploadFile

router = APIRouter()


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str):
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)

    def get_text(self) -> str:
        return " ".join(self.parts)


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload de PDF para extração e geração de agentes."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Apenas arquivos PDF são permitidos")
    content = await file.read()
    from main import evobrain

    return evobrain.process_pdf(content, file.filename)


@router.post("/upload/text")
async def upload_text(text: str = Body(..., embed=True)):
    """Upload de texto para extração e geração de agentes."""
    from main import evobrain

    return evobrain.process_text(text, "api")


@router.post("/upload/url")
async def upload_url(url: str = Body(..., embed=True)):
    """Processa texto de uma URL simples."""
    try:
        request = Request(url, headers={"User-Agent": "EvoBrain/1.0"})
        with urlopen(request, timeout=10) as response:
            html = response.read().decode("utf-8", errors="ignore")
        parser = _TextExtractor()
        parser.feed(html)
        text = parser.get_text()
        from main import evobrain

        return evobrain.process_text(text, url)
    except Exception as exc:
        raise HTTPException(400, f"Erro ao acessar URL: {exc}") from exc


@router.get("/upload/status")
async def get_upload_status():
    """Status do processamento contínuo."""
    from main import evobrain

    stats = evobrain.get_stats()
    return {
        "status": stats.get("status", "not_initialized"),
        "agents_created": stats.get("generation", {}).get("total_agents", 0),
        "pending_agents": stats.get("generation", {}).get("pending", 0),
    }


@router.get("/upload/status/{task_id}")
async def get_upload_status_by_task(task_id: str):
    """Mantém compatibilidade com o endpoint antigo de status."""
    from main import evobrain

    stats = evobrain.get_stats()
    return {
        "task_id": task_id,
        "status": "processing" if stats.get("generation", {}).get("pending", 0) > 0 else "completed",
        "agents_created": stats.get("generation", {}).get("total_agents", 0),
        "pending_agents": stats.get("generation", {}).get("pending", 0),
    }
