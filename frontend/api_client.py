"""API client for communicating with backend."""
import httpx
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SRMAPIClient:
    """HTTP client for SRM backend API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of the backend API
        """
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(timeout=30.0)
    
    def health_check(self) -> bool:
        """
        Check if backend is healthy.
        
        Returns:
            True if backend is healthy, False otherwise
        """
        try:
            response = self.client.get(f"{self.base_url}/api/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def chat(self, message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Send chat message to backend.
        
        Args:
            message: User message
            history: Chat history
            
        Returns:
            Response dictionary with 'response' and optional 'tool_calls'
            
        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            response = self.client.post(
                f"{self.base_url}/api/chat",
                json={
                    "message": message,
                    "history": history
                }
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Chat request failed: {e}")
            raise
    
    def extract_cil(self, image_bytes: bytes, filename: str = "image.jpg") -> Dict[str, Any]:
        """
        Extract CIL from image.
        
        Args:
            image_bytes: Image file bytes
            filename: Filename for upload
            
        Returns:
            OCRResult dictionary
            
        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            files = {"file": (filename, image_bytes, "image/jpeg")}
            response = self.client.post(
                f"{self.base_url}/api/ocr/extract-cil",
                files=files
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"CIL extraction failed: {e}")
            raise
    
    def extract_bill_info(self, image_bytes: bytes, filename: str = "image.jpg") -> Dict[str, Any]:
        """
        Extract complete bill information from image.
        
        Args:
            image_bytes: Image file bytes
            filename: Filename for upload
            
        Returns:
            OCRResult dictionary with complete bill info
            
        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            files = {"file": (filename, image_bytes, "image/jpeg")}
            response = self.client.post(
                f"{self.base_url}/api/ocr/extract-bill",
                files=files
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Bill info extraction failed: {e}")
            raise
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


