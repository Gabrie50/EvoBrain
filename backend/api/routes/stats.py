from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
async def get_stats():
    """Retorna estatísticas completas"""
    from main import evobrain
    return evobrain.get_stats()


@router.get("/stats/summary")
async def get_stats_summary():
    """Retorna resumo das estatísticas"""
    from main import evobrain
    stats = evobrain.get_stats()
    
    return {
        'status': stats.get('status'),
        'accuracy': stats.get('simulation', {}).get('accuracy', 0),
        'active_agents': stats.get('simulation', {}).get('active_agents', 0),
        'total_agents': stats.get('generation', {}).get('total_agents', 0),
        'predictions_made': stats.get('simulation', {}).get('predictions_made', 0),
        'uptime_hours': stats.get('uptime', 0) / 3600
    }


@router.get("/stats/agents")
async def get_agents_stats():
    """Estatísticas dos agentes"""
    from main import evobrain
    stats = evobrain.get_stats()
    
    return {
        'active': stats.get('simulation', {}).get('active_agents', 0),
        'total_ever': stats.get('generation', {}).get('total_agents', 0),
        'pending': stats.get('generation', {}).get('pending', 0),
        'creation_rate': stats.get('generation', {}).get('created_last_minute', 0)
    }


@router.get("/stats/simulation")
async def get_simulation_stats():
    """Estatísticas da simulação"""
    from main import evobrain
    return evobrain.get_stats().get('simulation', {})
