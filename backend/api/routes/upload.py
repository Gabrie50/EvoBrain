from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional

router = APIRouter()


@router.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload de PDF para extração e geração de agentes"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Apenas arquivos PDF são permitidos")
    
    content = await file.read()
    
    from main import evobrain
    result = evobrain.process_pdf(content, file.filename)
    
    return result


@router.post("/upload/text")
async def upload_text(text: str):
    """Upload de texto para extração"""
    from main import evobrain
    
    result = evobrain.extractor.extract_from_text(text)
    
    return result


@router.get("/upload/status/{task_id}")
async def get_upload_status(task_id: str):
    """Status do processamento"""
    from main import evobrain
    
    # Por enquanto, retorna status básico
    stats = evobrain.get_stats()
    
    return {
        'task_id': task_id,
        'status': 'processing' if stats.get('generation', {}).get('pending', 0) > 0 else 'completed',
        'agents_created': stats.get('generation', {}).get('total_agents', 0),
        'pending_agents': stats.get('generation', {}).get('pending', 0)
    }
