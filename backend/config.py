"""Configuration management using Pydantic BaseSettings."""
from typing import Optional
from pydantic import Field
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI Configuration
    azure_openai_api_key: Optional[str] = Field(None, env="AZURE_OPENAI_API_KEY")
    azure_openai_endpoint: Optional[str] = Field(None, env="AZURE_OPENAI_ENDPOINT")
    azure_openai_deployment_name: str = Field("gpt-4o", env="AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_api_version: str = Field("2024-08-01-preview", env="AZURE_OPENAI_API_VERSION")
    
    # Azure Document Intelligence Configuration
    azure_document_intelligence_endpoint: Optional[str] = Field(None, env="AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    azure_document_intelligence_key: Optional[str] = Field(None, env="AZURE_DOCUMENT_INTELLIGENCE_KEY")
    
    # Application Constants
    app_title: str = "نظام خدمة العملاء - SRM"
    app_icon: str = "💧"
    
    # API Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env (e.g., Azure Speech config for future use)

    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate that all required settings are present.
        
        Returns:
            tuple: (is_valid, list_of_missing_keys)
        """
        missing_keys = []
        
        if not self.azure_openai_api_key:
            missing_keys.append("AZURE_OPENAI_API_KEY")
        if not self.azure_openai_endpoint:
            missing_keys.append("AZURE_OPENAI_ENDPOINT")
        if not self.azure_document_intelligence_endpoint:
            missing_keys.append("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        if not self.azure_document_intelligence_key:
            missing_keys.append("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        
        is_valid = len(missing_keys) == 0
        return is_valid, missing_keys
    
    def get_error_message(self, missing_keys: list[str]) -> str:
        """
        Generate user-friendly error message for missing configuration.
        
        Args:
            missing_keys: List of missing environment variable names
            
        Returns:
            str: Formatted error message in Arabic and English
        """
        keys_str = ", ".join(missing_keys)
        return f"""
        ⚠️ خطأ في الإعدادات / Configuration Error
        
        المفاتيح التالية مفقودة في ملف .env:
        The following keys are missing in .env file:
        
        {keys_str}
        
        الرجاء نسخ ملف .env.example إلى .env وملء القيم المطلوبة.
        Please copy .env.example to .env and fill in the required values.
        """
    
    @property
    def AZURE_OPENAI_API_KEY(self) -> Optional[str]:
        """Backward compatibility property."""
        return self.azure_openai_api_key
    
    @property
    def AZURE_OPENAI_ENDPOINT(self) -> Optional[str]:
        """Backward compatibility property."""
        return self.azure_openai_endpoint
    
    @property
    def AZURE_OPENAI_DEPLOYMENT_NAME(self) -> str:
        """Backward compatibility property."""
        return self.azure_openai_deployment_name
    
    @property
    def AZURE_OPENAI_API_VERSION(self) -> str:
        """Backward compatibility property."""
        return self.azure_openai_api_version
    
    @property
    def AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT(self) -> Optional[str]:
        """Backward compatibility property."""
        return self.azure_document_intelligence_endpoint
    
    @property
    def AZURE_DOCUMENT_INTELLIGENCE_KEY(self) -> Optional[str]:
        """Backward compatibility property."""
        return self.azure_document_intelligence_key
    
    @property
    def APP_TITLE(self) -> str:
        """Backward compatibility property."""
        return self.app_title
    
    @property
    def APP_ICON(self) -> str:
        """Backward compatibility property."""
        return self.app_icon


# Create singleton instance
settings = Settings()

