"""Tests for repository layer."""
import pytest
from backend.repositories import MockRepository, BaseRepository
from backend.models import User, Zone, PaymentStatus, ServiceStatus, MaintenanceStatus


class TestMockRepository:
    """Tests for MockRepository."""
    
    @pytest.fixture
    def repository(self):
        """Create a mock repository instance."""
        return MockRepository()
    
    def test_get_user_by_cil_found(self, repository):
        """Test retrieving an existing user by CIL."""
        user = repository.get_user_by_cil("1071324-101")
        
        assert user is not None
        assert isinstance(user, User)
        assert user.cil == "1071324-101"
        assert user.name == "Abdenbi EL MARZOUKI"
        assert user.payment_status == PaymentStatus.PAID
        assert user.service_status == ServiceStatus.ACTIVE
    
    def test_get_user_by_cil_not_found(self, repository):
        """Test retrieving a non-existent user."""
        user = repository.get_user_by_cil("9999999-999")
        
        assert user is None
    
    def test_get_user_by_cil_unpaid(self, repository):
        """Test retrieving an unpaid user."""
        user = repository.get_user_by_cil("5029012-505")
        
        assert user is not None
        assert user.payment_status == PaymentStatus.UNPAID
        assert user.outstanding_balance == 890.0
        assert user.service_status == ServiceStatus.DISCONNECTED
    
    def test_get_zone_by_id_found(self, repository):
        """Test retrieving an existing zone."""
        zone = repository.get_zone_by_id(1)
        
        assert zone is not None
        assert isinstance(zone, Zone)
        assert zone.zone_id == 1
        assert zone.maintenance_status == MaintenanceStatus.IN_PROGRESS
        assert zone.outage_reason is not None
    
    def test_get_zone_by_id_not_found(self, repository):
        """Test retrieving a non-existent zone."""
        zone = repository.get_zone_by_id(999)
        
        assert zone is None
    
    def test_get_zone_by_id_no_maintenance(self, repository):
        """Test retrieving a zone with no maintenance."""
        zone = repository.get_zone_by_id(2)
        
        assert zone is not None
        assert zone.maintenance_status == MaintenanceStatus.NONE
        assert zone.outage_reason is None
        assert zone.estimated_restoration is None
    
    def test_get_all_users(self, repository):
        """Test retrieving all users."""
        users = repository.get_all_users()
        
        assert len(users) == 5
        assert all(isinstance(user, User) for user in users)
        assert all(user.cil for user in users)
    
    def test_get_all_zones(self, repository):
        """Test retrieving all zones."""
        zones = repository.get_all_zones()
        
        assert len(zones) == 4
        assert all(isinstance(zone, Zone) for zone in zones)
        assert all(zone.zone_id for zone in zones)
    
    def test_repository_implements_base(self, repository):
        """Test that MockRepository implements BaseRepository."""
        assert isinstance(repository, BaseRepository)


