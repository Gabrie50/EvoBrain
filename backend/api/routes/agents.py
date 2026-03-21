from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/agents")
async def list_agents():
    """Lista todos os agentes"""
    from main import evobrain
    return evobrain.list_agents()


@router.get("/agents/{agent_name}")
async def get_agent(agent_name: str):
    """Retorna detalhes de um agente"""
    from main import evobrain
    
    agent = evobrain.generator.get_agent(agent_name) if evobrain.generator else None
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Busca estatísticas do agente RL
    rl_agent = None
    if evobrain.simulation and agent_name in evobrain.simulation.rl_agents:
        rl_agent = evobrain.simulation.rl_agents[agent_name]
    
    return {
        'profile': {
            'id': agent.id,
            'name': agent.name,
            'personality': agent.personality,
            'traits': agent.traits,
            'mbti': agent.mbti,
            'history': agent.history[:500],
            'position': agent.position
        },
        'stats': {
            'acertos': agent.acertos,
            'erros': agent.erros,
            'total_uso': agent.total_uso,
            'accuracy': agent.accuracy,
            'fitness': agent.fitness,
            'specializations': agent.specializations
        },
        'rl_stats': rl_agent.get_stats() if rl_agent else None
    }


@router.get("/agents/{agent_name}/stats")
async def get_agent_stats(agent_name: str):
    """Retorna estatísticas de um agente"""
    from main import evobrain
    
    agent = evobrain.generator.get_agent(agent_name) if evobrain.generator else None
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        'name': agent.name,
        'accuracy': agent.accuracy,
        'total_uses': agent.total_uso,
        'acertos': agent.acertos,
        'erros': agent.erros,
        'fitness': agent.fitness,
        'specializations': agent.specializations,
        'personality': agent.personality
    }
