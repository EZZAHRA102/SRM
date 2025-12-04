"""Tests for AI tools."""
import pytest
from unittest.mock import Mock, patch
from backend.ai.tools import create_payment_tool, create_maintenance_tool
from backend.services import UserService, MaintenanceService
from backend.repositories import MockRepository


class TestAITools:
    """Tests for AI tool creation."""
    
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
    
    def test_create_payment_tool(self, user_service):
        """Test payment tool creation."""
        tool = create_payment_tool(user_service)
        
        assert tool is not None
        assert tool.name == "check_payment"
        assert callable(tool.invoke)
    
    def test_payment_tool_returns_correct_format(self, user_service):
        """Test payment tool returns correct format."""
        tool = create_payment_tool(user_service)
        
        result = tool.invoke({"cil": "1071324-101"})
        
        assert isinstance(result, str)
        assert "معلومات العميل" in result
        assert "1071324-101" in result or "Abdenbi" in result
    
    def test_payment_tool_user_not_found(self, user_service):
        """Test payment tool handles user not found."""
        tool = create_payment_tool(user_service)
        
        result = tool.invoke({"cil": "9999999-999"})
        
        assert isinstance(result, str)
        assert "لم يتم العثور" in result
    
    def test_create_maintenance_tool(self, maintenance_service):
        """Test maintenance tool creation."""
        tool = create_maintenance_tool(maintenance_service)
        
        assert tool is not None
        assert tool.name == "check_maintenance"
        assert callable(tool.invoke)
    
    def test_maintenance_tool_returns_correct_format(self, maintenance_service):
        """Test maintenance tool returns correct format."""
        tool = create_maintenance_tool(maintenance_service)
        
        result = tool.invoke({"cil": "1071324-101"})
        
        assert isinstance(result, str)
        assert "منطقتك" in result or "صيانة" in result
    
    def test_maintenance_tool_user_not_found(self, maintenance_service):
        """Test maintenance tool handles user not found."""
        tool = create_maintenance_tool(maintenance_service)
        
        result = tool.invoke({"cil": "9999999-999"})
        
        assert isinstance(result, str)
        assert "لم يتم العثور" in result


