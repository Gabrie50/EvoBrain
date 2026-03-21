from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()


@router.get("/report/generate")
async def generate_report(type: str = Query("full", description="full|summary|detailed")):
    """Gera relatório da simulação"""
    from main import evobrain
    
    if not evobrain.reporter:
        return {'report': 'Report generator not available'}
    
    stats = evobrain.get_stats()
    
    if type == "summary":
        report = evobrain.reporter.generate_summary(stats)
    elif type == "detailed":
        report = evobrain.reporter.generate_detailed_analysis(stats)
    else:
        report = evobrain.generate_report()
    
    return {
        'type': type,
        'report': report,
        'timestamp': __import__('time').time()
    }


@router.get("/report/summary")
async def get_summary():
    """Retorna resumo executivo"""
    from main import evobrain
    
    if not evobrain.reporter:
        return {'summary': 'Report generator not available'}
    
    stats = evobrain.get_stats()
    summary = evobrain.reporter.generate_summary(stats)
    
    return {
        'summary': summary,
        'stats': {
            'accuracy': stats.get('simulation', {}).get('accuracy', 0),
            'active_agents': stats.get('simulation', {}).get('active_agents', 0),
            'total_predictions': stats.get('simulation', {}).get('predictions_made', 0)
        }
    }
