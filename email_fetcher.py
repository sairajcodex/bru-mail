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
            
            # Extract body text
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode("utf-8", errors="ignore")
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="ignore")
            
            return {
                "id": email_id.decode(),
                "subject": subject.strip(),
                "sender": sender.strip(),
                "date": date,
                "body": body.strip()
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

