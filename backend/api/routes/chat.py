from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    agent_name: str
    question: str

class ChatResponse(BaseModel):
    response: str
    agent_name: str

router = APIRouter()


@router.post("/chat/agent", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Conversa com um agente"""
    from main import evobrain
    
    if not evobrain.chat_engine:
        raise HTTPException(status_code=503, detail="Chat engine not available")
    
    response = evobrain.chat_with_agent(request.agent_name, request.question)
    
    return ChatResponse(
        response=response,
        agent_name=request.agent_name
    )


@router.get("/chat/agents")
async def list_chat_agents():
    """Lista agentes disponíveis para chat"""
    from main import evobrain
    
    if not evobrain.generator:
        return {'agents': []}
    
    agents = []
    for agent in evobrain.generator.get_all_agents():
        agents.append({
            'name': agent.name,
            'id': agent.id,
            'personality': agent.personality[:100],
            'accuracy': agent.accuracy
        })
    
    return {'agents': agents}


@router.post("/chat/agent/{agent_name}/reset")
async def reset_chat(agent_name: str):
    """Reseta conversa com um agente"""
    from main import evobrain
    
    if evobrain.chat_engine:
        evobrain.chat_engine.reset_conversation(agent_name)
    
    return {'status': 'reset', 'agent': agent_name}
