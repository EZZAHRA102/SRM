"""User domain models."""
from enum import Enum
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, field_validator


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PAID = "مدفوع"
    UNPAID = "غير مدفوع"


class ServiceStatus(str, Enum):
    """Service status enumeration."""
    ACTIVE = "نشط"
    DISCONNECTED = "مقطوع"


class ServiceType(str, Enum):
    """Service type enumeration."""
    WATER = "ماء"
    ELECTRICITY = "كهرباء"
    BOTH = "ماء وكهرباء"


class User(BaseModel):
    """User model representing a customer."""
    cil: str = Field(..., description="Customer Identification Number (format: 1071324-101)")
    name: str = Field(..., description="Customer name")
    address: str = Field(..., description="Customer address")
    phone: str = Field(..., description="Customer phone number")
    service_type: ServiceType = Field(..., description="Type of service")
    zone_id: int = Field(..., description="Zone ID where customer is located")
    payment_status: PaymentStatus = Field(..., description="Payment status")
    last_payment_date: date = Field(..., description="Last payment date")
    outstanding_balance: float = Field(..., ge=0, description="Outstanding balance in Dirhams")
    service_status: ServiceStatus = Field(..., description="Current service status")

    @field_validator("cil")
    @classmethod
    def validate_cil(cls, v: str) -> str:
        """Validate CIL format."""
        # CIL format: 7digits-3digits (e.g., 1071324-101)
        parts = v.split("-")
        if len(parts) != 2:
            raise ValueError("CIL must be in format: 7digits-3digits (e.g., 1071324-101)")
        if not (parts[0].isdigit() and parts[1].isdigit()):
            raise ValueError("CIL must contain only digits separated by dash")
        if len(parts[0]) != 7 or len(parts[1]) != 3:
            raise ValueError("CIL must be in format: 7digits-3digits (e.g., 1071324-101)")
        return v

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "cil": "1071324-101",
                "name": "Abdenbi EL MARZOUKI",
                "address": "967, Lot. Sala Al Jadida Zone (1), Sala Al Jadida",
                "phone": "0612345678",
                "service_type": "ماء وكهرباء",
                "zone_id": 1,
                "payment_status": "مدفوع",
                "last_payment_date": "2024-11-15",
                "outstanding_balance": 0.0,
                "service_status": "نشط"
            }
        }


