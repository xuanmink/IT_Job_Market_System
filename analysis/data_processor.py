"""
Data Processing Engine (Member 4 - SP2)
Handles: CSV/JSON loading, Regex-based salary normalization,
skill string parsing, and data cleaning using Pandas.
"""

import re
import pandas as pd
import os


class DataProcessor:
    """
    Data Processing Engine using Pandas and Regular Expressions.
    Cleans, normalizes, and structures raw scraped data for database insertion.
    """

    def __init__(self):
        self.raw_data = None
        self.cleaned_data = None
        self.processing_log = []

    def load_csv(self, filepath):
        """Load raw CSV data into a Pandas DataFrame."""
        if not os.path.exists(filepath):
            self._log(f"File not found: {filepath}")
            return None

        self.raw_data = pd.read_csv(filepath, encoding='utf-8-sig')
        self._log(f"Loaded {len(self.raw_data)} rows from {filepath}")
        return self.raw_data

    def load_from_list(self, job_list):
        """Load data from a list of dictionaries (from scraper output)."""
        self.raw_data = pd.DataFrame(job_list)
        self._log(f"Loaded {len(self.raw_data)} rows from scraper output")
        return self.raw_data

    # ── Regex Engine for Salary Normalization ──────────────────────

    def normalize_salary(self, salary_string):
        """
        Regex-based salary normalization.
        Handles formats:
        - "25,000,000 - 45,000,000 VND" → (25000000, 45000000, "VND")
        - "1,500 - 3,000 USD" → (37500000, 75000000, "VND") [converted]
        - "25 - 45 triệu VND" → (25000000, 45000000, "VND")
        - "8 - 15 triệu" → (8000000, 15000000, "VND")
        - "Negotiable" / "Competitive" → (0, 0, "VND")
        """
        if not salary_string or not isinstance(salary_string, str):
            return 0, 0, "VND"

        salary_string = salary_string.strip()

        # Pattern 1: "25,000,000 - 45,000,000 VND"
        pattern_full = r'([\d,]+)\s*[-–]\s*([\d,]+)\s*(VND|USD|vnđ|usd)?'
        match = re.search(pattern_full, salary_string, re.IGNORECASE)
        if match:
            min_sal = int(match.group(1).replace(',', ''))
            max_sal = int(match.group(2).replace(',', ''))
            currency = (match.group(3) or 'VND').upper()

            # Convert USD to VND (approximate rate)
            if currency == 'USD':
                min_sal = int(min_sal * 25000)
                max_sal = int(max_sal * 25000)
                currency = 'VND'

            # Handle "triệu" format: "25 - 45 triệu"
            if 'triệu' in salary_string.lower() or 'trieu' in salary_string.lower():
                if min_sal < 1000:  # Likely in millions
                    min_sal *= 1000000
                    max_sal *= 1000000

            return min_sal, max_sal, currency

        # Pattern 2: "25 - 45 triệu VND" or "8 - 15 triệu"
        pattern_trieu = r'(\d+)\s*[-–]\s*(\d+)\s*(?:triệu|trieu|tr)'
        match = re.search(pattern_trieu, salary_string, re.IGNORECASE)
        if match:
            min_sal = int(match.group(1)) * 1000000
            max_sal = int(match.group(2)) * 1000000
            return min_sal, max_sal, "VND"

        # Pattern 3: Single number with currency
        pattern_single = r'([\d,]+)\s*(VND|USD|triệu|trieu|tr)'
        match = re.search(pattern_single, salary_string, re.IGNORECASE)
        if match:
            salary = int(match.group(1).replace(',', ''))
            unit = match.group(2).lower()
            if unit in ['triệu', 'trieu', 'tr']:
                salary *= 1000000
            elif unit == 'usd':
                salary = int(salary * 25000)
            return salary, salary, "VND"

        # Pattern 4: "Negotiable", "Competitive", "Thương lượng", "Cạnh tranh"
        negotiable_patterns = r'(negotiable|competitive|thương lượng|cạnh tranh|thoả thuận|thỏa thuận)'
        if re.search(negotiable_patterns, salary_string, re.IGNORECASE):
            return 0, 0, "VND"

        return 0, 0, "VND"

    # ── Skill String Parsing ──────────────────────────────────────

    def parse_skills(self, skill_string):
        """
        Parse messy skill strings into clean, distinct keyword lists.
        Handles: comma-separated, slash-separated, and various formats.
        """
        if not skill_string or not isinstance(skill_string, str):
            return []

        # Normalize separators
        cleaned = re.sub(r'[;/|•·]', ',', skill_string)
        # Remove parenthetical content
        cleaned = re.sub(r'\([^)]*\)', '', cleaned)
        # Split by comma and clean each skill
        skills = [s.strip() for s in cleaned.split(',') if s.strip()]
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in skills:
            skill_upper = skill.upper()
            if skill_upper not in seen and len(skill) > 1:
                seen.add(skill_upper)
                unique_skills.append(skill)

        return unique_skills

    # ── Full Data Cleaning Pipeline ───────────────────────────────

    def clean_data(self, df=None):
        """
        Full data cleaning pipeline:
        1. Remove duplicates
        2. Handle missing values
        3. Normalize salaries
        4. Parse skills
        5. Standardize text fields
        """
        if df is not None:
            self.raw_data = df.copy()
        elif self.raw_data is None:
            self._log("No data to clean. Load data first.")
            return None

        df = self.raw_data.copy()
        self._log(f"Starting data cleaning pipeline with {len(df)} rows")

        # 1. Remove exact duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['title', 'company'], keep='first')
        removed = initial_count - len(df)
        if removed:
            self._log(f"Removed {removed} duplicate entries")

        # 2. Handle missing values
        df['title'] = df['title'].fillna('Unknown Position')
        df['company'] = df['company'].fillna('Unknown Company')
        df['location'] = df['location'].fillna('Not Specified')
        df['skills'] = df['skills'].fillna('')
        df['salary_raw'] = df['salary_raw'].fillna('Negotiable')

        # 3. Normalize salaries using Regex
        if 'salary_raw' in df.columns:
            salary_parsed = df['salary_raw'].apply(self.normalize_salary)
            df['salary_min'] = salary_parsed.apply(lambda x: x[0])
            df['salary_max'] = salary_parsed.apply(lambda x: x[1])
            df['salary_currency'] = salary_parsed.apply(lambda x: x[2])
            self._log("Salary normalization completed")

        # 4. Parse and clean skills
        if 'skills' in df.columns:
            df['skills_list'] = df['skills'].apply(self.parse_skills)
            df['skills_clean'] = df['skills_list'].apply(lambda x: ', '.join(x))
            self._log("Skill parsing completed")

        # 5. Standardize text fields
        df['title'] = df['title'].str.strip()
        df['company'] = df['company'].str.strip()
        df['location'] = df['location'].str.strip()

        self.cleaned_data = df
        self._log(f"Data cleaning completed. {len(df)} clean records ready.")
        return df

    def insert_into_db(self, db_manager, df=None):
        """Insert cleaned data into the SQLite database."""
        if df is None:
            df = self.cleaned_data
        if df is None:
            self._log("No cleaned data available for insertion.")
            return

        inserted = 0
        for _, row in df.iterrows():
            try:
                # Insert company
                company_name = row.get('company', 'Unknown')
                db_manager.cursor.execute(
                    'INSERT OR IGNORE INTO Companies (name, location) VALUES (?, ?)',
                    (company_name, row.get('location', ''))
                )
                db_manager.cursor.execute(
                    'SELECT id FROM Companies WHERE name = ?', (company_name,)
                )
                company_id = db_manager.cursor.fetchone()[0]

                # Insert job
                db_manager.cursor.execute('''
                    INSERT INTO Jobs (title, company_id, location, salary_min, salary_max,
                                      salary_currency, experience_level, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('title', ''),
                    company_id,
                    row.get('location', ''),
                    row.get('salary_min', 0),
                    row.get('salary_max', 0),
                    row.get('salary_currency', 'VND'),
                    row.get('experience', 'Not specified'),
                    row.get('source', 'Unknown')
                ))
                job_id = db_manager.cursor.lastrowid

                # Insert skills
                skills = row.get('skills_list', [])
                if isinstance(skills, str):
                    skills = self.parse_skills(skills)

                for skill_name in skills:
                    db_manager.cursor.execute(
                        'INSERT OR IGNORE INTO Skills (name) VALUES (?)',
                        (skill_name,)
                    )
                    db_manager.cursor.execute(
                        'SELECT id FROM Skills WHERE name = ?', (skill_name,)
                    )
                    skill_id = db_manager.cursor.fetchone()[0]
                    db_manager.cursor.execute(
                        'INSERT OR IGNORE INTO JobSkills (job_id, skill_id) VALUES (?, ?)',
                        (job_id, skill_id)
                    )

                inserted += 1
            except Exception as e:
                self._log(f"Error inserting row: {e}")
                continue

        db_manager.conn.commit()
        self._log(f"✅ Inserted {inserted} records into database")

    def get_summary(self):
        """Get a summary of the cleaned data."""
        if self.cleaned_data is None:
            return {"status": "No data processed yet"}

        df = self.cleaned_data
        return {
            "total_records": len(df),
            "unique_companies": df['company'].nunique(),
            "unique_titles": df['title'].nunique(),
            "has_salary": int((df.get('salary_min', 0) > 0).sum()),
            "avg_salary_min": int(df.loc[df.get('salary_min', 0) > 0, 'salary_min'].mean()) if 'salary_min' in df.columns else 0,
            "avg_salary_max": int(df.loc[df.get('salary_max', 0) > 0, 'salary_max'].mean()) if 'salary_max' in df.columns else 0,
        }

    def _log(self, message):
        """Log processing messages."""
        from datetime import datetime
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self.processing_log.append(entry)
        print(entry)
