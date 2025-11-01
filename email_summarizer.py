"""
Email Summarizer Module
Uses LLM to generate concise summaries
"""
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSummarizer:
    """Summarizes emails using LLM"""
    
    def __init__(self, llm_client, summary_limit: int = 1000):
        self.llm_client = llm_client
        self.summary_limit = summary_limit
    
    def summarize(self, subject: str, body: str) -> str:
        """Generate summary of email"""
        if not self.llm_client:
            logger.warning("No LLM client available, returning truncated body")
            return body[:200] + "..." if len(body) > 200 else body
        
        # Limit body length for token efficiency
        body_truncated = body[:self.summary_limit]
        
        prompt = f"""Summarize this email briefly in 1-2 sentences. Focus on the key information.

Subject: {subject}

Body:
{body_truncated}

Summary:"""
        
        try:
            summary = self.llm_client.generate(prompt, max_tokens=150)
            if summary:
                return summary.strip()
            else:
                # Fallback to simple truncation
                return f"{subject}: {body_truncated[:100]}..."
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            # Fallback
            return f"{subject}: {body[:100]}..." if len(body) > 100 else f"{subject}: {body}"

