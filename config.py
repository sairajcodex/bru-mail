"""
Configuration file for Email Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# IMAP Configuration
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # Use app password for Gmail

# LLM Provider Configuration
# Options: "ollama", "gemini", "none"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# Ollama Configuration (for local LLMs)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  # Options: llama3.2, mistral, qwen2.5, etc.

# Gemini API Configuration (free tier alternative)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")  # Free tier supports flash model

# Email Processing Configuration
MAX_EMAILS_TO_PROCESS = int(os.getenv("MAX_EMAILS_TO_PROCESS", "50"))
SUMMARY_LIMIT = int(os.getenv("SUMMARY_LIMIT", "1000"))  # Max chars in body for summarization

# Report Configuration
REPORT_FORMAT = os.getenv("REPORT_FORMAT", "json")  # Options: json, csv, txt
REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "reports")

