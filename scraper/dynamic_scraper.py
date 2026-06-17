"""
Dynamic Web Scraper for TopCV/VietnamWorks (Member 3 - SP1)
Uses Selenium WebDriver concepts for dynamic content with JS rendering.
Includes realistic simulated data as fallback for demo purposes.
"""

import random
from datetime import datetime, timedelta
from scraper.base_scraper import BaseScraper

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False


class DynamicScraper(BaseScraper):
    """
    Dynamic scraper using Selenium WebDriver for JavaScript-rendered pages.
    Handles: pagination, scrolling, and dynamic content loading.
    Falls back to realistic simulated data if Selenium is unavailable.
    """

    def __init__(self, base_url="https://topcv.vn"):
        super().__init__(base_url)
        self.source_name = "TopCV"
        self.driver = None

    def _init_driver(self):
        """Initialize Selenium WebDriver with Chrome in headless mode."""
        if not HAS_SELENIUM:
            self.log("Selenium not installed, will use simulated data")
            return False

        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            self.driver = webdriver.Chrome(options=options)
            self.log("Selenium WebDriver initialized successfully")
            return True
        except Exception as e:
            self.log(f"Failed to initialize WebDriver: {e}")
            return False

    def fetch_page(self, url):
        """
        Fetch page using Selenium, handling dynamic content loading.
        Scrolls down to trigger lazy-loaded content.
        """
        if not self.driver:
            return None

        try:
            self.driver.get(url)
            # Wait for main content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Scroll down to load dynamic content
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                import time
                time.sleep(1)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            return self.driver.page_source
        except Exception as e:
            self.log(f"Selenium fetch failed: {e}")
            return None

    def extract_jobs(self, html_content):
        """Extract job listings from dynamically loaded HTML content."""
        jobs = []
        if not html_content:
            return jobs

        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # TopCV job card selectors
            job_cards = soup.find_all('div', class_='job-item')
            if not job_cards:
                job_cards = soup.find_all('div', class_='job-list-item')

            for card in job_cards:
                try:
                    title_el = card.find(['h3', 'a'], class_=lambda x: x and 'title' in str(x).lower())
                    title = title_el.get_text(strip=True) if title_el else "Unknown"

                    company_el = card.find(['a', 'span'], class_=lambda x: x and 'company' in str(x).lower())
                    company = company_el.get_text(strip=True) if company_el else "Unknown"

                    location_el = card.find(['span', 'div'], class_=lambda x: x and 'address' in str(x).lower())
                    location = location_el.get_text(strip=True) if location_el else "Ho Chi Minh"

                    salary_el = card.find(['span', 'div'], class_=lambda x: x and 'salary' in str(x).lower())
                    salary = salary_el.get_text(strip=True) if salary_el else "Negotiable"

                    jobs.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'skills': '',
                        'salary_raw': salary,
                        'experience': 'Not specified',
                        'source': self.source_name,
                        'date_scraped': datetime.now().strftime("%Y-%m-%d")
                    })
                except Exception:
                    continue
        except ImportError:
            self.log("BeautifulSoup not available for parsing")

        return jobs

    def run_scraper(self, max_pages=5):
        """
        Override to handle Selenium initialization and fallback.
        """
        self.log(f"Starting Dynamic Scraper (Selenium) for {self.source_name}")
        self.log(f"Target: {self.base_url}")

        # Try live scraping with Selenium
        if self._init_driver():
            try:
                live_jobs = super().run_scraper(max_pages)
                if live_jobs:
                    self.log(f"Live scraping successful: {len(live_jobs)} jobs")
                    return live_jobs
            finally:
                if self.driver:
                    self.driver.quit()
                    self.log("WebDriver closed")

        # Fallback to simulated data
        self.log("Live scraping unavailable. Generating simulated data for TopCV/VietnamWorks...")
        self.job_data = self._generate_simulated_data()
        self.log(f"Generated {len(self.job_data)} simulated job listings")
        return self.job_data

    def _generate_simulated_data(self):
        """Generate realistic IT job data simulating TopCV/VietnamWorks listings."""
        job_templates = [
            {"title": "Lập trình viên PHP", "company": "TMA Solutions", "skills": "PHP, Laravel, MySQL, JavaScript, Git", "exp": "1-2 năm"},
            {"title": "Kỹ sư AI/ML", "company": "FPT Software", "skills": "Python, TensorFlow, PyTorch, Docker, Linux", "exp": "2-4 năm"},
            {"title": "Lập trình viên .NET", "company": "CMC Global", "skills": ".NET, C#, SQL Server, Azure, Git", "exp": "1-3 năm"},
            {"title": "Android Developer", "company": "VNG Corporation", "skills": "Kotlin, Java, Android SDK, Git, Firebase", "exp": "1-3 năm"},
            {"title": "Kỹ sư hệ thống nhúng", "company": "Viettel Group", "skills": "C, C++, RTOS, ARM, Linux", "exp": "2-4 năm"},
            {"title": "Database Administrator", "company": "VNPT Technology", "skills": "MySQL, PostgreSQL, Redis, Linux, Python", "exp": "2-4 năm"},
            {"title": "Network Engineer", "company": "VNPT Technology", "skills": "Cisco, Linux, Python, Firewall, TCP/IP", "exp": "1-3 năm"},
            {"title": "Kỹ sư thiết kế ASIC", "company": "Renesas Vietnam", "skills": "Verilog, SystemVerilog, UVM, Python, TCL", "exp": "3-5 năm"},
            {"title": "Frontend Developer (Angular)", "company": "FPT Software", "skills": "Angular, TypeScript, JavaScript, SCSS, Git", "exp": "1-3 năm"},
            {"title": "Tester/QA Engineer", "company": "KMS Technology", "skills": "Selenium, Python, Java, Jira, Agile", "exp": "1-2 năm"},
            {"title": "Technical Project Manager", "company": "NashTech Vietnam", "skills": "Agile, Scrum, Jira, Python, SQL", "exp": "5-7 năm"},
            {"title": "Kỹ sư bảo mật", "company": "CMC Global", "skills": "Python, Linux, Network Security, AWS, Docker", "exp": "3-5 năm"},
            {"title": "SAP Consultant", "company": "FPT Software", "skills": "SAP, ABAP, SQL, Python, Excel", "exp": "2-4 năm"},
            {"title": "Unity Game Developer", "company": "VNG Corporation", "skills": "C#, Unity, Git, 3D Modeling, Agile", "exp": "1-3 năm"},
            {"title": "Business Analyst", "company": "TMA Solutions", "skills": "SQL, Python, Jira, UML, Agile", "exp": "1-3 năm"},
        ]

        locations = ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Bắc Ninh", "Hải Phòng"]
        salary_ranges = [
            ("8 - 15 triệu VND", 8000000, 15000000),
            ("12 - 20 triệu VND", 12000000, 20000000),
            ("15 - 25 triệu VND", 15000000, 25000000),
            ("20 - 35 triệu VND", 20000000, 35000000),
            ("25 - 40 triệu VND", 25000000, 40000000),
            ("30 - 50 triệu VND", 30000000, 50000000),
            ("Thương lượng", 0, 0),
            ("Cạnh tranh", 0, 0),
        ]

        simulated = []
        for template in job_templates:
            sal = random.choice(salary_ranges)
            loc = random.choice(locations)
            days_ago = random.randint(1, 30)
            date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

            simulated.append({
                'title': template['title'],
                'company': template['company'],
                'location': loc,
                'skills': template['skills'],
                'salary_raw': sal[0],
                'experience': template['exp'],
                'source': self.source_name,
                'date_scraped': date
            })

        return simulated
