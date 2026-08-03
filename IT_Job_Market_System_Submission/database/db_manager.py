import sqlite3
import os


class DBManager:
    """
    Database Manager for IT Job Market Intelligence System.
    Manages SQLite database with normalized schema:
    - Jobs: Job listings with title, company, location, salary, experience
    - Companies: Unique companies
    - Skills: Unique technical skills
    - JobSkills: Many-to-many relationship between Jobs and Skills
    """

    def __init__(self, db_name='database/data.db'):
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def setup_tables(self):
        """Create normalized database schema."""
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS Companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                industry TEXT,
                location TEXT
            );

            CREATE TABLE IF NOT EXISTS Skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT
            );

            CREATE TABLE IF NOT EXISTS Jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company_id INTEGER,
                location TEXT,
                salary_min INTEGER,
                salary_max INTEGER,
                salary_currency TEXT DEFAULT 'VND',
                experience_level TEXT,
                job_type TEXT DEFAULT 'Full-time',
                description TEXT,
                source TEXT,
                date_scraped TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (company_id) REFERENCES Companies(id)
            );

            CREATE TABLE IF NOT EXISTS JobSkills (
                job_id INTEGER,
                skill_id INTEGER,
                PRIMARY KEY (job_id, skill_id),
                FOREIGN KEY (job_id) REFERENCES Jobs(id),
                FOREIGN KEY (skill_id) REFERENCES Skills(id)
            );
        ''')
        self.conn.commit()
        print("✅ Database schema created successfully.")

    def insert_mock_data(self):
        """Insert 50+ realistic IT job listings focused on Vietnam's IT market."""
        # Clear existing data
        self.cursor.executescript('''
            DELETE FROM JobSkills;
            DELETE FROM Jobs;
            DELETE FROM Companies;
            DELETE FROM Skills;
        ''')

        # --- Companies ---
        companies = [
            ("FPT Software", "Software Services", "Ha Noi"),
            ("VNG Corporation", "Technology", "Ho Chi Minh"),
            ("Viettel Group", "Telecommunications", "Ha Noi"),
            ("Intel Vietnam", "Semiconductors", "Ho Chi Minh"),
            ("Samsung Vietnam", "Electronics", "Bac Ninh"),
            ("Bosch Vietnam", "Engineering", "Ho Chi Minh"),
            ("Marvell Vietnam", "Semiconductors", "Ho Chi Minh"),
            ("FPT Semiconductor", "Semiconductors", "Ha Noi"),
            ("Renesas Vietnam", "Semiconductors", "Ho Chi Minh"),
            ("Synopsys Vietnam", "EDA Tools", "Ho Chi Minh"),
            ("Toshiba Vietnam", "Electronics", "Ha Noi"),
            ("NashTech Vietnam", "Software Services", "Ho Chi Minh"),
            ("KMS Technology", "Software Services", "Ho Chi Minh"),
            ("TMA Solutions", "Software Services", "Ho Chi Minh"),
            ("NAB Innovation Centre", "FinTech", "Ho Chi Minh"),
            ("Grab Vietnam", "Technology", "Ho Chi Minh"),
            ("Shopee Vietnam", "E-commerce", "Ho Chi Minh"),
            ("VNPT Technology", "Telecommunications", "Ha Noi"),
            ("CMC Global", "Software Services", "Ha Noi"),
            ("Axon Active Vietnam", "Software Services", "Da Nang"),
        ]
        self.cursor.executemany(
            'INSERT OR IGNORE INTO Companies (name, industry, location) VALUES (?, ?, ?)',
            companies
        )

        # --- Skills ---
        skills_data = [
            ("Python", "Programming"), ("Java", "Programming"), ("JavaScript", "Programming"),
            ("C++", "Programming"), ("C", "Programming"), ("Go", "Programming"),
            ("TypeScript", "Programming"), ("Rust", "Programming"), ("Kotlin", "Programming"),
            ("Swift", "Programming"), ("PHP", "Programming"), ("Ruby", "Programming"),
            ("Verilog", "Hardware"), ("SystemVerilog", "Hardware"), ("VHDL", "Hardware"),
            ("FPGA", "Hardware"), ("UVM", "Hardware"), ("TCL", "Hardware"),
            ("RTOS", "Embedded"), ("ARM", "Embedded"), ("Embedded C", "Embedded"),
            ("React", "Frontend"), ("Angular", "Frontend"), ("Vue.js", "Frontend"),
            ("Node.js", "Backend"), ("Django", "Backend"), ("Spring Boot", "Backend"),
            ("Flask", "Backend"), ("FastAPI", "Backend"), (".NET", "Backend"),
            ("AWS", "Cloud"), ("Azure", "Cloud"), ("GCP", "Cloud"),
            ("Docker", "DevOps"), ("Kubernetes", "DevOps"), ("Jenkins", "DevOps"),
            ("Terraform", "DevOps"), ("CI/CD", "DevOps"), ("Git", "DevOps"),
            ("MySQL", "Database"), ("PostgreSQL", "Database"), ("MongoDB", "Database"),
            ("Redis", "Database"), ("SQL", "Database"), ("Elasticsearch", "Database"),
            ("TensorFlow", "AI/ML"), ("PyTorch", "AI/ML"), ("Scikit-learn", "AI/ML"),
            ("Machine Learning", "AI/ML"), ("Deep Learning", "AI/ML"), ("NLP", "AI/ML"),
            ("Linux", "System"), ("Agile", "Methodology"), ("Scrum", "Methodology"),
            ("Pandas", "Data"), ("Matplotlib", "Data"), ("EDA", "Hardware"),
        ]
        self.cursor.executemany(
            'INSERT OR IGNORE INTO Skills (name, category) VALUES (?, ?)',
            skills_data
        )
        self.conn.commit()

        # Get company and skill ID mappings
        self.cursor.execute('SELECT id, name FROM Companies')
        company_map = {row[1]: row[0] for row in self.cursor.fetchall()}

        self.cursor.execute('SELECT id, name FROM Skills')
        skill_map = {row[1]: row[0] for row in self.cursor.fetchall()}

        # --- Jobs (50+ listings) ---
        jobs = [
            # Semiconductor / IC Design
            ("IC Design Engineer", "Intel Vietnam", "Ho Chi Minh", 25000000, 45000000, "Mid", "Full-time", "Design and verify digital ICs", "ITviec", ["Verilog", "SystemVerilog", "Python", "C++", "Linux"]),
            ("Digital Verification Engineer", "Marvell Vietnam", "Ho Chi Minh", 30000000, 50000000, "Mid", "Full-time", "Develop UVM testbenches for SoC verification", "ITviec", ["SystemVerilog", "UVM", "Python", "C++", "Verilog"]),
            ("Physical Design Engineer", "FPT Semiconductor", "Ha Noi", 20000000, 40000000, "Junior", "Full-time", "Perform PnR and timing closure", "ITviec", ["Python", "TCL", "EDA", "Linux", "Verilog"]),
            ("FPGA Design Engineer", "Viettel Group", "Ha Noi", 18000000, 35000000, "Mid", "Full-time", "FPGA-based system design for telecom", "TopCV", ["Verilog", "FPGA", "C++", "VHDL", "Linux"]),
            ("ASIC Design Engineer", "Renesas Vietnam", "Ho Chi Minh", 28000000, 55000000, "Senior", "Full-time", "RTL design and synthesis", "ITviec", ["Verilog", "SystemVerilog", "Python", "TCL"]),
            ("DFT Engineer", "Synopsys Vietnam", "Ho Chi Minh", 32000000, 60000000, "Senior", "Full-time", "Design-for-test implementation", "ITviec", ["SystemVerilog", "Verilog", "TCL", "Python", "EDA"]),
            ("Analog IC Designer", "Intel Vietnam", "Ho Chi Minh", 35000000, 65000000, "Senior", "Full-time", "Analog/mixed-signal IC design", "ITviec", ["Verilog", "Python", "C++", "FPGA"]),
            ("Chip Verification Lead", "Samsung Vietnam", "Bac Ninh", 40000000, 70000000, "Senior", "Full-time", "Lead verification team", "VietnamWorks", ["SystemVerilog", "UVM", "Python", "Verilog", "C++"]),

            # Embedded Systems
            ("Embedded Software Engineer", "Bosch Vietnam", "Ho Chi Minh", 20000000, 40000000, "Mid", "Full-time", "Develop embedded firmware for automotive", "ITviec", ["C", "C++", "RTOS", "ARM", "Embedded C"]),
            ("Embedded Linux Developer", "Viettel Group", "Ha Noi", 18000000, 32000000, "Junior", "Full-time", "BSP development for embedded Linux", "TopCV", ["C", "Linux", "Python", "ARM", "Git"]),
            ("IoT Engineer", "FPT Software", "Ha Noi", 15000000, 30000000, "Junior", "Full-time", "Design IoT solutions", "ITviec", ["C++", "Python", "RTOS", "ARM", "AWS"]),
            ("Firmware Engineer", "Samsung Vietnam", "Bac Ninh", 22000000, 42000000, "Mid", "Full-time", "Develop firmware for consumer electronics", "VietnamWorks", ["C", "C++", "RTOS", "ARM", "Linux"]),
            ("Automotive Software Engineer", "Bosch Vietnam", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "AUTOSAR-based software development", "ITviec", ["C", "C++", "Python", "RTOS", "Linux"]),

            # Backend / Full-stack
            ("Backend Developer (Python)", "VNG Corporation", "Ho Chi Minh", 20000000, 40000000, "Mid", "Full-time", "Build scalable backend services", "ITviec", ["Python", "Django", "PostgreSQL", "Docker", "Redis"]),
            ("Java Backend Developer", "FPT Software", "Ha Noi", 18000000, 35000000, "Mid", "Full-time", "Enterprise Java applications", "TopCV", ["Java", "Spring Boot", "MySQL", "Docker", "Git"]),
            ("Full-stack Developer", "KMS Technology", "Ho Chi Minh", 22000000, 45000000, "Mid", "Full-time", "Build web applications end-to-end", "ITviec", ["JavaScript", "React", "Node.js", "MongoDB", "Docker"]),
            ("Senior Backend Engineer", "Grab Vietnam", "Ho Chi Minh", 35000000, 65000000, "Senior", "Full-time", "Design microservices architecture", "ITviec", ["Go", "Python", "Kubernetes", "AWS", "PostgreSQL"]),
            ("Node.js Developer", "NashTech Vietnam", "Ho Chi Minh", 18000000, 35000000, "Mid", "Full-time", "RESTful API development", "ITviec", ["JavaScript", "Node.js", "TypeScript", "MongoDB", "Docker"]),
            (".NET Developer", "CMC Global", "Ha Noi", 16000000, 32000000, "Junior", "Full-time", "Enterprise software with .NET", "TopCV", [".NET", "C++", "SQL", "Azure", "Git"]),
            ("Python Developer", "TMA Solutions", "Ho Chi Minh", 15000000, 30000000, "Junior", "Full-time", "Python web and automation", "ITviec", ["Python", "Flask", "PostgreSQL", "Docker", "Git"]),
            ("FastAPI Developer", "NAB Innovation Centre", "Ho Chi Minh", 28000000, 50000000, "Mid", "Full-time", "High-performance API services", "ITviec", ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"]),

            # Frontend
            ("React Developer", "Shopee Vietnam", "Ho Chi Minh", 22000000, 45000000, "Mid", "Full-time", "Build e-commerce UI components", "ITviec", ["JavaScript", "React", "TypeScript", "Git", "Agile"]),
            ("Angular Developer", "FPT Software", "Da Nang", 16000000, 32000000, "Junior", "Full-time", "Enterprise Angular applications", "TopCV", ["JavaScript", "Angular", "TypeScript", "Git", "Agile"]),
            ("Vue.js Developer", "Axon Active Vietnam", "Da Nang", 18000000, 36000000, "Mid", "Full-time", "SPA development with Vue", "ITviec", ["JavaScript", "Vue.js", "TypeScript", "Node.js", "Git"]),
            ("Frontend Lead", "VNG Corporation", "Ho Chi Minh", 30000000, 55000000, "Senior", "Full-time", "Lead frontend architecture", "ITviec", ["React", "TypeScript", "JavaScript", "Git", "Agile"]),

            # DevOps / Cloud
            ("DevOps Engineer", "FPT Software", "Ha Noi", 22000000, 45000000, "Mid", "Full-time", "CI/CD pipeline management", "ITviec", ["Docker", "Kubernetes", "Jenkins", "AWS", "Linux"]),
            ("Cloud Engineer", "VNG Corporation", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "AWS infrastructure management", "ITviec", ["AWS", "Terraform", "Docker", "Kubernetes", "Python"]),
            ("SRE Engineer", "Grab Vietnam", "Ho Chi Minh", 35000000, 60000000, "Senior", "Full-time", "Site reliability and monitoring", "ITviec", ["Kubernetes", "Docker", "Python", "AWS", "Linux"]),
            ("Azure DevOps Engineer", "CMC Global", "Ha Noi", 20000000, 38000000, "Mid", "Full-time", "Azure cloud infrastructure", "TopCV", ["Azure", "Docker", "CI/CD", "Terraform", "Git"]),

            # Data / AI / ML
            ("Data Engineer", "Shopee Vietnam", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "Build data pipelines", "ITviec", ["Python", "SQL", "AWS", "Docker", "Pandas"]),
            ("Machine Learning Engineer", "VNG Corporation", "Ho Chi Minh", 30000000, 60000000, "Mid", "Full-time", "Build ML models for production", "ITviec", ["Python", "TensorFlow", "PyTorch", "Docker", "AWS"]),
            ("Data Scientist", "FPT Software", "Ha Noi", 22000000, 45000000, "Mid", "Full-time", "Statistical analysis and modeling", "TopCV", ["Python", "Scikit-learn", "Pandas", "SQL", "Matplotlib"]),
            ("NLP Engineer", "Grab Vietnam", "Ho Chi Minh", 35000000, 65000000, "Senior", "Full-time", "Natural language processing systems", "ITviec", ["Python", "PyTorch", "NLP", "Docker", "AWS"]),
            ("AI Research Engineer", "Samsung Vietnam", "Bac Ninh", 35000000, 70000000, "Senior", "Full-time", "Computer vision research", "VietnamWorks", ["Python", "PyTorch", "Deep Learning", "C++", "Linux"]),
            ("Data Analyst", "NAB Innovation Centre", "Ho Chi Minh", 18000000, 35000000, "Junior", "Full-time", "Business intelligence and reporting", "ITviec", ["Python", "SQL", "Pandas", "Matplotlib", "Elasticsearch"]),

            # Mobile
            ("Android Developer", "VNG Corporation", "Ho Chi Minh", 20000000, 40000000, "Mid", "Full-time", "Android app development", "ITviec", ["Kotlin", "Java", "Git", "Agile", "SQL"]),
            ("iOS Developer", "Grab Vietnam", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "iOS app development", "ITviec", ["Swift", "Git", "Agile", "SQL", "CI/CD"]),

            # QA / Testing
            ("QA Automation Engineer", "KMS Technology", "Ho Chi Minh", 18000000, 35000000, "Mid", "Full-time", "Automated testing frameworks", "ITviec", ["Python", "Java", "Selenium", "Git", "Agile"]),
            ("Performance Test Engineer", "TMA Solutions", "Ho Chi Minh", 16000000, 30000000, "Junior", "Full-time", "Load and performance testing", "TopCV", ["Python", "Java", "Linux", "Docker", "Git"]),

            # Security
            ("Security Engineer", "VNPT Technology", "Ha Noi", 22000000, 45000000, "Mid", "Full-time", "Network security and penetration testing", "TopCV", ["Python", "Linux", "Docker", "AWS", "Git"]),

            # Management / Lead
            ("Technical Lead (Python)", "NashTech Vietnam", "Ho Chi Minh", 40000000, 70000000, "Senior", "Full-time", "Lead Python development team", "ITviec", ["Python", "Django", "AWS", "Docker", "PostgreSQL"]),
            ("Engineering Manager", "Shopee Vietnam", "Ho Chi Minh", 50000000, 90000000, "Senior", "Full-time", "Manage engineering teams", "ITviec", ["Python", "Java", "AWS", "Agile", "Scrum"]),

            # Additional roles for diversity
            ("PHP Developer", "TMA Solutions", "Ho Chi Minh", 12000000, 25000000, "Junior", "Full-time", "Web development with Laravel", "TopCV", ["PHP", "JavaScript", "MySQL", "Git", "Docker"]),
            ("Ruby on Rails Developer", "Axon Active Vietnam", "Da Nang", 20000000, 40000000, "Mid", "Full-time", "Full-stack Ruby development", "ITviec", ["Ruby", "JavaScript", "PostgreSQL", "Docker", "Git"]),
            ("Rust Systems Developer", "Grab Vietnam", "Ho Chi Minh", 40000000, 75000000, "Senior", "Full-time", "High-performance systems", "ITviec", ["Rust", "Go", "Linux", "Docker", "Kubernetes"]),
            ("GCP Cloud Architect", "FPT Software", "Ha Noi", 35000000, 65000000, "Senior", "Full-time", "Google Cloud architecture", "TopCV", ["GCP", "Kubernetes", "Docker", "Terraform", "Python"]),
            ("Database Administrator", "VNPT Technology", "Ha Noi", 15000000, 30000000, "Mid", "Full-time", "Database management and optimization", "TopCV", ["MySQL", "PostgreSQL", "Redis", "Linux", "Python"]),
            ("Blockchain Developer", "VNG Corporation", "Ho Chi Minh", 30000000, 60000000, "Mid", "Full-time", "Smart contract development", "ITviec", ["JavaScript", "Python", "Go", "Docker", "Git"]),
            ("Scrum Master", "KMS Technology", "Ho Chi Minh", 25000000, 45000000, "Mid", "Full-time", "Agile project facilitation", "ITviec", ["Agile", "Scrum", "Git", "Python", "SQL"]),
            ("Junior Python Developer", "CMC Global", "Ha Noi", 8000000, 15000000, "Junior", "Full-time", "Entry-level Python programming", "TopCV", ["Python", "Git", "SQL", "Linux", "Flask"]),
            ("Senior Java Developer", "FPT Software", "Ha Noi", 30000000, 55000000, "Senior", "Full-time", "Microservices with Spring Boot", "ITviec", ["Java", "Spring Boot", "Docker", "Kubernetes", "PostgreSQL"]),
        ]

        for job in jobs:
            title, company, location, sal_min, sal_max, exp, jtype, desc, source, skill_names = job
            company_id = company_map.get(company)
            if not company_id:
                continue

            self.cursor.execute('''
                INSERT INTO Jobs (title, company_id, location, salary_min, salary_max,
                                  salary_currency, experience_level, job_type, description, source)
                VALUES (?, ?, ?, ?, ?, 'VND', ?, ?, ?, ?)
            ''', (title, company_id, location, sal_min, sal_max, exp, jtype, desc, source))
            job_id = self.cursor.lastrowid

            for skill_name in skill_names:
                skill_id = skill_map.get(skill_name)
                if skill_id:
                    self.cursor.execute(
                        'INSERT OR IGNORE INTO JobSkills (job_id, skill_id) VALUES (?, ?)',
                        (job_id, skill_id)
                    )

        self.conn.commit()
        print(f"✅ Inserted {len(jobs)} job listings with skills into the database.")

    # ── Query Methods for Analytics ──────────────────────────────────

    def get_all_jobs(self, limit=100, offset=0, search=None):
        """Get all jobs with company names and skills."""
        query = '''
            SELECT j.id, j.title, c.name as company, j.location,
                   j.salary_min, j.salary_max, j.experience_level,
                   j.job_type, j.source, j.date_scraped,
                   GROUP_CONCAT(s.name, ', ') as skills
            FROM Jobs j
            LEFT JOIN Companies c ON j.company_id = c.id
            LEFT JOIN JobSkills js ON j.id = js.job_id
            LEFT JOIN Skills s ON js.skill_id = s.id
        '''
        params = []
        if search:
            query += " WHERE j.title LIKE ? OR c.name LIKE ? OR s.name LIKE ?"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])

        query += " GROUP BY j.id ORDER BY j.id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_job_by_id(self, job_id):
        """Get details for a single job by ID."""
        self.cursor.execute('''
            SELECT j.*, c.name as company, c.industry,
                   GROUP_CONCAT(s.name, ', ') as skills
            FROM Jobs j
            LEFT JOIN Companies c ON j.company_id = c.id
            LEFT JOIN JobSkills js ON j.id = js.job_id
            LEFT JOIN Skills s ON js.skill_id = s.id
            WHERE j.id = ?
            GROUP BY j.id
        ''', (job_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_job_count(self):
        """Get total number of jobs."""
        self.cursor.execute('SELECT COUNT(*) FROM Jobs')
        return self.cursor.fetchone()[0]

    def get_company_count(self):
        """Get total number of companies."""
        self.cursor.execute('SELECT COUNT(*) FROM Companies')
        return self.cursor.fetchone()[0]

    def get_skill_frequency(self, limit=20):
        """Get top skills by frequency."""
        self.cursor.execute('''
            SELECT s.name, s.category, COUNT(js.job_id) as frequency
            FROM Skills s
            JOIN JobSkills js ON s.id = js.skill_id
            GROUP BY s.id
            ORDER BY frequency DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_salary_by_experience(self):
        """Get average salary by experience level."""
        self.cursor.execute('''
            SELECT experience_level,
                   AVG(salary_min) as avg_min,
                   AVG(salary_max) as avg_max,
                   AVG((salary_min + salary_max) / 2) as avg_salary,
                   MIN(salary_min) as min_salary,
                   MAX(salary_max) as max_salary,
                   COUNT(*) as job_count
            FROM Jobs
            WHERE experience_level IS NOT NULL
            GROUP BY experience_level
            ORDER BY avg_salary
        ''')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_top_companies(self, limit=10):
        """Get companies with most job listings."""
        self.cursor.execute('''
            SELECT c.name, c.industry, c.location, COUNT(j.id) as job_count
            FROM Companies c
            JOIN Jobs j ON c.id = j.company_id
            GROUP BY c.id
            ORDER BY job_count DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_jobs_by_source(self):
        """Get job count by source website."""
        self.cursor.execute('''
            SELECT source, COUNT(*) as count
            FROM Jobs
            GROUP BY source
            ORDER BY count DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_skills_by_category(self):
        """Get skill distribution by category."""
        self.cursor.execute('''
            SELECT s.category, COUNT(DISTINCT js.job_id) as job_count
            FROM Skills s
            JOIN JobSkills js ON s.id = js.skill_id
            GROUP BY s.category
            ORDER BY job_count DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_jobs_by_location(self):
        """Get job count by location."""
        self.cursor.execute('''
            SELECT location, COUNT(*) as count
            FROM Jobs
            GROUP BY location
            ORDER BY count DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_skills_from_db(self):
        """Legacy method: Get all skills as comma-separated strings."""
        self.cursor.execute('''
            SELECT GROUP_CONCAT(s.name, ', ') as skills
            FROM Jobs j
            JOIN JobSkills js ON j.id = js.job_id
            JOIN Skills s ON js.skill_id = s.id
            GROUP BY j.id
        ''')
        return [row[0] for row in self.cursor.fetchall()]

    def get_avg_salary(self):
        """Get overall average salary."""
        self.cursor.execute('SELECT AVG((salary_min + salary_max) / 2) FROM Jobs')
        result = self.cursor.fetchone()[0]
        return int(result) if result else 0

    def get_all_skill_names(self):
        """Get all unique skill names."""
        self.cursor.execute('''
            SELECT DISTINCT s.name
            FROM Skills s
            JOIN JobSkills js ON s.id = js.skill_id
            ORDER BY s.name
        ''')
        return [row[0] for row in self.cursor.fetchall()]

    def close(self):
        """Close database connection."""
        self.conn.close()