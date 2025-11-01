"""
Unsubscribe Link Extractor Module
Uses regex to extract unsubscribe links from email content
"""
import re
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnsubscribeExtractor:
    """Extracts unsubscribe links from email text"""
    
    def __init__(self):
        # Common unsubscribe patterns
        self.patterns = [
            # Standard unsubscribe URLs
            r'https?://[^\s<>"{}|\\^`\[\]]*(?:unsubscribe|optout|opt-out|remove|unsub)[^\s<>"{}|\\^`\[\]]*',
            # mailto unsubscribe
            r'mailto:[^\s<>"{}|\\^`\[\]]*[?&]subject=.*(?:unsubscribe|optout|opt-out|remove|unsub)',
            # Generic unsubscribe link tags
            r'<a[^>]*href=["\']([^"\']*(?:unsubscribe|optout|opt-out|remove|unsub)[^"\']*)["\']',
        ]
    
    def extract_links(self, text: str) -> List[str]:
        """Extract all unsubscribe links from text"""
        links = []
        
        if not text:
            return links
        
        # Try each pattern
        for pattern in self.patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            links.extend(matches)
        
        # Remove duplicates and clean up
        unique_links = []
        seen = set()
        
        for link in links:
            # Clean up the link
            link = link.strip().strip('"').strip("'").strip('>')
            
            # Skip if empty or already seen
            if not link or link in seen:
                continue
            
            # Normalize URL
            if link.startswith("mailto:"):
                unique_links.append(link)
                seen.add(link)
            elif link.startswith("http://") or link.startswith("https://"):
                unique_links.append(link)
                seen.add(link)
            elif link.startswith("//"):
                # Relative URL, make it https
                unique_links.append(f"https:{link}")
                seen.add(link)
        
        logger.info(f"Extracted {len(unique_links)} unsubscribe links")
        return unique_links
    
    def has_unsubscribe(self, text: str) -> bool:
        """Check if email contains unsubscribe link"""
        links = self.extract_links(text)
        return len(links) > 0

