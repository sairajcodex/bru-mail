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
        
        # Check if body has meaningful content
        body_stripped = body.strip()
        if not body_stripped or len(body_stripped) < 5:
            logger.warning(f"Email body is empty or too short, using subject only")
            return f"Email with subject: {subject} (no body content available)"
        
        # Limit body length for token efficiency
        body_truncated = body_stripped[:self.summary_limit]
        
        prompt = f"""Summarize this email briefly in 1-2 sentences. Focus on the key information.

Subject: {subject}

Body:
{body_truncated}

Summary:"""
        
        try:
            summary = self.llm_client.generate(prompt, max_tokens=150)
            if summary:
                summary_stripped = summary.strip()
                # Check if LLM gave a meaningful response or just asked for more content
                if any(phrase.lower() in summary_stripped.lower() for phrase in [
                    "please provide", "need more", "cannot summarize", "no content",
                    "text is missing", "unable to", "not enough information"
                ]):
                    logger.warning("LLM returned error message instead of summary, using fallback")
                    # Return a summary based on subject and truncated body
                    return f"Email about: {subject}. {body_truncated[:150]}..." if len(body_truncated) > 150 else f"Email about: {subject}. {body_truncated}"
                return summary_stripped
            else:
                # Fallback to simple truncation
                return f"{subject}: {body_truncated[:100]}..."
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            # Fallback
            return f"{subject}: {body_stripped[:100]}..." if len(body_stripped) > 100 else f"{subject}: {body_stripped}"

