"""
Email Categorizer Module
Hybrid approach: Rules first, then LLM fallback
"""
import re
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailCategorizer:
    """Categorizes emails using rules and optionally LLM"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.categories = ["Work", "Promotions", "Social", "News", "Other"]
        
        # Rule-based patterns
        self.work_patterns = {
            "subject": [r"invoice", r"meeting", r"client", r"project", r"deadline", r"task", r"urgent", r"code review"],
            "sender": [r"@.*\.(edu|gov|org|com)"],  # Professional domains
            "body": [r"invoice", r"invoice\s+number", r"payment", r"due date", r"project", r"meeting"]
        }
        
        self.promotion_patterns = {
            "subject": [r"sale", r"offer", r"discount", r"deal", r"limited time", r"save\s+\d+%", r"buy now", r"checkout"],
            "body": [r"shop now", r"buy now", r"limited offer", r"discount code", r"coupon", r"special price"]
        }
        
        self.social_patterns = {
            "subject": [r"friend request", r"mentioned you", r"commented", r"liked your", r"new follower"],
            "sender": [r"facebook", r"linkedin", r"twitter", r"instagram", r"tiktok", r"youtube"]
        }
        
        self.news_patterns = {
            "subject": [r"newsletter", r"daily digest", r"breaking", r"news", r"update"],
            "sender": [r"news", r"digest", r"newsletter"]
        }
    
    def _matches_patterns(self, text: str, patterns: list) -> bool:
        """Check if text matches any pattern"""
        if not text:
            return False
        text_lower = text.lower()
        for pattern in patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False
    
    def _contains_any_rule_words(self, subject: str, sender: str, body: str) -> bool:
        """Check if email contains ANY words from our predefined rule patterns
        
        This checks if the email contains any of the fixed vocabulary words we've 
        defined in our rules. If NOT, the email is out-of-vocabulary and needs LLM.
        """
        # Combine all patterns from all categories
        all_patterns = (
            self.work_patterns["subject"] + 
            self.work_patterns["sender"] + 
            self.work_patterns["body"] +
            self.promotion_patterns["subject"] + 
            self.promotion_patterns["body"] +
            self.social_patterns["subject"] + 
            self.social_patterns["sender"] +
            self.news_patterns["subject"] + 
            self.news_patterns["sender"]
        )
        
        # Combine all text fields for searching
        combined_text = f"{subject} {sender} {body}"
        
        # Check if ANY pattern matches the combined text
        for pattern in all_patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                # Found at least one rule-based word/pattern
                return True
        
        # No rule-based words found - this is out-of-vocabulary
        return False
    
    def categorize_with_rules(self, subject: str, sender: str, body: str) -> Optional[str]:
        """Categorize using deterministic rules - only if email contains rule-based keywords"""
        # Check Work
        if (self._matches_patterns(subject, self.work_patterns["subject"]) or
            self._matches_patterns(sender, self.work_patterns["sender"]) or
            self._matches_patterns(body, self.work_patterns["body"])):
            return "Work"
        
        # Check Promotions
        if (self._matches_patterns(subject, self.promotion_patterns["subject"]) or
            self._matches_patterns(body, self.promotion_patterns["body"])):
            return "Promotions"
        
        # Check Social
        if (self._matches_patterns(subject, self.social_patterns["subject"]) or
            self._matches_patterns(sender, self.social_patterns["sender"])):
            return "Social"
        
        # Check News
        if (self._matches_patterns(subject, self.news_patterns["subject"]) or
            self._matches_patterns(sender, self.news_patterns["sender"])):
            return "News"
        
        # No match found
        return None
    
    def categorize_with_llm(self, subject: str, sender: str, body: str) -> str:
        """Categorize using LLM when rules fail"""
        if not self.llm_client:
            logger.warning("No LLM client available, defaulting to 'Other'")
            return "Other"
        
        prompt = f"""Classify this email into one of these categories: Work, Promotions, Social, News, or Other.

Subject: {subject}
Sender: {sender}
Body (first 500 chars): {body[:500]}

Respond with ONLY the category name (one word):"""
        
        try:
            response = self.llm_client.generate(prompt)
            # Extract category from response
            response_clean = response.strip().lower()
            
            # Map response to valid category
            for cat in self.categories:
                if cat.lower() in response_clean:
                    logger.info(f"LLM categorized as: {cat}")
                    return cat
            
            return "Other"
        except Exception as e:
            logger.error(f"LLM categorization failed: {e}")
            return "Other"
    
    def categorize(self, subject: str, sender: str, body: str) -> str:
        """Hybrid categorization: Check if email contains predefined rule words
        
        Logic:
        1. If email contains ANY of our predefined rule-based words → use rules first
        2. If email contains NO predefined words (out-of-vocabulary) → use LLM immediately
        
        This ensures we use LLM for emails with words NOT in our fixed vocabulary,
        catching out-of-vocabulary patterns that rules can't handle.
        """
        # First check: Does the email contain ANY of our predefined rule-based words?
        contains_rule_words = self._contains_any_rule_words(subject, sender, body)
        
        if contains_rule_words:
            # Email contains our predefined words, try rule-based categorization
            category = self.categorize_with_rules(subject, sender, body)
            
            if category:
                logger.info(f"Rule-based categorization (words found in rules): {category}")
                return category
            else:
                # Words matched but didn't fit into a category - still use LLM for better classification
                logger.info("Rule words found but no category matched, using LLM for better classification")
                return self.categorize_with_llm(subject, sender, body)
        else:
            # Email contains words NOT in our predefined vocabulary
            # Use LLM to catch out-of-vocabulary patterns and classify intelligently
            logger.info("No rule-based words detected (out-of-vocabulary), using LLM for categorization")
            return self.categorize_with_llm(subject, sender, body)

