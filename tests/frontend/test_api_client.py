"""Tests for frontend API client."""
import pytest
from unittest.mock import patch, MagicMock
from frontend.api_client import SRMAPIClient


class TestSRMAPIClient:
    """Tests for SRM API client."""
    
    @pytest.fixture
    def api_client(self):
        """Create API client instance."""
        return SRMAPIClient(base_url="http://localhost:8000")
    
    @patch('httpx.Client.get')
    def test_api_client_health_check_success(self, mock_get, api_client):
        """Test health check - success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = api_client.health_check()
        
        assert result is True
        mock_get.assert_called_once_with("http://localhost:8000/api/health")
    
    @patch('httpx.Client.get')
    def test_api_client_health_check_failure(self, mock_get, api_client):
        """Test health check - failure."""
        mock_get.side_effect = Exception("Connection failed")
        
        result = api_client.health_check()
        
        assert result is False
    
    @patch('httpx.Client.post')
    def test_api_client_chat(self, mock_post, api_client):
        """Test chat method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": "مرحباً بك!",
            "tool_calls": None
        }
        mock_post.return_value = mock_response
        
        result = api_client.chat("مرحبا", [])
        
        assert result["response"] == "مرحباً بك!"
        mock_post.assert_called_once()
    
    @patch('httpx.Client.post')
    def test_api_client_extract_cil(self, mock_post, api_client):
        """Test CIL extraction."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "data": {"cil": "1071324-101"},
            "error": None
        }
        mock_post.return_value = mock_response
        
        result = api_client.extract_cil(b"fake_image_data")
        
        assert result["success"] is True
        assert result["data"]["cil"] == "1071324-101"
        mock_post.assert_called_once()
    
    @patch('httpx.Client.post')
    def test_api_client_extract_bill_info(self, mock_post, api_client):
        """Test bill info extraction."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "cil": "1071324-101",
                "name": "Test User",
                "amount_due": 150.50
            },
            "error": None
        }
        mock_post.return_value = mock_response
        
        result = api_client.extract_bill_info(b"fake_image_data")
        
        assert result["success"] is True
        assert result["data"]["cil"] == "1071324-101"
        assert result["data"]["name"] == "Test User"
        mock_post.assert_called_once()


