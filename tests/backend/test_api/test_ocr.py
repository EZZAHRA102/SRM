"""Tests for OCR endpoints."""
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.models import OCRResult, BillInfo
from backend.services import OCRService


@pytest.fixture
def mock_ocr_service():
    """Create a mock OCR service."""
    service = MagicMock(spec=OCRService)
    service.extract_cil.return_value = OCRResult(
        success=True,
        data=BillInfo(cil="1071324-101"),
        error=None
    )
    service.extract_bill_info.return_value = OCRResult(
        success=True,
        data=BillInfo(
            cil="1071324-101",
            name="Test User",
            amount_due=150.50
        ),
        error=None
    )
    return service


@pytest.fixture
def app_with_ocr_overrides(mock_ocr_service):
    """Create app with OCR dependency overrides."""
    from backend.main import app
    from backend.api import deps
    
    # Override dependencies
    app.dependency_overrides[deps.get_ocr_service] = lambda: mock_ocr_service
    
    yield app
    
    # Clean up
    app.dependency_overrides.clear()


def test_ocr_extract_cil_endpoint(app_with_ocr_overrides, mock_ocr_service):
    """Test CIL extraction endpoint."""
    client = TestClient(app_with_ocr_overrides)
    
    # Create a fake image file
    files = {"file": ("test.jpg", b"fake_image_data", "image/jpeg")}
    
    response = client.post("/api/ocr/extract-cil", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["cil"] == "1071324-101"


def test_ocr_extract_bill_endpoint(app_with_ocr_overrides, mock_ocr_service):
    """Test bill info extraction endpoint."""
    client = TestClient(app_with_ocr_overrides)
    
    # Create a fake image file
    files = {"file": ("test.jpg", b"fake_image_data", "image/jpeg")}
    
    response = client.post("/api/ocr/extract-bill", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["cil"] == "1071324-101"
    assert data["data"]["name"] == "Test User"

