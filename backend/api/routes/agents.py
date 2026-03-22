from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/agents")
async def list_agents():
    from main import evobrain

    return [agent.to_dict() for agent in evobrain.list_agents()]


@router.get("/agents/{agent_name}")
async def get_agent(agent_name: str):
    from main import evobrain

    agent = evobrain.generator.get_agent(agent_name) if evobrain.generator else None
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.to_dict()


@router.get("/agents/{agent_name}/stats")
async def get_agent_stats(agent_name: str):
    from main import evobrain

    agent = evobrain.generator.get_agent(agent_name) if evobrain.generator else None
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    memories = getattr(agent, "memories", getattr(agent, "memory", []))
    long_term_memories = getattr(agent, "long_term_memories", getattr(agent, "long_term_memory", []))
    return {
        "name": agent.name,
        "accuracy": agent.accuracy,
        "total_uses": agent.total_uso,
        "acertos": agent.acertos,
        "erros": agent.erros,
        "fitness": agent.fitness,
        "specializations": agent.specializations,
        "memories_count": len(memories),
        "long_term_memories": len(long_term_memories),
    }
