"""
Report Generator Module
Creates reports in various formats (JSON, CSV, TXT)
"""
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates reports from processed emails"""
    
    def __init__(self, output_dir: str = "reports", format: str = "json"):
        self.output_dir = Path(output_dir)
        self.format = format.lower()
        self.output_dir.mkdir(exist_ok=True)
    
    def generate(self, results: List[Dict]) -> str:
        """Generate report from results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Aggregate statistics
        stats = {
            "timestamp": datetime.now().isoformat(),
            "total_emails": len(results),
            "category_counts": {},
            "total_unsubscribe_links": 0,
            "emails_with_unsubscribe": 0
        }
        
        all_unsubscribe_links = []
        
        for result in results:
            # Count categories
            category = result.get("category", "Other")
            stats["category_counts"][category] = stats["category_counts"].get(category, 0) + 1
            
            # Count unsubscribe links
            unsubscribe_links = result.get("unsubscribe_links", [])
            if unsubscribe_links:
                stats["emails_with_unsubscribe"] += 1
                stats["total_unsubscribe_links"] += len(unsubscribe_links)
                all_unsubscribe_links.extend(unsubscribe_links)
        
        # Remove duplicate unsubscribe links
        unique_unsubscribe_links = list(dict.fromkeys(all_unsubscribe_links))
        stats["unique_unsubscribe_links"] = len(unique_unsubscribe_links)
        
        # Generate file based on format
        if self.format == "json":
            return self._generate_json(stats, results, unique_unsubscribe_links, timestamp)
        elif self.format == "csv":
            return self._generate_csv(stats, results, unique_unsubscribe_links, timestamp)
        else:  # txt
            return self._generate_txt(stats, results, unique_unsubscribe_links, timestamp)
    
    def _generate_json(self, stats: Dict, results: List[Dict], unsubscribe_links: List[str], timestamp: str) -> str:
        """Generate JSON report"""
        filename = self.output_dir / f"email_report_{timestamp}.json"
        
        report = {
            "statistics": stats,
            "unsubscribe_links": unsubscribe_links,
            "emails": results
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Generated JSON report: {filename}")
        return str(filename)
    
    def _generate_csv(self, stats: Dict, results: List[Dict], unsubscribe_links: List[str], timestamp: str) -> str:
        """Generate CSV report"""
        filename = self.output_dir / f"email_report_{timestamp}.csv"
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write statistics section
            writer.writerow(["STATISTICS"])
            writer.writerow(["Timestamp", stats["timestamp"]])
            writer.writerow(["Total Emails", stats["total_emails"]])
            writer.writerow(["Emails with Unsubscribe Links", stats["emails_with_unsubscribe"]])
            writer.writerow(["Total Unsubscribe Links", stats["total_unsubscribe_links"]])
            writer.writerow(["Unique Unsubscribe Links", stats["unique_unsubscribe_links"]])
            writer.writerow([])
            
            # Write category counts
            writer.writerow(["CATEGORY COUNTS"])
            for category, count in stats["category_counts"].items():
                writer.writerow([category, count])
            writer.writerow([])
            
            # Write unsubscribe links
            writer.writerow(["UNSUBSCRIBE LINKS"])
            for link in unsubscribe_links:
                writer.writerow([link])
            writer.writerow([])
            
            # Write email details
            writer.writerow(["EMAIL DETAILS"])
            writer.writerow(["Subject", "Sender", "Category", "Summary", "Unsubscribe Links"])
            for result in results:
                links_str = "; ".join(result.get("unsubscribe_links", []))
                writer.writerow([
                    result.get("subject", ""),
                    result.get("sender", ""),
                    result.get("category", ""),
                    result.get("summary", ""),
                    links_str
                ])
        
        logger.info(f"Generated CSV report: {filename}")
        return str(filename)
    
    def _generate_txt(self, stats: Dict, results: List[Dict], unsubscribe_links: List[str], timestamp: str) -> str:
        """Generate text report"""
        filename = self.output_dir / f"email_report_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write("EMAIL PROCESSING REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            # Statistics
            f.write("STATISTICS\n")
            f.write("-" * 60 + "\n")
            f.write(f"Timestamp: {stats['timestamp']}\n")
            f.write(f"Total Emails Processed: {stats['total_emails']}\n")
            f.write(f"Emails with Unsubscribe Links: {stats['emails_with_unsubscribe']}\n")
            f.write(f"Total Unsubscribe Links: {stats['total_unsubscribe_links']}\n")
            f.write(f"Unique Unsubscribe Links: {stats['unique_unsubscribe_links']}\n\n")
            
            # Category counts
            f.write("CATEGORY BREAKDOWN\n")
            f.write("-" * 60 + "\n")
            for category, count in sorted(stats["category_counts"].items(), key=lambda x: x[1], reverse=True):
                f.write(f"{category}: {count}\n")
            f.write("\n")
            
            # Unsubscribe links
            if unsubscribe_links:
                f.write("UNSUBSCRIBE LINKS\n")
                f.write("-" * 60 + "\n")
                for i, link in enumerate(unsubscribe_links, 1):
                    f.write(f"{i}. {link}\n")
                f.write("\n")
            
            # Email summaries
            f.write("EMAIL SUMMARIES\n")
            f.write("-" * 60 + "\n")
            for i, result in enumerate(results, 1):
                f.write(f"\n{i}. {result.get('subject', 'No Subject')}\n")
                f.write(f"   From: {result.get('sender', 'Unknown')}\n")
                f.write(f"   Category: {result.get('category', 'Other')}\n")
                f.write(f"   Summary: {result.get('summary', 'No summary available')}\n")
                if result.get('unsubscribe_links'):
                    f.write(f"   Unsubscribe: {', '.join(result['unsubscribe_links'])}\n")
        
        logger.info(f"Generated TXT report: {filename}")
        return str(filename)

