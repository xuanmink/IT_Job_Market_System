from abc import ABC, abstractmethod
import pandas as pd
import os
import json
from datetime import datetime


class BaseScraper(ABC):
    """
    Abstract base class for all web scrapers.
    Implements the Template Method pattern for scraping workflow.
    Subclasses must implement fetch_page() and extract_jobs().
    """

    def __init__(self, base_url):
        self.base_url = base_url
        self.job_data = []
        self.scrape_log = []

    @abstractmethod
    def fetch_page(self, url):
        """Fetch the HTML content of a page."""
        pass

    @abstractmethod
    def extract_jobs(self, html_content):
        """Extract job listings from HTML content."""
        pass

    def run_scraper(self, max_pages=5):
        """
        Template method: orchestrates the full scraping workflow.
        1. Fetch pages
        2. Extract jobs
        3. Save results
        """
        self.log(f"Starting scraper for {self.base_url}")
        self.log(f"Max pages to scrape: {max_pages}")

        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/page/{page}"
            self.log(f"Fetching page {page}: {url}")

            try:
                html = self.fetch_page(url)
                if html:
                    jobs = self.extract_jobs(html)
                    self.job_data.extend(jobs)
                    self.log(f"Extracted {len(jobs)} jobs from page {page}")
                else:
                    self.log(f"No content from page {page}, stopping.")
                    break
            except Exception as e:
                self.log(f"Error on page {page}: {str(e)}")
                break

        self.log(f"Total jobs scraped: {len(self.job_data)}")
        return self.job_data

    def save_to_csv(self, filename):
        """Save scraped data to CSV file."""
        if not self.job_data:
            self.log("No data to save.")
            return

        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        df = pd.DataFrame(self.job_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        self.log(f"✅ Successfully saved {len(self.job_data)} jobs to {filename}")

    def save_to_json(self, filename):
        """Save scraped data to JSON file."""
        if not self.job_data:
            self.log("No data to save.")
            return

        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.job_data, f, ensure_ascii=False, indent=2)
        self.log(f"✅ Successfully saved {len(self.job_data)} jobs to {filename}")

    def log(self, message):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.scrape_log.append(entry)
        print(entry)

    def get_log(self):
        """Return the scrape log."""
        return self.scrape_log

    def get_stats(self):
        """Return scraping statistics."""
        return {
            "source": self.base_url,
            "total_jobs": len(self.job_data),
            "log_entries": len(self.scrape_log),
            "last_run": datetime.now().isoformat()
        }