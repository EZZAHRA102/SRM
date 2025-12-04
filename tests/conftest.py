"""Pytest configuration and fixtures."""
import pytest
from datetime import date
from backend.models import User, Zone, PaymentStatus, ServiceStatus, ServiceType, MaintenanceStatus


@pytest.fixture
def sample_user_paid():
    """Sample user with paid status."""
    return User(
        cil="1071324-101",
        name="Abdenbi EL MARZOUKI",
        address="967, Lot. Sala Al Jadida Zone (1), Sala Al Jadida",
        phone="0612345678",
        service_type=ServiceType.BOTH,
        zone_id=1,
        payment_status=PaymentStatus.PAID,
        last_payment_date=date(2024, 11, 15),
        outstanding_balance=0.0,
        service_status=ServiceStatus.ACTIVE
    )


@pytest.fixture
def sample_user_unpaid():
    """Sample user with unpaid status."""
    return User(
        cil="5029012-505",
        name="يوسف السباعي",
        address="شارع الزرقطوني، طنجة",
        phone="0699887766",
        service_type=ServiceType.BOTH,
        zone_id=2,
        payment_status=PaymentStatus.UNPAID,
        last_payment_date=date(2024, 8, 15),
        outstanding_balance=890.0,
        service_status=ServiceStatus.DISCONNECTED
    )


@pytest.fixture
def sample_zone_maintenance():
    """Sample zone with maintenance in progress."""
    return Zone(
        zone_id=1,
        zone_name="الدار البيضاء - وسط المدينة",
        maintenance_status=MaintenanceStatus.IN_PROGRESS,
        outage_reason="إصلاح أنابيب المياه الرئيسية",
        estimated_restoration="2024-12-04 18:00",
        affected_services="ماء",
        status_updated="2024-12-03 08:00"
    )


@pytest.fixture
def sample_zone_no_maintenance():
    """Sample zone with no maintenance."""
    return Zone(
        zone_id=2,
        zone_name="الرباط - حي المحمدي",
        maintenance_status=MaintenanceStatus.NONE,
        outage_reason=None,
        estimated_restoration=None,
        affected_services=None,
        status_updated="2024-12-01 10:00"
    )


