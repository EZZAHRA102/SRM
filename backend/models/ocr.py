"""OCR domain models."""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CILExtraction(BaseModel):
    """CIL extraction result."""
    cil: str = Field(..., description="Extracted CIL number")


class BillInfo(BaseModel):
    """Complete bill information extracted from image."""
    cil: Optional[str] = Field(None, description="Customer Identification Number")
    name: Optional[str] = Field(None, description="Customer name")
    amount_due: Optional[float] = Field(None, ge=0, description="Amount due in Dirhams")
    due_date: Optional[str] = Field(None, description="Payment due date")
    bill_date: Optional[str] = Field(None, description="Bill issue date")
    service_type: Optional[str] = Field(None, description="Service type (ماء, كهرباء, etc.)")
    previous_balance: Optional[float] = Field(None, ge=0, description="Previous unpaid balance")
    consumption: Optional[float] = Field(None, ge=0, description="Current consumption")
    breakdown: Optional[Dict[str, float]] = Field(None, description="Breakdown by service type")
    raw_text: Optional[str] = Field(None, description="Raw extracted text")


class OCRResult(BaseModel):
    """OCR operation result."""
    success: bool = Field(..., description="Whether extraction was successful")
    data: Optional[BillInfo] = Field(None, description="Extracted data if successful")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "cil": "1071324-101",
                    "name": "Abdenbi EL MARZOUKI",
                    "amount_due": 150.50
                },
                "error": None
            }
        }


