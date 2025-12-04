"""Tests for chat endpoint."""
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.models import ChatMessage, ChatResponse
from backend.ai.agent import SRMAgent


@pytest.fixture
def mock_agent():
    """Create a mock agent."""
    agent = MagicMock(spec=SRMAgent)
    agent.chat.return_value = ChatResponse(
        response="مرحباً بك! كيف يمكنني مساعدتك؟",
        tool_calls=None
    )
    return agent


@pytest.fixture
def app_with_overrides(mock_agent):
    """Create app with dependency overrides."""
    from backend.main import app
    from backend.api import deps
    
    # Override dependencies
    app.dependency_overrides[deps.get_agent] = lambda: mock_agent
    
    yield app
    
    # Clean up
    app.dependency_overrides.clear()


def test_chat_endpoint_valid_request(app_with_overrides, mock_agent):
    """Test chat endpoint with valid request."""
    client = TestClient(app_with_overrides)
    
    request_data = {
        "message": "مرحبا",
        "history": []
    }
    
    response = client.post("/api/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "مرحباً بك! كيف يمكنني مساعدتك؟"


def test_chat_endpoint_with_history(app_with_overrides, mock_agent):
    """Test chat endpoint with history."""
    mock_agent.chat.return_value = ChatResponse(
        response="شكراً لك",
        tool_calls=None
    )
    
    client = TestClient(app_with_overrides)
    
    request_data = {
        "message": "رقم CIL: 1071324-101",
        "history": [
            {"role": "user", "content": "مرحبا"},
            {"role": "assistant", "content": "مرحباً بك!"}
        ]
    }
    
    response = client.post("/api/chat", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_chat_endpoint_invalid_request(app_with_overrides, mock_agent):
    """Test chat endpoint with invalid request."""
    mock_agent.chat.side_effect = Exception("Test error")
    
    client = TestClient(app_with_overrides)
    
    request_data = {
        "message": "test"
    }
    
    response = client.post("/api/chat", json=request_data)
    
    # Should return 500 if exception is raised
    assert response.status_code == 500

