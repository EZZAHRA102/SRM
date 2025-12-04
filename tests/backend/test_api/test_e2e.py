"""End-to-end tests for SRM API with real Azure integrations."""
import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.config import settings

# Test image path
TEST_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "picture", "test.jpg"
)

# Pytest markers
pytestmark = [
    pytest.mark.e2e,
    pytest.mark.slow
]


# ============================================================================
# Phase 1: Environment and Configuration Tests
# ============================================================================

def test_env_file_loading():
    """Test that .env file is loaded correctly."""
    # Settings should be loaded from .env
    assert settings is not None
    assert hasattr(settings, 'azure_openai_api_key')
    assert hasattr(settings, 'azure_document_intelligence_endpoint')


def test_azure_credentials_present():
    """Validate all Azure credentials are present."""
    missing_keys = []
    
    if not settings.azure_openai_api_key:
        missing_keys.append("AZURE_OPENAI_API_KEY")
    if not settings.azure_openai_endpoint:
        missing_keys.append("AZURE_OPENAI_ENDPOINT")
    if not settings.azure_document_intelligence_endpoint:
        missing_keys.append("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    if not settings.azure_document_intelligence_key:
        missing_keys.append("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    
    if missing_keys:
        pytest.skip(f"Missing Azure credentials: {', '.join(missing_keys)}")
    
    # Assert all credentials are present
    assert settings.azure_openai_api_key, "AZURE_OPENAI_API_KEY not set"
    assert settings.azure_openai_endpoint, "AZURE_OPENAI_ENDPOINT not set"
    assert settings.azure_document_intelligence_endpoint, "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT not set"
    assert settings.azure_document_intelligence_key, "AZURE_DOCUMENT_INTELLIGENCE_KEY not set"


def test_settings_object_construction():
    """Validate Settings object construction."""
    assert settings.azure_openai_deployment_name == "gpt-4o"
    assert settings.azure_openai_api_version == "2024-08-01-preview"
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8000


# ============================================================================
# Phase 2: Health Endpoint E2E Test
# ============================================================================

def test_health_endpoint_e2e():
    """Test health endpoint returns expected response."""
    client = TestClient(app)
    
    response = client.get("/api/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "SRM API"
    assert data["version"] == "1.0.0"


def test_root_endpoint_e2e():
    """Test root endpoint."""
    client = TestClient(app)
    
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"
    assert "docs" in data


# ============================================================================
# Phase 3: OCR Endpoints E2E Tests (Azure Document Intelligence)
# ============================================================================

@pytest.mark.skipif(
    not os.path.exists(TEST_IMAGE_PATH),
    reason="Test image not found"
)
def test_ocr_extract_cil_e2e():
    """Test CIL extraction endpoint with real Azure Document Intelligence."""
    client = TestClient(app)
    
    # Ensure test image exists
    assert os.path.exists(TEST_IMAGE_PATH), f"Test image not found at {TEST_IMAGE_PATH}"
    
    # Read test image
    with open(TEST_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
    
    # Make request
    files = {"file": ("test.jpg", image_bytes, "image/jpeg")}
    response = client.post("/api/ocr/extract-cil", files=files)
    
    # Validate response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.text}"
    data = response.json()
    
    # Validate structure
    assert "success" in data
    assert "data" in data or "error" in data
    
    # If successful, validate CIL extraction
    if data.get("success"):
        assert data["data"] is not None
        assert "cil" in data["data"]
        # Expected CIL from test image: 1071324-101
        assert data["data"]["cil"] == "1071324-101", f"Expected CIL '1071324-101', got '{data['data']['cil']}'"
        assert data["error"] is None
    else:
        # If failed, check error message
        assert data["error"] is not None
        pytest.fail(f"OCR extraction failed: {data.get('error')}")


@pytest.mark.skipif(
    not os.path.exists(TEST_IMAGE_PATH),
    reason="Test image not found"
)
def test_ocr_extract_bill_e2e():
    """Test full bill extraction endpoint with real Azure Document Intelligence."""
    client = TestClient(app)
    
    # Ensure test image exists
    assert os.path.exists(TEST_IMAGE_PATH), f"Test image not found at {TEST_IMAGE_PATH}"
    
    # Read test image
    with open(TEST_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
    
    # Make request
    files = {"file": ("test.jpg", image_bytes, "image/jpeg")}
    response = client.post("/api/ocr/extract-bill", files=files)
    
    # Validate response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.text}"
    data = response.json()
    
    # Validate structure
    assert "success" in data
    
    # If successful, validate bill extraction
    if data.get("success"):
        assert data["data"] is not None
        bill_info = data["data"]
        
        # Validate CIL (expected: 1071324-101)
        assert "cil" in bill_info
        assert bill_info["cil"] == "1071324-101", f"Expected CIL '1071324-101', got '{bill_info['cil']}'"
        
        # Validate customer name (if extracted, should be a non-empty string)
        # Note: Name extraction can vary, so we just validate it exists and is reasonable
        if "name" in bill_info and bill_info["name"]:
            name = bill_info["name"].strip()
            assert len(name) > 0, "Name should not be empty if extracted"
            # Name should contain letters (not just numbers or special chars)
            assert any(c.isalpha() for c in name), \
                f"Name should contain letters, got '{bill_info['name']}'"
        
        # Validate amount (expected: ~351.48)
        if "amount_due" in bill_info and bill_info["amount_due"] is not None:
            amount = bill_info["amount_due"]
            # Allow some tolerance (within 1 DH)
            assert abs(amount - 351.48) < 1.0, \
                f"Expected amount ~351.48, got {amount}"
        
        # Validate service type (should indicate water and/or electricity)
        if "service_type" in bill_info and bill_info["service_type"]:
            service_type = bill_info["service_type"]
            # Should contain water or electricity indicators
            assert len(service_type) > 0, "Service type should not be empty"
        
        # Validate raw_text exists
        assert "raw_text" in bill_info
        assert bill_info["raw_text"] is not None
        assert len(bill_info["raw_text"]) > 0, "Raw text should not be empty"
        
        assert data["error"] is None
    else:
        # If failed, check error message
        assert data["error"] is not None
        pytest.fail(f"Bill extraction failed: {data.get('error')}")


def test_ocr_extract_cil_invalid_image():
    """Test error handling with invalid image data."""
    client = TestClient(app)
    
    # Send invalid image data
    files = {"file": ("invalid.jpg", b"not an image", "image/jpeg")}
    response = client.post("/api/ocr/extract-cil", files=files)
    
    # Should return error (either 200 with success=False or 500)
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("success") is False or data.get("error") is not None


def test_ocr_extract_bill_invalid_image():
    """Test error handling with invalid image data for bill extraction."""
    client = TestClient(app)
    
    # Send invalid image data
    files = {"file": ("invalid.jpg", b"not an image", "image/jpeg")}
    response = client.post("/api/ocr/extract-bill", files=files)
    
    # Should return error (either 200 with success=False or 500)
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert data.get("success") is False or data.get("error") is not None


# ============================================================================
# Phase 4: Chat Endpoint E2E Tests (Azure OpenAI)
# ============================================================================

def test_chat_basic_greeting():
    """Test basic greeting message with Azure OpenAI."""
    client = TestClient(app)
    
    request_data = {
        "message": "مرحبا",
        "history": []
    }
    
    response = client.post("/api/chat", json=request_data)
    
    # Validate response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.text}"
    data = response.json()
    
    # Validate structure
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0, "Response should not be empty"
    
    # Response should be in Arabic (contains Arabic characters or is a greeting)
    # Just check it's not empty and is a string


def test_chat_cil_inquiry():
    """Test CIL inquiry that may trigger tool execution."""
    client = TestClient(app)
    
    request_data = {
        "message": "ما هي حالة الدفع لرقم CIL: 1071324-101؟",
        "history": []
    }
    
    response = client.post("/api/chat", json=request_data)
    
    # Validate response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.text}"
    data = response.json()
    
    # Validate structure
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0, "Response should not be empty"
    
    # May have tool_calls if agent decides to use payment tool
    if "tool_calls" in data:
        assert data["tool_calls"] is None or isinstance(data["tool_calls"], list)


def test_chat_with_history():
    """Test chat endpoint with conversation history."""
    client = TestClient(app)
    
    request_data = {
        "message": "شكراً لك",
        "history": [
            {"role": "user", "content": "مرحبا"},
            {"role": "assistant", "content": "مرحباً بك! كيف يمكنني مساعدتك؟"}
        ]
    }
    
    response = client.post("/api/chat", json=request_data)
    
    # Validate response
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.text}"
    data = response.json()
    
    # Validate structure
    assert "response" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0, "Response should not be empty"


def test_chat_invalid_request():
    """Test error handling for malformed requests."""
    client = TestClient(app)
    
    # Missing required field
    request_data = {
        "history": []
    }
    
    response = client.post("/api/chat", json=request_data)
    
    # Should return 422 (validation error) or 500
    assert response.status_code in [422, 500]


def test_chat_empty_message():
    """Test chat endpoint with empty message."""
    client = TestClient(app)
    
    request_data = {
        "message": "",
        "history": []
    }
    
    response = client.post("/api/chat", json=request_data)
    
    # May return 422 (validation error) or 200 with empty response
    assert response.status_code in [200, 422, 500]


# ============================================================================
# Phase 5: Integration Tests
# ============================================================================

@pytest.mark.skipif(
    not os.path.exists(TEST_IMAGE_PATH),
    reason="Test image not found"
)
def test_full_flow_ocr_then_chat():
    """Test full flow: OCR extracts CIL, then chat query about that CIL."""
    client = TestClient(app)
    
    # Step 1: Extract CIL from image
    with open(TEST_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
    
    files = {"file": ("test.jpg", image_bytes, "image/jpeg")}
    ocr_response = client.post("/api/ocr/extract-cil", files=files)
    
    assert ocr_response.status_code == 200
    ocr_data = ocr_response.json()
    
    if not ocr_data.get("success"):
        pytest.skip(f"OCR extraction failed: {ocr_data.get('error')}")
    
    extracted_cil = ocr_data["data"]["cil"]
    assert extracted_cil == "1071324-101", f"Expected CIL '1071324-101', got '{extracted_cil}'"
    
    # Step 2: Query chat about the extracted CIL
    chat_request = {
        "message": f"ما هي حالة الدفع لرقم CIL: {extracted_cil}؟",
        "history": []
    }
    
    chat_response = client.post("/api/chat", json=chat_request)
    
    # Validate chat response
    assert chat_response.status_code == 200, \
        f"Chat request failed with status {chat_response.status_code}: {chat_response.text}"
    
    chat_data = chat_response.json()
    assert "response" in chat_data
    assert isinstance(chat_data["response"], str)
    assert len(chat_data["response"]) > 0, "Chat response should not be empty"
    
    # The response should acknowledge the CIL or provide information
    # (exact content depends on Azure OpenAI and tool execution)


def test_full_flow_bill_extraction_then_chat():
    """Test full flow: Extract full bill info, then query about payment."""
    client = TestClient(app)
    
    # Step 1: Extract full bill information
    with open(TEST_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()
    
    files = {"file": ("test.jpg", image_bytes, "image/jpeg")}
    ocr_response = client.post("/api/ocr/extract-bill", files=files)
    
    assert ocr_response.status_code == 200
    ocr_data = ocr_response.json()
    
    if not ocr_data.get("success"):
        pytest.skip(f"Bill extraction failed: {ocr_data.get('error')}")
    
    bill_info = ocr_data["data"]
    assert "cil" in bill_info
    cil = bill_info["cil"]
    
    # Step 2: Query chat about payment status
    chat_request = {
        "message": f"ما هو المبلغ المستحق لرقم CIL: {cil}؟",
        "history": []
    }
    
    chat_response = client.post("/api/chat", json=chat_request)
    
    # Validate chat response
    assert chat_response.status_code == 200, \
        f"Chat request failed with status {chat_response.status_code}: {chat_response.text}"
    
    chat_data = chat_response.json()
    assert "response" in chat_data
    assert isinstance(chat_data["response"], str)
    assert len(chat_data["response"]) > 0, "Chat response should not be empty"

