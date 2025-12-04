"""Maintenance service for zone maintenance and outage information."""
from typing import Optional
from backend.models import User, Zone, MaintenanceStatus
from backend.repositories.base import BaseRepository


class MaintenanceCheckResult:
    """Result of a maintenance check operation."""
    
    def __init__(
        self,
        user: Optional[User],
        zone: Optional[Zone],
        message: str,
        has_maintenance: bool
    ):
        """
        Initialize maintenance check result.
        
        Args:
            user: User object if found, None otherwise
            zone: Zone object if found, None otherwise
            message: Formatted message in Arabic
            has_maintenance: Whether maintenance is in progress
        """
        self.user = user
        self.zone = zone
        self.message = message
        self.has_maintenance = has_maintenance


class MaintenanceService:
    """Service for maintenance-related operations."""
    
    def __init__(self, repository: BaseRepository):
        """
        Initialize maintenance service.
        
        Args:
            repository: Repository for data access
        """
        self.repository = repository
    
    def check_maintenance(self, cil: str) -> MaintenanceCheckResult:
        """
        Check maintenance status for a customer's zone.
        
        Args:
            cil: Customer Identification Number
            
        Returns:
            MaintenanceCheckResult with maintenance information
        """
        user = self.repository.get_user_by_cil(cil)
        
        if not user:
            return MaintenanceCheckResult(
                user=None,
                zone=None,
                message=f"لم يتم العثور على عميل برقم CIL: {cil}",
                has_maintenance=False
            )
        
        zone_id = user.zone_id
        zone = self.repository.get_zone_by_id(zone_id)
        
        if not zone:
            return MaintenanceCheckResult(
                user=user,
                zone=None,
                message="لا توجد معلومات عن المنطقة.",
                has_maintenance=False
            )
        
        zone_name = zone.zone_name
        maintenance_status = zone.maintenance_status
        
        if maintenance_status == MaintenanceStatus.IN_PROGRESS:
            outage_reason = zone.outage_reason or "غير محدد"
            estimated_restoration = zone.estimated_restoration or "غير محدد"
            affected_services = zone.affected_services or "غير محدد"
            
            message = f"""
📍 منطقتك: {zone_name}
⚙️ حالة الصيانة: {maintenance_status.value}

سبب الانقطاع: {outage_reason}
الخدمات المتأثرة: {affected_services}
الوقت المتوقع للإصلاح: {estimated_restoration}

نعتذر عن الإزعاج. فرقنا تعمل على حل المشكلة في أقرب وقت ممكن.
"""
            return MaintenanceCheckResult(
                user=user,
                zone=zone,
                message=message.strip(),
                has_maintenance=True
            )
        else:
            message = f"""
📍 منطقتك: {zone_name}
✅ حالة الصيانة: {maintenance_status.value}

لا توجد أعمال صيانة مجدولة في منطقتك حالياً.
"""
            return MaintenanceCheckResult(
                user=user,
                zone=zone,
                message=message.strip(),
                has_maintenance=False
            )


