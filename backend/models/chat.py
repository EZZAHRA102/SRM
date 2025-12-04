"""Chat domain models."""
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "رقم CIL الخاص بي هو: 1071324-101"
            }
        }


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., description="User message")
    history: List[ChatMessage] = Field(default_factory=list, description="Chat history")
    language: str = Field(default="ar", description="Language: 'ar' or 'fr'")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "message": "رقم CIL الخاص بي هو: 1071324-101",
                "history": []
            }
        }


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="Assistant response")
    tool_calls: Optional[List[dict[str, Any]]] = Field(None, description="Tool calls made during processing")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "response": "شكراً لك. دعني أتحقق من حالة الدفع...",
                "tool_calls": None
            }
        }


