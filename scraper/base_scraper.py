from abc import ABC, abstractmethod
import pandas as pd
import os


class BaseScraper(ABC):
    def __init__(self, base_url):
        self.base_url = base_url
        self.job_data = []

    @abstractmethod
    def fetch_page(self, url):
        pass

    @abstractmethod
    def extract_jobs(self, html_content):
        pass

    def save_to_csv(self, filename):
        if not self.job_data:
            print("No data to save.")
            return

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        df = pd.DataFrame(self.job_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Successfully saved {len(self.job_data)} jobs to {filename}")