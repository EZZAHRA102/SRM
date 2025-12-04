"""Chat endpoint."""
import logging
from fastapi import APIRouter, Depends, HTTPException
from backend.models import ChatRequest, ChatResponse
from backend.api.deps import get_agent
from backend.ai.agent import SRMAgent

logger = logging.getLogger(__name__)
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
    logger.info("=" * 60)
    logger.info("Chat API Request: /chat")
    logger.info(f"User message length: {len(request.message)} chars")
    logger.info(f"Chat history: {len(request.history)} previous messages")
    logger.debug(f"User message: {request.message[:200]}...")
    
    try:
        response = agent.chat(
            message=request.message,
            history=request.history
        )
        
        logger.info(f"Chat response generated: {len(response.response)} chars")
        logger.info(f"Tool calls made: {len(response.tool_calls) if response.tool_calls else 0}")
        logger.info("=" * 60)
        
        return response
    except Exception as e:
        logger.error(f"Chat processing failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


