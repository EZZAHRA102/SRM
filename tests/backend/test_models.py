"""Tests for Pydantic models."""
import pytest
from datetime import date
from pydantic import ValidationError

from backend.models import (
    User, Zone, ChatMessage, ChatRequest, ChatResponse,
    PaymentStatus, ServiceStatus, ServiceType, MaintenanceStatus,
    CILExtraction, BillInfo, OCRResult
)


class TestUserModel:
    """Tests for User model."""
    
    def test_valid_user(self, sample_user_paid):
        """Test creating a valid user."""
        assert sample_user_paid.cil == "1071324-101"
        assert sample_user_paid.payment_status == PaymentStatus.PAID
        assert sample_user_paid.service_type == ServiceType.BOTH
    
    def test_invalid_cil_format_no_dash(self):
        """Test CIL validation - missing dash."""
        with pytest.raises(ValidationError) as exc_info:
            User(
                cil="1071324101",
                name="Test User",
                address="Test Address",
                phone="0612345678",
                service_type=ServiceType.WATER,
                zone_id=1,
                payment_status=PaymentStatus.PAID,
                last_payment_date=date(2024, 11, 15),
                outstanding_balance=0.0,
                service_status=ServiceStatus.ACTIVE
            )
        assert "CIL must be in format" in str(exc_info.value)
    
    def test_invalid_cil_format_wrong_length(self):
        """Test CIL validation - wrong digit count."""
        with pytest.raises(ValidationError) as exc_info:
            User(
                cil="12345-101",
                name="Test User",
                address="Test Address",
                phone="0612345678",
                service_type=ServiceType.WATER,
                zone_id=1,
                payment_status=PaymentStatus.PAID,
                last_payment_date=date(2024, 11, 15),
                outstanding_balance=0.0,
                service_status=ServiceStatus.ACTIVE
            )
        assert "CIL must be in format" in str(exc_info.value)
    
    def test_invalid_cil_format_non_digits(self):
        """Test CIL validation - non-digit characters."""
        with pytest.raises(ValidationError) as exc_info:
            User(
                cil="1071324-ABC",
                name="Test User",
                address="Test Address",
                phone="0612345678",
                service_type=ServiceType.WATER,
                zone_id=1,
                payment_status=PaymentStatus.PAID,
                last_payment_date=date(2024, 11, 15),
                outstanding_balance=0.0,
                service_status=ServiceStatus.ACTIVE
            )
        assert "CIL must contain only digits" in str(exc_info.value)
    
    def test_negative_outstanding_balance(self):
        """Test validation - negative balance should fail."""
        with pytest.raises(ValidationError) as exc_info:
            User(
                cil="1071324-101",
                name="Test User",
                address="Test Address",
                phone="0612345678",
                service_type=ServiceType.WATER,
                zone_id=1,
                payment_status=PaymentStatus.PAID,
                last_payment_date=date(2024, 11, 15),
                outstanding_balance=-100.0,
                service_status=ServiceStatus.ACTIVE
            )
        assert "greater than or equal to 0" in str(exc_info.value)
    
    def test_user_enum_values(self, sample_user_paid):
        """Test enum values are correct."""
        assert sample_user_paid.payment_status.value == "مدفوع"
        assert sample_user_paid.service_status.value == "نشط"
        assert sample_user_paid.service_type.value == "ماء وكهرباء"


class TestZoneModel:
    """Tests for Zone model."""
    
    def test_valid_zone_with_maintenance(self, sample_zone_maintenance):
        """Test creating a valid zone with maintenance."""
        assert sample_zone_maintenance.zone_id == 1
        assert sample_zone_maintenance.maintenance_status == MaintenanceStatus.IN_PROGRESS
        assert sample_zone_maintenance.outage_reason is not None
    
    def test_valid_zone_no_maintenance(self, sample_zone_no_maintenance):
        """Test creating a valid zone without maintenance."""
        assert sample_zone_no_maintenance.maintenance_status == MaintenanceStatus.NONE
        assert sample_zone_no_maintenance.outage_reason is None
    
    def test_zone_enum_values(self, sample_zone_maintenance):
        """Test enum values are correct."""
        assert sample_zone_maintenance.maintenance_status.value == "جاري الصيانة"


class TestChatModels:
    """Tests for chat models."""
    
    def test_chat_message_valid(self):
        """Test creating a valid chat message."""
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
    
    def test_chat_request_valid(self):
        """Test creating a valid chat request."""
        request = ChatRequest(
            message="رقم CIL الخاص بي هو: 1071324-101",
            history=[]
        )
        assert request.message == "رقم CIL الخاص بي هو: 1071324-101"
        assert len(request.history) == 0
    
    def test_chat_request_with_history(self):
        """Test chat request with history."""
        history = [
            ChatMessage(role="user", content="Hello"),
            ChatMessage(role="assistant", content="Hi there")
        ]
        request = ChatRequest(message="Test", history=history)
        assert len(request.history) == 2
    
    def test_chat_response_valid(self):
        """Test creating a valid chat response."""
        response = ChatResponse(
            response="شكراً لك",
            tool_calls=None
        )
        assert response.response == "شكراً لك"
        assert response.tool_calls is None


class TestOCRModels:
    """Tests for OCR models."""
    
    def test_cil_extraction_valid(self):
        """Test creating a valid CIL extraction."""
        extraction = CILExtraction(cil="1071324-101")
        assert extraction.cil == "1071324-101"
    
    def test_bill_info_partial(self):
        """Test creating bill info with partial data."""
        bill_info = BillInfo(
            cil="1071324-101",
            name="Test User",
            amount_due=150.50
        )
        assert bill_info.cil == "1071324-101"
        assert bill_info.name == "Test User"
        assert bill_info.amount_due == 150.50
        assert bill_info.due_date is None
    
    def test_bill_info_negative_amount(self):
        """Test validation - negative amount should fail."""
        with pytest.raises(ValidationError) as exc_info:
            BillInfo(
                cil="1071324-101",
                amount_due=-100.0
            )
        assert "greater than or equal to 0" in str(exc_info.value)
    
    def test_ocr_result_success(self):
        """Test OCR result with success."""
        bill_info = BillInfo(cil="1071324-101", amount_due=150.50)
        result = OCRResult(success=True, data=bill_info, error=None)
        assert result.success is True
        assert result.data is not None
        assert result.error is None
    
    def test_ocr_result_failure(self):
        """Test OCR result with failure."""
        result = OCRResult(
            success=False,
            data=None,
            error="Failed to extract text"
        )
        assert result.success is False
        assert result.data is None
        assert result.error == "Failed to extract text"


