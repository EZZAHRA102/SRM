"""Tests for AI agent."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.ai.agent import SRMAgent
from backend.config import Settings
from backend.services import UserService, MaintenanceService
from backend.repositories import MockRepository
from backend.models import ChatMessage


class TestSRMAgent:
    """Tests for SRM Agent."""
    
    @pytest.fixture
    def settings(self):
        """Create mock settings."""
        settings = Settings()
        settings.azure_openai_endpoint = "https://test.openai.azure.com/"
        settings.azure_openai_api_key = "test-key"
        settings.azure_openai_api_version = "2024-08-01-preview"
        settings.azure_openai_deployment_name = "gpt-4o"
        return settings
    
    @pytest.fixture
    def user_service(self):
        """Create user service."""
        repository = MockRepository()
        return UserService(repository)
    
    @pytest.fixture
    def maintenance_service(self):
        """Create maintenance service."""
        repository = MockRepository()
        return MaintenanceService(repository)
    
    @pytest.fixture
    def agent(self, settings, user_service, maintenance_service):
        """Create agent."""
        return SRMAgent(settings, user_service, maintenance_service)
    
    @patch('backend.ai.agent.AzureChatOpenAI')
    def test_agent_initialization(self, mock_llm_class, agent):
        """Test agent initialization."""
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm_class.return_value = mock_llm
        
        success = agent.initialize()
        
        assert success is True
        assert agent._llm is not None
        assert agent._tools is not None
        assert len(agent._tools) == 2
    
    @patch('backend.ai.agent.AzureChatOpenAI')
    def test_agent_initialization_failure(self, mock_llm_class, agent):
        """Test agent initialization failure."""
        mock_llm_class.side_effect = Exception("Connection failed")
        
        success = agent.initialize()
        
        assert success is False
    
    @patch('backend.ai.agent.AzureChatOpenAI')
    def test_agent_chat_basic(self, mock_llm_class, agent):
        """Test basic chat without tool calls."""
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = "مرحباً بك! كيف يمكنني مساعدتك؟"
        mock_response.tool_calls = None
        
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = mock_response
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm_class.return_value = mock_llm
        
        agent.initialize()
        
        history = []
        response = agent.chat("مرحبا", history)
        
        assert response.response == "مرحباً بك! كيف يمكنني مساعدتك؟"
        assert response.tool_calls is None
    
    @patch('backend.ai.agent.AzureChatOpenAI')
    def test_agent_chat_with_tool_calls(self, mock_llm_class, agent):
        """Test chat with tool calls."""
        # Mock first response (with tool call)
        mock_tool_response = MagicMock()
        mock_tool_response.tool_calls = [{
            'name': 'check_payment',
            'args': {'cil': '1071324-101'},
            'id': 'call_123'
        }]
        
        # Mock final response (after tool execution)
        mock_final_response = MagicMock()
        mock_final_response.content = "حالة الدفع: مدفوع"
        
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = [mock_tool_response, mock_final_response]
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm_class.return_value = mock_llm
        
        agent.initialize()
        
        history = []
        response = agent.chat("رقم CIL الخاص بي: 1071324-101", history)
        
        assert response.response == "حالة الدفع: مدفوع"
        assert response.tool_calls is not None
        assert len(response.tool_calls) == 1
    
    def test_agent_chat_not_initialized(self, agent):
        """Test chat when agent not initialized."""
        history = []
        response = agent.chat("مرحبا", history)
        
        assert "لم يتم تهيئة" in response.response
    
    @patch('backend.ai.agent.AzureChatOpenAI')
    def test_agent_build_messages(self, mock_llm_class, agent):
        """Test message building."""
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm_class.return_value = mock_llm
        
        agent.initialize()
        
        history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi")
        ]
        
        messages = agent._build_messages("Test", history)
        
        assert len(messages) == 4  # System + 2 history + 1 current
        assert "SRM" in messages[0].content or "مساعد" in messages[0].content  # System message check
    
    @patch('backend.ai.agent.AzureChatOpenAI')
    def test_agent_execute_tools(self, mock_llm_class, agent):
        """Test tool execution."""
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm_class.return_value = mock_llm
        
        agent.initialize()
        
        tool_calls = [{
            'name': 'check_payment',
            'args': {'cil': '1071324-101'},
            'id': 'call_123'
        }]
        
        tool_messages = agent._execute_tools(tool_calls)
        
        assert len(tool_messages) == 1
        assert tool_messages[0].tool_call_id == 'call_123'
        assert "معلومات العميل" in tool_messages[0].content

