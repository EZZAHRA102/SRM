"""Zone domain models."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class MaintenanceStatus(str, Enum):
    """Maintenance status enumeration."""
    IN_PROGRESS = "جاري الصيانة"
    NONE = "لا توجد صيانة"


class Zone(BaseModel):
    """Zone model representing a service zone."""
    zone_id: int = Field(..., description="Zone ID")
    zone_name: str = Field(..., description="Zone name")
    maintenance_status: MaintenanceStatus = Field(..., description="Current maintenance status")
    outage_reason: Optional[str] = Field(None, description="Reason for outage if maintenance in progress")
    estimated_restoration: Optional[str] = Field(None, description="Estimated restoration time")
    affected_services: Optional[str] = Field(None, description="Affected services (ماء, كهرباء, etc.)")
    status_updated: str = Field(..., description="Last status update timestamp")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "zone_id": 1,
                "zone_name": "الدار البيضاء - وسط المدينة",
                "maintenance_status": "جاري الصيانة",
                "outage_reason": "إصلاح أنابيب المياه الرئيسية",
                "estimated_restoration": "2024-12-04 18:00",
                "affected_services": "ماء",
                "status_updated": "2024-12-03 08:00"
            }
        }


