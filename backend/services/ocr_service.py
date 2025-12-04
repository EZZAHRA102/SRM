"""OCR Service using Azure Document Intelligence with clear patterns and error handling."""
import re
import logging
import base64
from typing import Optional, Dict, Any
from backend.models import OCRResult, BillInfo

logger = logging.getLogger(__name__)


class OCRService:
    """
    OCR Service for extracting information from utility bill images.
    
    Features:
    - Clear, documented regex patterns
    - Fallback chain with logging
    - Proper error handling
    - CIL format normalization
    """
    
    # CIL Extraction Patterns (ordered by specificity)
    # Pattern 1: CIL with label prefix (most specific)
    # Example: "CIL: 1071324-101" or "رقم العميل: 1071324-101"
    CIL_PATTERN_WITH_LABEL = re.compile(
        r'(?:CIL|N°\s*Client|رقم\s*العميل|Client\s*ID|Identifiant)\s*:?\s*(\d{7}-\d{3})',
        re.IGNORECASE
    )
    
    # Pattern 2: Reversed CIL with label (3-7 format)
    # Example: "CIL: 101-1071324" → will be normalized to "1071324-101"
    CIL_PATTERN_REVERSED_WITH_LABEL = re.compile(
        r'(?:CIL|N°\s*Client|رقم\s*العميل|Client\s*ID|Identifiant)\s*:?\s*(\d{3}-\d{7})',
        re.IGNORECASE
    )
    
    # Pattern 3: Standalone CIL in correct format (7-3)
    # Example: "1071324-101"
    CIL_PATTERN_STANDALONE = re.compile(r'\b(\d{7}-\d{3})\b')
    
    # Pattern 4: Standalone reversed CIL (3-7)
    # Example: "101-1071324" → will be normalized
    CIL_PATTERN_REVERSED_STANDALONE = re.compile(r'\b(\d{3}-\d{7})\b')
    
    # Pattern 5: CIL without dash (7-10 digits)
    # Example: "1071324101" or "1071324"
    CIL_PATTERN_NO_DASH = re.compile(
        r'(?:CIL|N°\s*Client|رقم\s*العميل|Client\s*ID|Identifiant)\s*:?\s*(\d{7,10})',
        re.IGNORECASE
    )
    
    # Pattern 6: Fallback - any 8-10 digit number
    # Example: "1071324101"
    CIL_PATTERN_FALLBACK = re.compile(r'\b(\d{8,10})\b')
    
    # Name extraction patterns
    NAME_PATTERNS = [
        # Pattern: "Nom: Abdenbi EL MARZOUKI" or "الاسم: محمد الإدريسي"
        # Match until end of line or next label
        re.compile(
            r'(?:Nom|الاسم|Name)\s*:?\s*([A-Za-zÀ-ÿأ-ي\s]{3,50}?)(?:\n|$)',
            re.IGNORECASE | re.MULTILINE
        ),
        # Pattern: "Abdenbi EL MARZOUKI" (French name format) - standalone
        re.compile(r'^([A-Z][a-zà-ÿ]+\s+(?:EL\s+)?[A-Z][A-ZÀ-Ÿa-zà-ÿ]+)$', re.MULTILINE),
        # Pattern: "Client: Name"
        re.compile(
            r'(?:Client|العميل)\s*:?\s*([A-Za-zÀ-ÿأ-ي\s]{3,50}?)(?:\n|$)',
            re.IGNORECASE | re.MULTILINE
        )
    ]
    
    # Amount extraction patterns
    AMOUNT_PATTERNS = [
        # Pattern: "Total Encaissé Dirhams: 351.48" (Redal format)
        re.compile(
            r'(?:Total\s+Encaissé?\s+Dirhams?|مجموع\s+محصل\s+درهم)\s*:?\s*([\d,\.]+)',
            re.IGNORECASE
        ),
        # Pattern: "Montant Dirhams: 351.48"
        re.compile(
            r'(?:Montant\s+Dirhams?|مجموع\s+درهم)\s*:?\s*([\d,\.]+)',
            re.IGNORECASE
        ),
        # Pattern: "Montant à payer: 150.50 DH"
        re.compile(
            r'(?:Montant|المبلغ|Amount|Total)\s*(?:à\s*payer|المستحق|Due)?\s*:?\s*([\d,\.]+)\s*(?:DH|درهم|MAD)?',
            re.IGNORECASE
        ),
        # Pattern: Amount at end of line "150.50 DH"
        re.compile(r'([\d,\.]+)\s*(?:DH|درهم|MAD)\s*$', re.IGNORECASE | re.MULTILINE)
    ]
    
    # Date extraction patterns
    DATE_PATTERNS = [
        # Pattern: "Date du paiement: 10-07-2013"
        re.compile(
            r'(?:Date\s+du\s+paiement|تاريخ\s+الاتمام)\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            re.IGNORECASE
        ),
        # Pattern: "Date limite: 10-07-2013"
        re.compile(
            r'(?:Date\s*limite|تاريخ\s*الاستحقاق|Due\s*Date|Échéance)\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            re.IGNORECASE
        ),
        # Pattern: Standalone date
        re.compile(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})')
    ]
    
    # Service type patterns
    SERVICE_TYPE_KEYWORDS = {
        'water': [r'\b(?:Eau\s+et\s+Assainissement|Eau|ماء|الماء|Water)\b'],
        'electricity': [r'\b(?:Électricité|Electricité|كهرباء|Electricity)\b']
    }
    
    # Consumption patterns
    CONSUMPTION_PATTERNS = [
        re.compile(
            r'(?:Consommation|الاستهلاك|Consumption)\s*:?\s*([\d,\.]+)\s*(?:m³|kWh|كيلووات)?',
            re.IGNORECASE
        )
    ]
    
    def __init__(self, endpoint: str, key: str):
        """
        Initialize OCR service.
        
        Args:
            endpoint: Azure Document Intelligence endpoint
            key: Azure Document Intelligence API key
        """
        self.endpoint = endpoint
        self.key = key
        self._client = None
    
    def _get_client(self):
        """Get or create Azure Document Intelligence client."""
        if self._client is None:
            try:
                from azure.ai.documentintelligence import DocumentIntelligenceClient
                from azure.core.credentials import AzureKeyCredential
                
                self._client = DocumentIntelligenceClient(
                    endpoint=self.endpoint,
                    credential=AzureKeyCredential(self.key)
                )
            except ImportError:
                logger.error("azure-ai-documentintelligence package not installed")
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Document Intelligence client: {e}")
                raise
        
        return self._client
    
    def _analyze_document(self, image_bytes: bytes) -> str:
        """
        Analyze document and extract text.
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            Extracted text content
            
        Raises:
            Exception: If document analysis fails
        """
        try:
            client = self._get_client()
            
            # The SDK version 1.0.0b1 requires base64Source parameter
            # Convert bytes to base64 string
            base64_data = base64.b64encode(image_bytes).decode("utf-8")
            
            poller = client.begin_analyze_document(
                "prebuilt-read",
                analyze_request={"base64Source": base64_data}
            )
            
            result = poller.result()
            
            if not result.content:
                logger.warning("No text content found in document")
                return ""
            
            # Log raw OCR extracted text (first 500 chars for brevity)
            raw_text_preview = result.content[:500] + "..." if len(result.content) > 500 else result.content
            logger.debug(f"OCR Raw Text (preview): {raw_text_preview}")
            logger.info(f"OCR extracted {len(result.content)} characters of text")
            
            return result.content
            
        except Exception as e:
            logger.error(f"Document analysis failed: {e}")
            raise
    
    def _normalize_cil_format(self, cil: str) -> str:
        """
        Normalize CIL format to standard 7digits-3digits.
        
        Handles reversed formats: 101-1071324 → 1071324-101
        
        Args:
            cil: CIL string (may be in various formats)
            
        Returns:
            Normalized CIL string
        """
        if '-' not in cil:
            return cil
        
        parts = cil.split('-')
        if len(parts) != 2:
            return cil
        
        # If format is 3digits-7digits, reverse it to 7digits-3digits
        if len(parts[0]) == 3 and len(parts[1]) == 7:
            normalized = f"{parts[1]}-{parts[0]}"
            logger.info(f"Normalized reversed CIL: {cil} → {normalized}")
            return normalized
        
        # Already in correct format (7-3)
        return cil
    
    def _extract_cil_from_text(self, text: str) -> Optional[str]:
        """
        Extract CIL from text using pattern matching.
        
        Args:
            text: Text content to search
            
        Returns:
            Extracted CIL or None if not found
        """
        patterns = [
            (self.CIL_PATTERN_WITH_LABEL, False, "CIL_PATTERN_WITH_LABEL"),  # Correct format with label
            (self.CIL_PATTERN_REVERSED_WITH_LABEL, True, "CIL_PATTERN_REVERSED_WITH_LABEL"),  # Reversed with label
            (self.CIL_PATTERN_STANDALONE, False, "CIL_PATTERN_STANDALONE"),  # Standalone correct
            (self.CIL_PATTERN_REVERSED_STANDALONE, True, "CIL_PATTERN_REVERSED_STANDALONE"),  # Standalone reversed
            (self.CIL_PATTERN_NO_DASH, False, "CIL_PATTERN_NO_DASH"),  # No dash
            (self.CIL_PATTERN_FALLBACK, False, "CIL_PATTERN_FALLBACK")  # Fallback
        ]
        
        logger.debug(f"Attempting CIL extraction from text (length: {len(text)} chars)")
        
        for pattern, is_reversed, pattern_name in patterns:
            match = pattern.search(text)
            logger.debug(f"Trying pattern {pattern_name}: {'MATCH' if match else 'no match'}")
            if match:
                cil = match.group(1)
                logger.debug(f"Pattern {pattern_name} matched: {cil}")
                if is_reversed or '-' in cil:
                    original_cil = cil
                    cil = self._normalize_cil_format(cil)
                    if original_cil != cil:
                        logger.debug(f"Normalized CIL: {original_cil} → {cil}")
                logger.info(f"Extracted CIL using pattern {pattern_name}: {cil}")
                return cil
        
        logger.warning("No CIL pattern matched in text")
        logger.debug(f"Text content searched: {text[:200]}...")  # Log first 200 chars for debugging
        return None
    
    def _extract_name_from_text(self, text: str) -> Optional[str]:
        """
        Extract customer name from text.
        
        Args:
            text: Text content to search
            
        Returns:
            Extracted name or None if not found
        """
        logger.debug("Attempting name extraction from text")
        for idx, pattern in enumerate(self.NAME_PATTERNS):
            match = pattern.search(text)
            logger.debug(f"Trying name pattern {idx+1}: {'MATCH' if match else 'no match'}")
            if match:
                name = match.group(1).strip()
                # Clean up: remove any trailing text that might have been captured
                # Split by newline and take first part
                name = name.split('\n')[0].strip()
                # Validate: must be longer than 3 chars and not just digits
                if len(name) > 3 and not name.isdigit() and not any(char.isdigit() for char in name[:5]):
                    logger.info(f"Extracted name using pattern {idx+1}: {name}")
                    return name
                else:
                    logger.debug(f"Pattern {idx+1} matched but name '{name}' failed validation")
        
        logger.warning("No name pattern matched")
        return None
    
    def _extract_amount_from_text(self, text: str) -> Optional[float]:
        """
        Extract amount due from text.
        
        Args:
            text: Text content to search
            
        Returns:
            Extracted amount or None if not found
        """
        logger.debug("Attempting amount extraction from text")
        for idx, pattern in enumerate(self.AMOUNT_PATTERNS):
            match = pattern.search(text)
            logger.debug(f"Trying amount pattern {idx+1}: {'MATCH' if match else 'no match'}")
            if match:
                amount_str = match.group(1).replace(',', '.')
                try:
                    amount = float(amount_str)
                    if amount >= 0:  # Validate non-negative
                        logger.info(f"Extracted amount using pattern {idx+1}: {amount} DH")
                        return amount
                except ValueError:
                    logger.debug(f"Pattern {idx+1} matched '{amount_str}' but failed to parse as float")
                    continue
        
        logger.warning("No amount pattern matched")
        return None
    
    def _extract_date_from_text(self, text: str) -> Optional[str]:
        """
        Extract due date from text.
        
        Args:
            text: Text content to search
            
        Returns:
            Extracted date string or None if not found
        """
        logger.debug("Attempting date extraction from text")
        for idx, pattern in enumerate(self.DATE_PATTERNS):
            match = pattern.search(text)
            logger.debug(f"Trying date pattern {idx+1}: {'MATCH' if match else 'no match'}")
            if match:
                date_str = match.group(1)
                logger.info(f"Extracted date using pattern {idx+1}: {date_str}")
                return date_str
        
        logger.warning("No date pattern matched")
        return None
    
    def _extract_service_type_from_text(self, text: str) -> Optional[str]:
        """
        Extract service type from text.
        
        Args:
            text: Text content to search
            
        Returns:
            Service type string (e.g., "ماء", "كهرباء", "ماء وكهرباء")
        """
        service_types = []
        
        for service_name, patterns in self.SERVICE_TYPE_KEYWORDS.items():
            for pattern_str in patterns:
                if re.search(pattern_str, text, re.IGNORECASE):
                    if service_name == 'water':
                        service_types.append("ماء")
                    elif service_name == 'electricity':
                        service_types.append("كهرباء")
                    break
        
        if service_types:
            result = " و".join(service_types)
            logger.info(f"Extracted service type: {result}")
            return result
        
        return None
    
    def _extract_consumption_from_text(self, text: str) -> Optional[float]:
        """
        Extract consumption from text.
        
        Args:
            text: Text content to search
            
        Returns:
            Extracted consumption value or None if not found
        """
        for pattern in self.CONSUMPTION_PATTERNS:
            match = pattern.search(text)
            if match:
                consumption_str = match.group(1).replace(',', '.')
                try:
                    consumption = float(consumption_str)
                    if consumption >= 0:
                        logger.info(f"Extracted consumption: {consumption}")
                        return consumption
                except ValueError:
                    continue
        
        return None
    
    def extract_cil(self, image_bytes: bytes) -> OCRResult:
        """
        Extract only CIL from image.
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            OCRResult with CIL extraction
        """
        logger.info(f"Starting CIL extraction (image size: {len(image_bytes)} bytes)")
        try:
            text = self._analyze_document(image_bytes)
            
            if not text:
                logger.warning("CIL extraction: No text found in image")
                return OCRResult(
                    success=False,
                    data=None,
                    error="No text found in image"
                )
            
            cil = self._extract_cil_from_text(text)
            
            if not cil:
                logger.warning("CIL extraction: CIL number not found in extracted text")
                return OCRResult(
                    success=False,
                    data=None,
                    error="CIL number not found in image"
                )
            
            bill_info = BillInfo(cil=cil, raw_text=text)
            logger.info(f"CIL extraction SUCCESS: CIL={cil}")
            
            return OCRResult(
                success=True,
                data=bill_info,
                error=None
            )
            
        except Exception as e:
            logger.error(f"CIL extraction failed: {e}", exc_info=True)
            return OCRResult(
                success=False,
                data=None,
                error=f"Extraction failed: {str(e)}"
            )
    
    def extract_bill_info(self, image_bytes: bytes) -> OCRResult:
        """
        Extract comprehensive bill information from image.
        
        Args:
            image_bytes: Image file bytes
            
        Returns:
            OCRResult with complete bill information
        """
        logger.info(f"Starting bill info extraction (image size: {len(image_bytes)} bytes)")
        try:
            text = self._analyze_document(image_bytes)
            
            if not text:
                logger.warning("Bill extraction: No text found in image")
                return OCRResult(
                    success=False,
                    data=None,
                    error="No text found in image"
                )
            
            # Extract all fields
            logger.debug("Extracting individual fields from OCR text...")
            cil = self._extract_cil_from_text(text)
            name = self._extract_name_from_text(text)
            amount_due = self._extract_amount_from_text(text)
            due_date = self._extract_date_from_text(text)
            service_type = self._extract_service_type_from_text(text)
            consumption = self._extract_consumption_from_text(text)
            
            # Extract breakdown (water/electricity amounts)
            logger.debug("Extracting service breakdown...")
            breakdown = {}
            water_match = re.search(
                r'(?:Eau\s+et\s+Assainissement|الماء\s+والتطهير).*?([\d,\.]+)',
                text,
                re.IGNORECASE
            )
            elec_match = re.search(
                r'(?:Electricité|كهرباء).*?([\d,\.]+)',
                text,
                re.IGNORECASE
            )
            
            if water_match:
                try:
                    breakdown["water"] = float(water_match.group(1).replace(',', '.'))
                    logger.debug(f"Extracted water breakdown: {breakdown['water']}")
                except ValueError:
                    logger.debug("Water breakdown match found but failed to parse")
                    pass
            
            if elec_match:
                try:
                    breakdown["electricity"] = float(elec_match.group(1).replace(',', '.'))
                    logger.debug(f"Extracted electricity breakdown: {breakdown['electricity']}")
                except ValueError:
                    logger.debug("Electricity breakdown match found but failed to parse")
                    pass
            
            # Log extracted fields summary
            logger.info("Bill extraction results:")
            logger.info(f"  CIL: {cil}")
            logger.info(f"  Name: {name}")
            logger.info(f"  Amount Due: {amount_due} DH" if amount_due else "  Amount Due: Not found")
            logger.info(f"  Due Date: {due_date}" if due_date else "  Due Date: Not found")
            logger.info(f"  Service Type: {service_type}" if service_type else "  Service Type: Not found")
            logger.info(f"  Consumption: {consumption}" if consumption else "  Consumption: Not found")
            logger.info(f"  Breakdown: {breakdown}" if breakdown else "  Breakdown: None")
            
            bill_info = BillInfo(
                cil=cil,
                name=name,
                amount_due=amount_due,
                due_date=due_date,
                service_type=service_type,
                consumption=consumption,
                breakdown=breakdown if breakdown else None,
                raw_text=text
            )
            
            logger.info("Bill information extraction SUCCESS")
            
            return OCRResult(
                success=True,
                data=bill_info,
                error=None
            )
            
        except Exception as e:
            logger.error(f"Bill information extraction failed: {e}", exc_info=True)
            return OCRResult(
                success=False,
                data=None,
                error=f"Extraction failed: {str(e)}"
            )

