"""Chat endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from backend.models import ChatRequest, ChatResponse
from backend.api.deps import get_agent
from backend.ai.agent import SRMAgent

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent: SRMAgent = Depends(get_agent)
) -> ChatResponse:
    """
    Process a chat message and return AI response.
    
    Args:
        request: Chat request with message and history
        agent: SRM agent instance
        
    Returns:
        ChatResponse with agent response
        
    Raises:
        HTTPException: If chat processing fails
    """
    try:
        response = agent.chat(
            message=request.message,
            history=request.history
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


