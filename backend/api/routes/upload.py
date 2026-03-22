from fastapi import APIRouter, Body, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Apenas arquivos PDF são permitidos")
    content = await file.read()
    from main import evobrain

    result = evobrain.process_pdf(content, file.filename)
    return result


@router.post("/upload/text")
async def upload_text(text: str = Body(..., embed=True)):
    from main import evobrain

    result = evobrain.process_text(text, "api")
    return result


@router.post("/upload/url")
async def upload_url(url: str = Body(..., embed=True)):
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        from main import evobrain

        result = evobrain.process_text(text, url)
        return result
    except Exception as exc:
        raise HTTPException(400, f"Erro ao acessar URL: {exc}") from exc


@router.get("/upload/status")
async def get_upload_status():
    from main import evobrain

    if evobrain.continuous_learning:
        return evobrain.continuous_learning.get_statistics()
    return {"status": "not_initialized"}
