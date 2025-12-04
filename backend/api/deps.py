"""FastAPI dependency injection."""
from functools import lru_cache
from backend.config import Settings, settings
from backend.repositories import MockRepository, BaseRepository
from backend.services import UserService, MaintenanceService, OCRService
from backend.ai.agent import SRMAgent


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).
    
    Returns:
        Settings instance
    """
    return settings


def get_repository() -> BaseRepository:
    """
    Get repository instance.
    
    Returns:
        BaseRepository instance
    """
    return MockRepository()


def get_user_service() -> UserService:
    """
    Get user service instance.
    
    Returns:
        UserService instance
    """
    repository = get_repository()
    return UserService(repository)


def get_maintenance_service() -> MaintenanceService:
    """
    Get maintenance service instance.
    
    Returns:
        MaintenanceService instance
    """
    repository = get_repository()
    return MaintenanceService(repository)


def get_ocr_service() -> OCRService:
    """
    Get OCR service instance.
    
    Returns:
        OCRService instance
    """
    app_settings = get_settings()
    
    if not app_settings.azure_document_intelligence_endpoint or not app_settings.azure_document_intelligence_key:
        raise ValueError("Azure Document Intelligence credentials not configured")
    
    return OCRService(
        endpoint=app_settings.azure_document_intelligence_endpoint,
        key=app_settings.azure_document_intelligence_key
    )


_agent_instance: SRMAgent | None = None


def get_agent() -> SRMAgent:
    """
    Get or create agent instance (singleton).
    
    Returns:
        SRMAgent instance
    """
    global _agent_instance
    
    if _agent_instance is None:
        app_settings = get_settings()
        user_service = get_user_service()
        maintenance_service = get_maintenance_service()
        
        _agent_instance = SRMAgent(
            settings=app_settings,
            user_service=user_service,
            maintenance_service=maintenance_service
        )
        
        if not _agent_instance.initialize():
            raise RuntimeError("Failed to initialize SRM agent")
    
    return _agent_instance


