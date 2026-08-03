"""
Static Web Scraper for ITviec (Member 2 - SP1)
Uses BeautifulSoup + requests to scrape static HTML pages.
Includes realistic simulated data as fallback for demo purposes.
"""

import random
from datetime import datetime, timedelta
from scraper.base_scraper import BaseScraper

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


class ITViecScraper(BaseScraper):
    """
    Static scraper for ITviec.com using BeautifulSoup.
    Extracts: job title, company, location, skills, salary, experience level.
    Falls back to realistic simulated data if live scraping fails.
    """

    def __init__(self, base_url="https://itviec.com"):
        super().__init__(base_url)
        self.source_name = "ITviec"

    def fetch_page(self, url):
        """
        Fetch HTML from a static page using requests.
        Returns HTML string or None if request fails.
        """
        if not HAS_DEPS:
            self.log("requests/bs4 not available, using simulated data")
            return None

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                self.log(f"HTTP {response.status_code} for {url}")
                return None
        except Exception as e:
            self.log(f"Request failed: {str(e)}")
            return None

    def extract_jobs(self, html_content):
        """
        Parse HTML with BeautifulSoup to extract job listings.
        Looks for common ITviec HTML structure patterns.
        """
        jobs = []
        if not html_content or not HAS_DEPS:
            return jobs

        soup = BeautifulSoup(html_content, 'html.parser')

        # ITviec uses various class names for job cards
        job_cards = soup.find_all('div', class_='job_content')
        if not job_cards:
            job_cards = soup.find_all('div', class_='job-item')
        if not job_cards:
            job_cards = soup.find_all('article')

        for card in job_cards:
            try:
                title_el = card.find(['h2', 'h3', 'a'], class_=lambda x: x and 'title' in str(x).lower())
                title = title_el.get_text(strip=True) if title_el else "Unknown Title"

                company_el = card.find(['span', 'a', 'div'], class_=lambda x: x and 'company' in str(x).lower())
                company = company_el.get_text(strip=True) if company_el else "Unknown Company"

                location_el = card.find(['span', 'div'], class_=lambda x: x and 'city' in str(x).lower())
                location = location_el.get_text(strip=True) if location_el else "Ho Chi Minh"

                skill_els = card.find_all(['span', 'a'], class_=lambda x: x and 'tag' in str(x).lower())
                skills = ", ".join([s.get_text(strip=True) for s in skill_els]) if skill_els else ""

                salary_el = card.find(['span', 'div'], class_=lambda x: x and 'salary' in str(x).lower())
                salary = salary_el.get_text(strip=True) if salary_el else "Negotiable"

                jobs.append({
                    'title': title,
                    'company': company,
                    'location': location,
                    'skills': skills,
                    'salary_raw': salary,
                    'experience': 'Not specified',
                    'source': self.source_name,
                    'date_scraped': datetime.now().strftime("%Y-%m-%d")
                })
            except Exception as e:
                self.log(f"Error parsing job card: {e}")
                continue

        return jobs

    def run_scraper(self, max_pages=5):
        """
        Override run_scraper to use simulated data as fallback.
        This ensures the demo always has data to show.
        """
        self.log(f"Starting ITviec Static Scraper (BeautifulSoup)")
        self.log(f"Target: {self.base_url}")

        # Try live scraping first
        live_jobs = super().run_scraper(max_pages)

        # If live scraping got data, use it
        if live_jobs:
            self.log(f"Live scraping successful: {len(live_jobs)} jobs")
            return live_jobs

        # Fallback: generate realistic simulated data
        self.log("Live scraping unavailable. Generating realistic simulated data...")
        self.job_data = self._generate_simulated_data()
        self.log(f"Generated {len(self.job_data)} simulated job listings from ITviec")
        return self.job_data

    def _generate_simulated_data(self):
        """Generate realistic IT job data simulating ITviec listings."""
        job_templates = [
            {"title": "Senior Python Developer", "company": "FPT Software", "skills": "Python, Django, PostgreSQL, Docker, AWS", "exp": "3-5 years"},
            {"title": "React Frontend Developer", "company": "VNG Corporation", "skills": "JavaScript, React, TypeScript, Redux, Git", "exp": "2-4 years"},
            {"title": "IC Design Engineer", "company": "Intel Vietnam", "skills": "Verilog, SystemVerilog, Python, C++", "exp": "2-5 years"},
            {"title": "DevOps Engineer", "company": "Grab Vietnam", "skills": "Docker, Kubernetes, AWS, Jenkins, Terraform", "exp": "3-5 years"},
            {"title": "Java Backend Developer", "company": "KMS Technology", "skills": "Java, Spring Boot, MySQL, Docker, Microservices", "exp": "2-4 years"},
            {"title": "Data Scientist", "company": "Shopee Vietnam", "skills": "Python, TensorFlow, Pandas, SQL, Machine Learning", "exp": "2-4 years"},
            {"title": "Embedded Software Engineer", "company": "Bosch Vietnam", "skills": "C, C++, RTOS, ARM, Linux", "exp": "1-3 years"},
            {"title": "Full-stack Developer", "company": "NashTech Vietnam", "skills": "JavaScript, Node.js, React, MongoDB, Docker", "exp": "2-4 years"},
            {"title": "Cloud Solutions Architect", "company": "CMC Global", "skills": "AWS, Azure, Terraform, Kubernetes, Python", "exp": "5-7 years"},
            {"title": "FPGA Design Engineer", "company": "Viettel Group", "skills": "Verilog, FPGA, VHDL, C++, Linux", "exp": "2-4 years"},
            {"title": "Mobile Developer (iOS)", "company": "TMA Solutions", "skills": "Swift, iOS, Git, REST API, Firebase", "exp": "1-3 years"},
            {"title": "Machine Learning Engineer", "company": "VNG Corporation", "skills": "Python, PyTorch, NLP, Docker, AWS", "exp": "3-5 years"},
            {"title": "QA Automation Engineer", "company": "FPT Software", "skills": "Python, Selenium, Java, Git, Agile", "exp": "1-3 years"},
            {"title": "Blockchain Developer", "company": "KMS Technology", "skills": "Solidity, JavaScript, Go, Docker, Web3", "exp": "2-4 years"},
            {"title": "Site Reliability Engineer", "company": "Grab Vietnam", "skills": "Go, Kubernetes, Docker, AWS, Prometheus", "exp": "3-5 years"},
        ]

        locations = ["Ho Chi Minh", "Ha Noi", "Da Nang", "Bac Ninh"]
        salary_ranges = [
            ("8,000,000 - 15,000,000 VND", 8000000, 15000000),
            ("15,000,000 - 25,000,000 VND", 15000000, 25000000),
            ("20,000,000 - 35,000,000 VND", 20000000, 35000000),
            ("25,000,000 - 45,000,000 VND", 25000000, 45000000),
            ("30,000,000 - 50,000,000 VND", 30000000, 50000000),
            ("35,000,000 - 65,000,000 VND", 35000000, 65000000),
            ("1,500 - 3,000 USD", 37500000, 75000000),
            ("Competitive", 0, 0),
            ("Negotiable", 0, 0),
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
