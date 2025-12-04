"""OCR endpoints."""
import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from backend.models import OCRResult
from backend.api.deps import get_ocr_service
from backend.services import OCRService

logger = logging.getLogger(__name__)
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
    logger.info("=" * 60)
    logger.info("OCR API Request: /ocr/extract-cil")
    logger.info(f"File: {file.filename}, Content-Type: {file.content_type}, Size: {file.size if hasattr(file, 'size') else 'unknown'}")
    
    try:
        image_bytes = await file.read()
        logger.info(f"File read successfully: {len(image_bytes)} bytes")
        
        result = ocr_service.extract_cil(image_bytes)
        
        logger.info(f"OCR Result: success={result.success}")
        if result.success and result.data:
            logger.info(f"Extracted CIL: {result.data.cil}")
        elif result.error:
            logger.warning(f"OCR Error: {result.error}")
        
        logger.info("=" * 60)
        return result
    except Exception as e:
        logger.error(f"CIL extraction failed: {e}", exc_info=True)
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
    logger.info("=" * 60)
    logger.info("OCR API Request: /ocr/extract-bill")
    logger.info(f"File: {file.filename}, Content-Type: {file.content_type}, Size: {file.size if hasattr(file, 'size') else 'unknown'}")
    
    try:
        image_bytes = await file.read()
        logger.info(f"File read successfully: {len(image_bytes)} bytes")
        
        result = ocr_service.extract_bill_info(image_bytes)
        
        logger.info(f"OCR Result: success={result.success}")
        if result.success and result.data:
            logger.info(f"Extracted Bill Info:")
            logger.info(f"  CIL: {result.data.cil}")
            logger.info(f"  Name: {result.data.name}")
            logger.info(f"  Amount Due: {result.data.amount_due}")
            logger.info(f"  Due Date: {result.data.due_date}")
            logger.info(f"  Service Type: {result.data.service_type}")
        elif result.error:
            logger.warning(f"OCR Error: {result.error}")
        
        logger.info("=" * 60)
        return result
    except Exception as e:
        logger.error(f"Bill information extraction failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Bill information extraction failed: {str(e)}"
        )


