"""Tests for service layer."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services import UserService, MaintenanceService, OCRService
from backend.repositories import MockRepository
from backend.models import PaymentStatus, ServiceStatus, MaintenanceStatus


class TestUserService:
    """Tests for UserService."""
    
    @pytest.fixture
    def repository(self):
        """Create mock repository."""
        return MockRepository()
    
    @pytest.fixture
    def user_service(self, repository):
        """Create user service."""
        return UserService(repository)
    
    def test_get_user_found(self, user_service):
        """Test getting an existing user."""
        user = user_service.get_user("1071324-101")
        
        assert user is not None
        assert user.cil == "1071324-101"
        assert user.name == "Abdenbi EL MARZOUKI"
    
    def test_get_user_not_found(self, user_service):
        """Test getting a non-existent user."""
        user = user_service.get_user("9999999-999")
        
        assert user is None
    
    def test_check_payment_paid_user(self, user_service):
        """Test payment check for paid user."""
        result = user_service.check_payment("1071324-101")
        
        assert result.user is not None
        assert result.is_paid is True
        assert result.user.payment_status == PaymentStatus.PAID
        assert "✅" in result.message
        assert "مدفوع" in result.message
    
    def test_check_payment_unpaid_user(self, user_service):
        """Test payment check for unpaid user."""
        result = user_service.check_payment("5029012-505")
        
        assert result.user is not None
        assert result.is_paid is False
        assert result.user.payment_status == PaymentStatus.UNPAID
        assert "⚠️" in result.message
        assert "غير مدفوع" in result.message
        assert "890" in result.message  # Outstanding balance
    
    def test_check_payment_user_not_found(self, user_service):
        """Test payment check for non-existent user."""
        result = user_service.check_payment("9999999-999")
        
        assert result.user is None
        assert result.is_paid is False
        assert "لم يتم العثور" in result.message


class TestMaintenanceService:
    """Tests for MaintenanceService."""
    
    @pytest.fixture
    def repository(self):
        """Create mock repository."""
        return MockRepository()
    
    @pytest.fixture
    def maintenance_service(self, repository):
        """Create maintenance service."""
        return MaintenanceService(repository)
    
    def test_check_maintenance_active(self, maintenance_service):
        """Test maintenance check for zone with active maintenance."""
        result = maintenance_service.check_maintenance("1071324-101")
        
        assert result.user is not None
        assert result.zone is not None
        assert result.has_maintenance is True
        assert result.zone.maintenance_status == MaintenanceStatus.IN_PROGRESS
        assert "⚙️" in result.message
        assert "جاري الصيانة" in result.message
        assert result.zone.outage_reason is not None
    
    def test_check_maintenance_none(self, maintenance_service):
        """Test maintenance check for zone with no maintenance."""
        result = maintenance_service.check_maintenance("1300994-101")
        
        assert result.user is not None
        assert result.zone is not None
        assert result.has_maintenance is False
        assert result.zone.maintenance_status == MaintenanceStatus.NONE
        assert "✅" in result.message
        assert "لا توجد صيانة" in result.message
    
    def test_check_maintenance_user_not_found(self, maintenance_service):
        """Test maintenance check for non-existent user."""
        result = maintenance_service.check_maintenance("9999999-999")
        
        assert result.user is None
        assert result.zone is None
        assert result.has_maintenance is False
        assert "لم يتم العثور" in result.message


class TestOCRService:
    """Tests for OCRService."""
    
    @pytest.fixture
    def ocr_service(self):
        """Create OCR service with mock credentials."""
        return OCRService(
            endpoint="https://test-endpoint.cognitiveservices.azure.com/",
            key="test-key"
        )
    
    def test_normalize_cil_format_correct(self, ocr_service):
        """Test CIL normalization - already correct format."""
        cil = "1071324-101"
        normalized = ocr_service._normalize_cil_format(cil)
        assert normalized == "1071324-101"
    
    def test_normalize_cil_format_reversed(self, ocr_service):
        """Test CIL normalization - reversed format."""
        cil = "101-1071324"
        normalized = ocr_service._normalize_cil_format(cil)
        assert normalized == "1071324-101"
    
    def test_extract_cil_from_text_with_label(self, ocr_service):
        """Test CIL extraction - with label prefix."""
        text = "CIL: 1071324-101"
        cil = ocr_service._extract_cil_from_text(text)
        assert cil == "1071324-101"
    
    def test_extract_cil_from_text_reversed(self, ocr_service):
        """Test CIL extraction - reversed format."""
        text = "CIL: 101-1071324"
        cil = ocr_service._extract_cil_from_text(text)
        assert cil == "1071324-101"  # Should be normalized
    
    def test_extract_cil_from_text_standalone(self, ocr_service):
        """Test CIL extraction - standalone."""
        text = "رقم العميل: 1071324-101"
        cil = ocr_service._extract_cil_from_text(text)
        assert cil == "1071324-101"
    
    def test_extract_cil_from_text_not_found(self, ocr_service):
        """Test CIL extraction - not found."""
        text = "This text has no CIL number"
        cil = ocr_service._extract_cil_from_text(text)
        assert cil is None
    
    def test_extract_name_from_text(self, ocr_service):
        """Test name extraction."""
        text = "Nom: Abdenbi EL MARZOUKI"
        name = ocr_service._extract_name_from_text(text)
        assert name == "Abdenbi EL MARZOUKI"
    
    def test_extract_amount_from_text(self, ocr_service):
        """Test amount extraction."""
        text = "Total Encaissé Dirhams: 351.48"
        amount = ocr_service._extract_amount_from_text(text)
        assert amount == 351.48
    
    def test_extract_date_from_text(self, ocr_service):
        """Test date extraction."""
        text = "Date du paiement: 10-07-2013"
        date_str = ocr_service._extract_date_from_text(text)
        assert date_str == "10-07-2013"
    
    def test_extract_service_type_water(self, ocr_service):
        """Test service type extraction - water."""
        text = "Eau et Assainissement"
        service_type = ocr_service._extract_service_type_from_text(text)
        assert service_type == "ماء"
    
    def test_extract_service_type_electricity(self, ocr_service):
        """Test service type extraction - electricity."""
        text = "Électricité"
        service_type = ocr_service._extract_service_type_from_text(text)
        assert service_type == "كهرباء"
    
    def test_extract_service_type_both(self, ocr_service):
        """Test service type extraction - both."""
        text = "Eau et Assainissement et Électricité"
        service_type = ocr_service._extract_service_type_from_text(text)
        assert "ماء" in service_type and "كهرباء" in service_type
    
    @patch('backend.services.ocr_service.OCRService._analyze_document')
    def test_extract_cil_success(self, mock_analyze, ocr_service):
        """Test CIL extraction - success case."""
        mock_analyze.return_value = "CIL: 1071324-101"
        
        result = ocr_service.extract_cil(b"fake_image_bytes")
        
        assert result.success is True
        assert result.data is not None
        assert result.data.cil == "1071324-101"
        assert result.error is None
    
    @patch('backend.services.ocr_service.OCRService._analyze_document')
    def test_extract_cil_no_text(self, mock_analyze, ocr_service):
        """Test CIL extraction - no text found."""
        mock_analyze.return_value = ""
        
        result = ocr_service.extract_cil(b"fake_image_bytes")
        
        assert result.success is False
        assert result.data is None
        assert "No text found" in result.error
    
    @patch('backend.services.ocr_service.OCRService._analyze_document')
    def test_extract_cil_not_found(self, mock_analyze, ocr_service):
        """Test CIL extraction - CIL not found in text."""
        mock_analyze.return_value = "This is some text without CIL"
        
        result = ocr_service.extract_cil(b"fake_image_bytes")
        
        assert result.success is False
        assert result.data is None
        assert "CIL number not found" in result.error
    
    @patch('backend.services.ocr_service.OCRService._analyze_document')
    def test_extract_bill_info_complete(self, mock_analyze, ocr_service):
        """Test full bill info extraction."""
        mock_analyze.return_value = """
        CIL: 1071324-101
        Nom: Abdenbi EL MARZOUKI
        Total Encaissé Dirhams: 351.48
        Date du paiement: 10-07-2013
        Eau et Assainissement
        """
        
        result = ocr_service.extract_bill_info(b"fake_image_bytes")
        
        assert result.success is True
        assert result.data is not None
        assert result.data.cil == "1071324-101"
        assert result.data.name == "Abdenbi EL MARZOUKI"
        assert result.data.amount_due == 351.48
        assert result.data.due_date == "10-07-2013"
        assert result.data.service_type == "ماء"


