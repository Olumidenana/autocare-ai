"""
Application Configuration and Environment Variables for AutoCare AI.
"""

from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    # App General
    APP_NAME: str = "AutoCare AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Meta WhatsApp Cloud API credentials
    WHATSAPP_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_BUSINESS_ACCOUNT_ID: Optional[str] = None
    WHATSAPP_VERIFY_TOKEN: str = "autocare_secret_token_123"
    
    # AI Providers
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    
    # Simulation / Offline Testing Mode
    # If True or if no API keys are present, uses the built-in Master Mechanic Rule Engine
    SIMULATION_MODE: bool = False
    
    model_config = {
        "env_file": str(ENV_PATH),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }

settings = Settings()
