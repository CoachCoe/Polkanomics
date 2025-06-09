from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Model Configuration
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TEMPERATURE: float = TEMPERATURE
    
    # System Prompts
    ECONOMICS_PROMPT: str = """You are an expert in economics, game theory, and tokenomics, with special expertise in the Polkadot ecosystem. 
    You provide detailed, accurate, and well-reasoned responses about:
    - Economic theories and principles
    - Game theory concepts and applications
    - Tokenomics design and analysis
    - Polkadot ecosystem specifics, including:
        * DOT token economics
        * Parachain economics
        * Staking mechanisms
        * Governance tokenomics
        * Cross-chain economics
    
    Always provide context and explain complex concepts clearly. When discussing tokenomics, include both theoretical frameworks and practical applications."""
    
    # Knowledge Base Configuration
    KNOWLEDGE_BASE_DIR: str = "knowledge_base"
    
    # API Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Ollama-specific settings
    OLLAMA_MODEL_NAME: str = os.getenv("OLLAMA_MODEL_NAME", "llama3")
    
    class Config:
        env_file = ".env"

settings = Settings() 