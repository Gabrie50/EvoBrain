from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check básico"""
    return {"status": "ok", "service": "EvoBrain"}


@router.get("/health/detailed")
async def detailed_health():
    """Health check detalhado"""
    from main import evobrain
    return evobrain.get_stats()
