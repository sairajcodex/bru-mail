"""
IMAP Email Fetcher Module
Handles connecting to email server and fetching emails
"""
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    logger.warning("BeautifulSoup4 not available. HTML parsing will be limited.")


class EmailFetcher:
    """Fetches emails from IMAP server"""
    
    def __init__(self, imap_server: str, username: str, password: str, port: int = 993):
        self.imap_server = imap_server
        self.username = username
        self.password = password
        self.port = port
        self.mail = None
    
    def connect(self) -> bool:
        """Connect to IMAP server"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.port)
            self.mail.login(self.username, self.password)
            logger.info(f"Successfully connected to {self.imap_server}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            return False
    
    def select_mailbox(self, mailbox: str = "inbox") -> bool:
        """Select mailbox (inbox, sent, etc.)"""
        try:
            status, _ = self.mail.select(mailbox)
            if status == "OK":
                logger.info(f"Selected mailbox: {mailbox}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to select mailbox: {e}")
            return False
    
    def _extract_text_from_html(self, html_content: str) -> str:
        """Extract readable text from HTML content"""
        if not BS4_AVAILABLE:
            # Fallback: basic HTML tag removal using regex
            import re
            # Remove script and style tags
            html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
            # Remove HTML tags but keep text
            text = re.sub(r'<[^>]+>', ' ', html_content)
            # Decode HTML entities
            text = text.replace('&nbsp;', ' ')
            text = text.replace('&amp;', '&')
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            text = text.replace('&quot;', '"')
            # Clean up whitespace
            text = ' '.join(text.split())
            return text.strip()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            # Get text
            text = soup.get_text()
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text.strip()
        except Exception as e:
            logger.warning(f"Failed to parse HTML: {e}")
            # Fallback to basic extraction
            return html_content.strip()

    def fetch_recent_emails(self, max_count: int = 50) -> List[bytes]:
        """Fetch recent email IDs"""
        try:
            # Search for all emails (you can customize this with date filters)
            status, messages = self.mail.search(None, "ALL")
            if status != "OK":
                logger.error("Failed to search emails")
                return []
            
            email_ids = messages[0].split()
            # Get the most recent N emails
            recent_ids = email_ids[-max_count:] if len(email_ids) > max_count else email_ids
            logger.info(f"Found {len(recent_ids)} emails to process")
            return recent_ids
        except Exception as e:
            logger.error(f"Failed to fetch email IDs: {e}")
            return []
    
    def get_email_content(self, email_id: bytes) -> Optional[Dict]:
        """Extract content from email"""
        try:
            # Fetch email by ID
            status, msg_data = self.mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                return None
            
            # Parse email message
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode subject
            subject_header = decode_header(msg["Subject"])
            subject = ""
            for part, encoding in subject_header:
                if isinstance(part, bytes):
                    subject += part.decode(encoding if encoding else "utf-8", errors="ignore")
                else:
                    subject += str(part)
            
            # Get sender
            from_header = decode_header(msg.get("From", ""))
            sender = ""
            for part, encoding in from_header:
                if isinstance(part, bytes):
                    sender += part.decode(encoding if encoding else "utf-8", errors="ignore")
                else:
                    sender += str(part)
            
            # Get date
            date = msg.get("Date", "")
            
            # Extract body text - prioritize plain text, fallback to HTML
            body = ""
            html_body = ""
            
            if msg.is_multipart():
                # Walk through all parts to find text/plain and text/html
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            decoded = payload.decode("utf-8", errors="ignore")
                            body += decoded
                    elif content_type == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            decoded = payload.decode("utf-8", errors="ignore")
                            html_body += decoded
            else:
                # Single part email
                content_type = msg.get_content_type()
                payload = msg.get_payload(decode=True)
                if payload:
                    decoded = payload.decode("utf-8", errors="ignore")
                    if content_type == "text/html":
                        html_body = decoded
                    else:
                        body = decoded
            
            # Use plain text if available, otherwise extract text from HTML
            if body.strip():
                # We have plain text, use it
                final_body = body.strip()
            elif html_body.strip():
                # No plain text, but we have HTML - extract text from it
                logger.debug(f"Email {email_id.decode()} has only HTML content, extracting text...")
                final_body = self._extract_text_from_html(html_body)
                if not final_body:
                    # If extraction failed, log and use a fallback message
                    logger.warning(f"Could not extract text from HTML for email {email_id.decode()}")
                    final_body = "[Email content could not be extracted - HTML only email with no readable text]"
            else:
                # No body content at all
                final_body = ""
            
            return {
                "id": email_id.decode(),
                "subject": subject.strip(),
                "sender": sender.strip(),
                "date": date,
                "body": final_body
            }
        except Exception as e:
            logger.error(f"Failed to parse email {email_id}: {e}")
            return None
    
    def fetch_and_parse_emails(self, max_count: int = 50) -> List[Dict]:
        """Fetch and parse multiple emails"""
        email_ids = self.fetch_recent_emails(max_count)
        emails = []
        
        for email_id in email_ids:
            email_data = self.get_email_content(email_id)
            if email_data:
                emails.append(email_data)
        
        return emails
    
    def disconnect(self):
        """Close connection"""
        if self.mail:
            try:
                self.mail.logout()
                logger.info("Disconnected from IMAP server")
            except Exception as e:
                logger.error(f"Error during logout: {e}")

