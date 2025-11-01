"""
Email Agent Main Orchestrator
Coordinates all modules to process emails end-to-end
"""
import logging
import sys
from config import (
    IMAP_SERVER, IMAP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD,
    LLM_PROVIDER, OLLAMA_BASE_URL, OLLAMA_MODEL,
    GEMINI_API_KEY, GEMINI_MODEL,
    MAX_EMAILS_TO_PROCESS, SUMMARY_LIMIT,
    REPORT_FORMAT, REPORT_OUTPUT_DIR
)
from email_fetcher import EmailFetcher
from unsubscribe_extractor import UnsubscribeExtractor
from email_categorizer import EmailCategorizer
from email_summarizer import EmailSummarizer
from report_generator import ReportGenerator
from llm_client import LLMClientFactory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main orchestration function"""
    logger.info("=" * 60)
    logger.info("EMAIL AGENT - Starting Processing")
    logger.info("=" * 60)
    
    # Validate configuration
    if not EMAIL_USERNAME or not EMAIL_PASSWORD:
        logger.error("EMAIL_USERNAME and EMAIL_PASSWORD must be set in .env file")
        sys.exit(1)
    
    # Initialize LLM client
    llm_client = None
    if LLM_PROVIDER != "none":
        try:
            llm_kwargs = {}
            if LLM_PROVIDER == "ollama":
                llm_kwargs = {
                    "base_url": OLLAMA_BASE_URL,
                    "model": OLLAMA_MODEL
                }
            elif LLM_PROVIDER == "gemini":
                if not GEMINI_API_KEY:
                    logger.error("GEMINI_API_KEY required for Gemini provider")
                    sys.exit(1)
                llm_kwargs = {
                    "api_key": GEMINI_API_KEY,
                    "model": GEMINI_MODEL
                }
            
            llm_client = LLMClientFactory.create_client(LLM_PROVIDER, **llm_kwargs)
            logger.info(f"Initialized LLM client: {LLM_PROVIDER}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            logger.warning("Continuing without LLM (rules-based categorization only)")
    
    # Initialize modules
    logger.info("Initializing modules...")
    email_fetcher = EmailFetcher(IMAP_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD, IMAP_PORT)
    unsubscribe_extractor = UnsubscribeExtractor()
    email_categorizer = EmailCategorizer(llm_client=llm_client)
    email_summarizer = EmailSummarizer(llm_client=llm_client, summary_limit=SUMMARY_LIMIT)
    report_generator = ReportGenerator(output_dir=REPORT_OUTPUT_DIR, format=REPORT_FORMAT)
    
    # Connect to email server
    logger.info("Connecting to email server...")
    if not email_fetcher.connect():
        logger.error("Failed to connect to email server. Exiting.")
        sys.exit(1)
    
    if not email_fetcher.select_mailbox("inbox"):
        logger.error("Failed to select inbox. Exiting.")
        email_fetcher.disconnect()
        sys.exit(1)
    
    # Fetch emails
    logger.info(f"Fetching up to {MAX_EMAILS_TO_PROCESS} emails...")
    emails = email_fetcher.fetch_and_parse_emails(max_count=MAX_EMAILS_TO_PROCESS)
    
    if not emails:
        logger.warning("No emails found to process")
        email_fetcher.disconnect()
        return
    
    logger.info(f"Processing {len(emails)} emails...")
    
    # Process each email
    results = []
    for i, email_data in enumerate(emails, 1):
        logger.info(f"\n[{i}/{len(emails)}] Processing: {email_data.get('subject', 'No Subject')[:50]}")
        
        # Extract unsubscribe links
        body = email_data.get("body", "")
        unsubscribe_links = unsubscribe_extractor.extract_links(body)
        
        # Categorize email
        category = email_categorizer.categorize(
            subject=email_data.get("subject", ""),
            sender=email_data.get("sender", ""),
            body=body
        )
        
        # Summarize email (only if LLM is available, or for important categories)
        summary = ""
        if llm_client:
            summary = email_summarizer.summarize(
                subject=email_data.get("subject", ""),
                body=body
            )
        else:
            # Simple truncation if no LLM
            summary = f"{email_data.get('subject', '')}: {body[:100]}..." if len(body) > 100 else body
        
        # Store result
        results.append({
            "subject": email_data.get("subject", ""),
            "sender": email_data.get("sender", ""),
            "date": email_data.get("date", ""),
            "category": category,
            "summary": summary,
            "unsubscribe_links": unsubscribe_links
        })
        
        logger.info(f"  Category: {category}")
        logger.info(f"  Unsubscribe links: {len(unsubscribe_links)}")
    
    # Disconnect from email server
    email_fetcher.disconnect()
    
    # Generate report
    logger.info("\n" + "=" * 60)
    logger.info("Generating report...")
    logger.info("=" * 60)
    report_file = report_generator.generate(results)
    
    logger.info("\n" + "=" * 60)
    logger.info("EMAIL AGENT - Processing Complete!")
    logger.info("=" * 60)
    logger.info(f"Processed {len(results)} emails")
    logger.info(f"Report saved to: {report_file}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

