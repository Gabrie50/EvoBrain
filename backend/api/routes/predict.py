from fastapi import APIRouter

router = APIRouter()


@router.get("/predict/current")
async def get_current_prediction():
    """Retorna previsão atual"""
    from main import evobrain
    return evobrain.get_prediction()


@router.get("/predict/history")
async def get_prediction_history(limit: int = 100):
    """Retorna histórico de previsões"""
    from main import evobrain
    if evobrain.simulation:
        return {
            'history': evobrain.simulation.get_prediction_history(limit),
            'limit': limit
        }
    return {'history': [], 'limit': limit}
