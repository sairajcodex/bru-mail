"""
LLM Client Module
Supports multiple LLM providers: Ollama (local) and Gemini (cloud/free tier)
"""
import requests
import json
from typing import Optional
import logging

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for Ollama (local LLM)"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._check_connection()
    
    def _check_connection(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info(f"Connected to Ollama at {self.base_url}")
                # Check if model is available
                models = [m.get("name", "") for m in response.json().get("models", [])]
                if not any(self.model in m for m in models):
                    logger.warning(f"Model {self.model} may not be available. Available models: {models}")
            else:
                logger.error(f"Ollama connection failed: {response.status_code}")
        except Exception as e:
            logger.error(f"Cannot connect to Ollama: {e}")
            logger.info("Make sure Ollama is installed and running: https://ollama.ai")
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response from Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return ""
        except Exception as e:
            logger.error(f"Failed to generate with Ollama: {e}")
            return ""


class GeminiClient:
    """Client for Google Gemini API (free tier)"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        self.api_key = api_key
        self.model_name = model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        logger.info(f"Initialized Gemini client with model: {model}")
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response from Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7
                )
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Failed to generate with Gemini: {e}")
            return ""


class LLMClientFactory:
    """Factory to create appropriate LLM client"""
    
    @staticmethod
    def create_client(provider: str, **kwargs):
        """Create LLM client based on provider"""
        if provider == "ollama":
            return OllamaClient(
                base_url=kwargs.get("base_url", "http://localhost:11434"),
                model=kwargs.get("model", "llama3.2")
            )
        elif provider == "gemini":
            api_key = kwargs.get("api_key")
            if not api_key:
                raise ValueError("GEMINI_API_KEY is required for Gemini provider")
            return GeminiClient(
                api_key=api_key,
                model=kwargs.get("model", "gemini-1.5-flash")
            )
        elif provider == "none":
            logger.info("No LLM provider selected, categorization will use rules only")
            return None
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

