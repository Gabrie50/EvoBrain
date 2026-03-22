from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class ChatRequest(BaseModel):
    agent_name: str
    question: str


router = APIRouter()


@router.post("/chat/agent")
async def chat_with_agent(request: ChatRequest):
    from main import evobrain

    if not evobrain.chat_engine:
        raise HTTPException(status_code=503, detail="Chat engine not available")
    response = evobrain.chat_with_agent(request.agent_name, request.question)
    return {"response": response, "agent_name": request.agent_name}


@router.get("/chat/agents")
async def list_chat_agents():
    from main import evobrain

    if not evobrain.generator:
        return {"agents": []}
    agents = [
        {"name": agent.name, "id": agent.id, "personality": agent.personality[:100], "accuracy": agent.accuracy}
        for agent in evobrain.generator.get_all_agents()
    ]
    return {"agents": agents}
