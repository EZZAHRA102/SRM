"""OCR endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.models import OCRResult
from backend.api.deps import get_ocr_service
from backend.services import OCRService

router = APIRouter()


@router.post("/ocr/extract-cil", response_model=OCRResult)
async def extract_cil(
    file: UploadFile = File(...),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> OCRResult:
    """
    Extract CIL number from uploaded image.
    
    Args:
        file: Uploaded image file
        ocr_service: OCR service instance
        
    Returns:
        OCRResult with CIL extraction
        
    Raises:
        HTTPException: If extraction fails
    """
    try:
        image_bytes = await file.read()
        result = ocr_service.extract_cil(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"CIL extraction failed: {str(e)}"
        )


@router.post("/ocr/extract-bill", response_model=OCRResult)
async def extract_bill_info(
    file: UploadFile = File(...),
    ocr_service: OCRService = Depends(get_ocr_service)
) -> OCRResult:
    """
    Extract comprehensive bill information from uploaded image.
    
    Args:
        file: Uploaded image file
        ocr_service: OCR service instance
        
    Returns:
        OCRResult with complete bill information
        
    Raises:
        HTTPException: If extraction fails
    """
    try:
        image_bytes = await file.read()
        result = ocr_service.extract_bill_info(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Bill information extraction failed: {str(e)}"
        )


