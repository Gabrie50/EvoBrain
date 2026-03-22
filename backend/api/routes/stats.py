from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
async def get_stats():
    from main import evobrain

    return evobrain.get_stats()


@router.get("/stats/summary")
async def get_stats_summary():
    from main import evobrain

    stats = evobrain.get_stats()
    return {
        "status": stats.get("status"),
        "accuracy": stats.get("simulation", {}).get("accuracy", 0),
        "active_agents": stats.get("simulation", {}).get("active_agents", 0),
        "total_agents": stats.get("generation", {}).get("total_agents", 0),
        "predictions_made": stats.get("simulation", {}).get("predictions_made", 0),
    }
