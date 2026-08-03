import sqlite3
import os
import sys
import hashlib
import secrets

# Ensure utf-8 stdout on Windows console
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def hash_password(password, salt=None):
    """Hash password using SHA-256 with random salt."""
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password, stored_hash):
    """Verify plain password against stored salt:hash."""
    try:
        if not stored_hash or ':' not in stored_hash:
            return False
        salt, hashed = stored_hash.split(':', 1)
        return hashlib.sha256((salt + password).encode('utf-8')).hexdigest() == hashed
    except Exception:
        return False


class DBManager:
    """
    Database Manager for IT Job Market Intelligence System.
    Manages SQLite database with normalized schema:
    - Jobs: Job listings with title, company, location, salary, experience, degree requirement
    - Companies: Unique companies
    - Skills: Unique technical skills
    - JobSkills: Many-to-many relationship between Jobs and Skills
    - Certificates: Unique IT and language certifications
    - JobCertificates: Many-to-many relationship between Jobs and Certificates
    - Users: User account authentication, profiles, saved skills, certificates & degrees
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

            CREATE TABLE IF NOT EXISTS Certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                issuer TEXT,
                level TEXT
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
                degree_required TEXT DEFAULT 'Đại học (Bachelor)',
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

            CREATE TABLE IF NOT EXISTS JobCertificates (
                job_id INTEGER,
                cert_id INTEGER,
                is_required INTEGER DEFAULT 0,
                PRIMARY KEY (job_id, cert_id),
                FOREIGN KEY (job_id) REFERENCES Jobs(id),
                FOREIGN KEY (cert_id) REFERENCES Certificates(id)
            );

            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'JobSeeker',
                skills TEXT DEFAULT '',
                certificates TEXT DEFAULT '',
                degree TEXT DEFAULT 'Đại học (Bachelor)',
                experience_level TEXT DEFAULT 'Junior',
                created_at TEXT DEFAULT (datetime('now'))
            );
        ''')
        self.conn.commit()

        # Migrate existing Jobs table if degree_required column is missing
        try:
            self.cursor.execute("SELECT degree_required FROM Jobs LIMIT 1")
        except sqlite3.OperationalError:
            try:
                self.cursor.execute("ALTER TABLE Jobs ADD COLUMN degree_required TEXT DEFAULT 'Đại học (Bachelor)'")
                self.conn.commit()
            except Exception:
                pass

        print("✅ Database schema created successfully.")

    def insert_mock_data(self):
        """Insert 50+ realistic IT job listings, certificates, and demo accounts."""
        # Clear existing data
        self.cursor.executescript('''
            DELETE FROM JobCertificates;
            DELETE FROM JobSkills;
            DELETE FROM Jobs;
            DELETE FROM Companies;
            DELETE FROM Skills;
            DELETE FROM Certificates;
            DELETE FROM Users;
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

        # --- Certificates ---
        certs_data = [
            ("AWS Certified Solutions Architect", "Cloud", "Amazon Web Services", "Associate/Professional"),
            ("AWS Certified Developer", "Cloud", "Amazon Web Services", "Associate"),
            ("AWS Certified SysOps Administrator", "Cloud", "Amazon Web Services", "Associate"),
            ("AWS Certified Machine Learning", "AI/Data", "Amazon Web Services", "Specialty"),
            ("Microsoft Certified: Azure Solutions Architect", "Cloud", "Microsoft", "Expert"),
            ("Microsoft Certified: Azure Developer Associate", "Cloud", "Microsoft", "Associate"),
            ("Google Cloud Certified Professional Cloud Architect", "Cloud", "Google", "Professional"),
            ("CKA (Certified Kubernetes Administrator)", "DevOps", "CNCF / Linux Foundation", "Professional"),
            ("CKAD (Certified Kubernetes Application Developer)", "DevOps", "CNCF / Linux Foundation", "Associate"),
            ("Docker Certified Associate (DCA)", "DevOps", "Docker / Mirantis", "Associate"),
            ("HashiCorp Certified: Terraform Associate", "DevOps", "HashiCorp", "Associate"),
            ("CCNA (Cisco Certified Network Associate)", "Security/Network", "Cisco", "Associate"),
            ("CCNP (Cisco Certified Network Professional)", "Security/Network", "Cisco", "Professional"),
            ("CEH (Certified Ethical Hacker)", "Security/Network", "EC-Council", "Professional"),
            ("CompTIA Security+", "Security/Network", "CompTIA", "Fundamental"),
            ("PMP (Project Management Professional)", "Management/Agile", "PMI", "Expert"),
            ("PSM I (Professional Scrum Master)", "Management/Agile", "Scrum.org", "Associate"),
            ("PMI-ACP (Agile Certified Practitioner)", "Management/Agile", "PMI", "Professional"),
            ("Oracle Certified Professional: Java SE", "Programming", "Oracle", "Professional"),
            ("TensorFlow Developer Certificate", "AI/Data", "Google", "Associate"),
            ("Databricks Certified Data Engineer", "AI/Data", "Databricks", "Associate/Professional"),
            ("TOEIC 750+", "Language", "ETS", "Intermediate"),
            ("TOEIC 850+", "Language", "ETS", "Advanced"),
            ("IELTS 6.5+", "Language", "British Council / IDP", "Intermediate"),
            ("IELTS 7.5+", "Language", "British Council / IDP", "Advanced"),
            ("JLPT N3", "Language", "Japan Foundation", "Intermediate"),
            ("JLPT N2", "Language", "Japan Foundation", "Advanced"),
            ("JLPT N1", "Language", "Japan Foundation", "Fluent/Master"),
        ]
        self.cursor.executemany(
            'INSERT OR IGNORE INTO Certificates (name, category, issuer, level) VALUES (?, ?, ?, ?)',
            certs_data
        )

        # --- Demo Users ---
        demo_users = [
            ("student", "student@demo.com", hash_password("123456"), "Nguyễn Văn An (Fresher)", "JobSeeker",
             "Python, Flask, Git, SQL", "TOEIC 750+", "Đại học (Bachelor)", "Fresher"),
            ("developer", "dev@demo.com", hash_password("123456"), "Trần Thị Mai (Fullstack Dev)", "JobSeeker",
             "JavaScript, React, Node.js, TypeScript, PostgreSQL, Docker", "AWS Certified Developer, IELTS 6.5+", "Kỹ sư (Engineer)", "Mid"),
            ("lead", "lead@demo.com", hash_password("123456"), "Lê Hoàng Nam (DevOps / Tech Lead)", "JobSeeker",
             "Python, Go, Docker, Kubernetes, AWS, Terraform, CI/CD, Linux", "AWS Certified Solutions Architect, CKA, PSM I", "Thạc sĩ (Master)", "Senior"),
        ]
        self.cursor.executemany(
            'INSERT OR IGNORE INTO Users (username, email, password_hash, full_name, role, skills, certificates, degree, experience_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            demo_users
        )
        self.conn.commit()

        # Get ID mappings
        self.cursor.execute('SELECT id, name FROM Companies')
        company_map = {row[1]: row[0] for row in self.cursor.fetchall()}

        self.cursor.execute('SELECT id, name FROM Skills')
        skill_map = {row[1]: row[0] for row in self.cursor.fetchall()}

        self.cursor.execute('SELECT id, name FROM Certificates')
        cert_map = {row[1]: row[0] for row in self.cursor.fetchall()}

        # --- Jobs (50+ listings with degree requirements and certificate preferences) ---
        jobs = [
            # Semiconductor / IC Design
            ("IC Design Engineer", "Intel Vietnam", "Ho Chi Minh", 25000000, 45000000, "Mid", "Full-time", "Kỹ sư (Engineer)", "Design and verify digital ICs", "ITviec",
             ["Verilog", "SystemVerilog", "Python", "C++", "Linux"], ["TOEIC 750+"]),
            ("Digital Verification Engineer", "Marvell Vietnam", "Ho Chi Minh", 30000000, 50000000, "Mid", "Full-time", "Đại học (Bachelor)", "Develop UVM testbenches for SoC verification", "ITviec",
             ["SystemVerilog", "UVM", "Python", "C++", "Verilog"], ["IELTS 6.5+"]),
            ("Physical Design Engineer", "FPT Semiconductor", "Ha Noi", 20000000, 40000000, "Junior", "Full-time", "Đại học (Bachelor)", "Perform PnR and timing closure", "ITviec",
             ["Python", "TCL", "EDA", "Linux", "Verilog"], []),
            ("FPGA Design Engineer", "Viettel Group", "Ha Noi", 18000000, 35000000, "Mid", "Full-time", "Kỹ sư (Engineer)", "FPGA-based system design for telecom", "TopCV",
             ["Verilog", "FPGA", "C++", "VHDL", "Linux"], []),
            ("ASIC Design Engineer", "Renesas Vietnam", "Ho Chi Minh", 28000000, 55000000, "Senior", "Full-time", "Đại học (Bachelor)", "RTL design and synthesis", "ITviec",
             ["Verilog", "SystemVerilog", "Python", "TCL"], ["JLPT N3", "JLPT N2"]),
            ("DFT Engineer", "Synopsys Vietnam", "Ho Chi Minh", 32000000, 60000000, "Senior", "Full-time", "Thạc sĩ (Master)", "Design-for-test implementation", "ITviec",
             ["SystemVerilog", "Verilog", "TCL", "Python", "EDA"], ["IELTS 7.5+"]),
            ("Analog IC Designer", "Intel Vietnam", "Ho Chi Minh", 35000000, 65000000, "Senior", "Full-time", "Kỹ sư (Engineer)", "Analog/mixed-signal IC design", "ITviec",
             ["Verilog", "Python", "C++", "FPGA"], ["TOEIC 850+"]),
            ("Chip Verification Lead", "Samsung Vietnam", "Bac Ninh", 40000000, 70000000, "Senior", "Full-time", "Thạc sĩ (Master)", "Lead verification team", "VietnamWorks",
             ["SystemVerilog", "UVM", "Python", "Verilog", "C++"], ["PMP (Project Management Professional)", "IELTS 6.5+"]),

            # Embedded Systems
            ("Embedded Software Engineer", "Bosch Vietnam", "Ho Chi Minh", 20000000, 40000000, "Mid", "Full-time", "Kỹ sư (Engineer)", "Develop embedded firmware for automotive", "ITviec",
             ["C", "C++", "RTOS", "ARM", "Embedded C"], ["TOEIC 750+"]),
            ("Embedded Linux Developer", "Viettel Group", "Ha Noi", 18000000, 32000000, "Junior", "Full-time", "Đại học (Bachelor)", "BSP development for embedded Linux", "TopCV",
             ["C", "Linux", "Python", "ARM", "Git"], []),
            ("IoT Engineer", "FPT Software", "Ha Noi", 15000000, 30000000, "Junior", "Full-time", "Đại học (Bachelor)", "Design IoT solutions", "ITviec",
             ["C++", "Python", "RTOS", "ARM", "AWS"], ["AWS Certified Developer"]),
            ("Firmware Engineer", "Samsung Vietnam", "Bac Ninh", 22000000, 42000000, "Mid", "Full-time", "Kỹ sư (Engineer)", "Develop firmware for consumer electronics", "VietnamWorks",
             ["C", "C++", "RTOS", "ARM", "Linux"], ["TOEIC 750+"]),
            ("Automotive Software Engineer", "Bosch Vietnam", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "Kỹ sư (Engineer)", "AUTOSAR-based software development", "ITviec",
             ["C", "C++", "Python", "RTOS", "Linux"], ["IELTS 6.5+"]),

            # Backend / Full-stack
            ("Backend Developer (Python)", "VNG Corporation", "Ho Chi Minh", 20000000, 40000000, "Mid", "Full-time", "Đại học (Bachelor)", "Build scalable backend services", "ITviec",
             ["Python", "Django", "PostgreSQL", "Docker", "Redis"], ["AWS Certified Developer"]),
            ("Java Backend Developer", "FPT Software", "Ha Noi", 18000000, 35000000, "Mid", "Full-time", "Đại học (Bachelor)", "Enterprise Java applications", "TopCV",
             ["Java", "Spring Boot", "MySQL", "Docker", "Git"], ["Oracle Certified Professional: Java SE", "TOEIC 750+"]),
            ("Full-stack Developer", "KMS Technology", "Ho Chi Minh", 22000000, 45000000, "Mid", "Full-time", "Đại học (Bachelor)", "Build web applications end-to-end", "ITviec",
             ["JavaScript", "React", "Node.js", "MongoDB", "Docker"], ["AWS Certified Developer"]),
            ("Senior Backend Engineer", "Grab Vietnam", "Ho Chi Minh", 35000000, 65000000, "Senior", "Full-time", "Đại học (Bachelor)", "Design microservices architecture", "ITviec",
             ["Go", "Python", "Kubernetes", "AWS", "PostgreSQL"], ["AWS Certified Solutions Architect", "CKA (Certified Kubernetes Administrator)"]),
            ("Node.js Developer", "NashTech Vietnam", "Ho Chi Minh", 18000000, 35000000, "Mid", "Full-time", "Đại học (Bachelor)", "RESTful API development", "ITviec",
             ["JavaScript", "Node.js", "TypeScript", "MongoDB", "Docker"], ["TOEIC 750+"]),
            (".NET Developer", "CMC Global", "Ha Noi", 16000000, 32000000, "Junior", "Full-time", "Cao đẳng / Tự học", "Enterprise software with .NET", "TopCV",
             [".NET", "C++", "SQL", "Azure", "Git"], ["Microsoft Certified: Azure Developer Associate"]),
            ("Python Developer", "TMA Solutions", "Ho Chi Minh", 15000000, 30000000, "Junior", "Full-time", "Đại học (Bachelor)", "Python web and automation", "ITviec",
             ["Python", "Flask", "PostgreSQL", "Docker", "Git"], []),
            ("FastAPI Developer", "NAB Innovation Centre", "Ho Chi Minh", 28000000, 50000000, "Mid", "Full-time", "Đại học (Bachelor)", "High-performance API services", "ITviec",
             ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS"], ["AWS Certified Solutions Architect", "IELTS 6.5+"]),

            # Frontend
            ("React Developer", "Shopee Vietnam", "Ho Chi Minh", 22000000, 45000000, "Mid", "Full-time", "Đại học (Bachelor)", "Build e-commerce UI components", "ITviec",
             ["JavaScript", "React", "TypeScript", "Git", "Agile"], ["PSM I (Professional Scrum Master)"]),
            ("Angular Developer", "FPT Software", "Da Nang", 16000000, 32000000, "Junior", "Full-time", "Đại học (Bachelor)", "Enterprise Angular applications", "TopCV",
             ["JavaScript", "Angular", "TypeScript", "Git", "Agile"], ["JLPT N3"]),
            ("Vue.js Developer", "Axon Active Vietnam", "Da Nang", 18000000, 36000000, "Mid", "Full-time", "Đại học (Bachelor)", "SPA development with Vue", "ITviec",
             ["JavaScript", "Vue.js", "TypeScript", "Node.js", "Git"], ["PSM I (Professional Scrum Master)"]),
            ("Frontend Lead", "VNG Corporation", "Ho Chi Minh", 30000000, 55000000, "Senior", "Full-time", "Đại học (Bachelor)", "Lead frontend architecture", "ITviec",
             ["React", "TypeScript", "JavaScript", "Git", "Agile"], ["PSM I (Professional Scrum Master)", "IELTS 6.5+"]),

            # DevOps / Cloud
            ("DevOps Engineer", "FPT Software", "Ha Noi", 22000000, 45000000, "Mid", "Full-time", "Đại học (Bachelor)", "CI/CD pipeline management", "ITviec",
             ["Docker", "Kubernetes", "Jenkins", "AWS", "Linux"], ["AWS Certified Solutions Architect", "Docker Certified Associate (DCA)"]),
            ("Cloud Engineer", "VNG Corporation", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "Đại học (Bachelor)", "AWS infrastructure management", "ITviec",
             ["AWS", "Terraform", "Docker", "Kubernetes", "Python"], ["AWS Certified Solutions Architect", "HashiCorp Certified: Terraform Associate"]),
            ("SRE Engineer", "Grab Vietnam", "Ho Chi Minh", 35000000, 60000000, "Senior", "Full-time", "Đại học (Bachelor)", "Site reliability and monitoring", "ITviec",
             ["Kubernetes", "Docker", "Python", "AWS", "Linux"], ["CKA (Certified Kubernetes Administrator)", "AWS Certified Solutions Architect"]),
            ("Azure DevOps Engineer", "CMC Global", "Ha Noi", 20000000, 38000000, "Mid", "Full-time", "Đại học (Bachelor)", "Azure cloud infrastructure", "TopCV",
             ["Azure", "Docker", "CI/CD", "Terraform", "Git"], ["Microsoft Certified: Azure Developer Associate"]),

            # Data / AI / ML
            ("Data Engineer", "Shopee Vietnam", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "Đại học (Bachelor)", "Build data pipelines", "ITviec",
             ["Python", "SQL", "AWS", "Docker", "Pandas"], ["Databricks Certified Data Engineer", "AWS Certified Solutions Architect"]),
            ("Machine Learning Engineer", "VNG Corporation", "Ho Chi Minh", 30000000, 60000000, "Mid", "Full-time", "Thạc sĩ (Master)", "Build ML models for production", "ITviec",
             ["Python", "TensorFlow", "PyTorch", "Docker", "AWS"], ["TensorFlow Developer Certificate", "AWS Certified Machine Learning"]),
            ("Data Scientist", "FPT Software", "Ha Noi", 22000000, 45000000, "Mid", "Full-time", "Thạc sĩ (Master)", "Statistical analysis and modeling", "TopCV",
             ["Python", "Scikit-learn", "Pandas", "SQL", "Matplotlib"], ["TensorFlow Developer Certificate", "TOEIC 750+"]),
            ("NLP Engineer", "Grab Vietnam", "Ho Chi Minh", 35000000, 65000000, "Senior", "Full-time", "Thạc sĩ (Master)", "Natural language processing systems", "ITviec",
             ["Python", "PyTorch", "NLP", "Docker", "AWS"], ["AWS Certified Machine Learning", "IELTS 7.5+"]),
            ("AI Research Engineer", "Samsung Vietnam", "Bac Ninh", 35000000, 70000000, "Senior", "Full-time", "Thạc sĩ (Master)", "Computer vision research", "VietnamWorks",
             ["Python", "PyTorch", "Deep Learning", "C++", "Linux"], ["TensorFlow Developer Certificate", "TOEIC 850+"]),
            ("Data Analyst", "NAB Innovation Centre", "Ho Chi Minh", 18000000, 35000000, "Junior", "Full-time", "Đại học (Bachelor)", "Business intelligence and reporting", "ITviec",
             ["Python", "SQL", "Pandas", "Matplotlib", "Elasticsearch"], ["IELTS 6.5+"]),

            # Mobile
            ("Android Developer", "VNG Corporation", "Ho Chi Minh", 20000000, 40000000, "Mid", "Full-time", "Đại học (Bachelor)", "Android app development", "ITviec",
             ["Kotlin", "Java", "Git", "Agile", "SQL"], ["PSM I (Professional Scrum Master)"]),
            ("iOS Developer", "Grab Vietnam", "Ho Chi Minh", 25000000, 50000000, "Mid", "Full-time", "Đại học (Bachelor)", "iOS app development", "ITviec",
             ["Swift", "Git", "Agile", "SQL", "CI/CD"], ["IELTS 6.5+"]),

            # QA / Testing
            ("QA Automation Engineer", "KMS Technology", "Ho Chi Minh", 18000000, 35000000, "Mid", "Full-time", "Đại học (Bachelor)", "Automated testing frameworks", "ITviec",
             ["Python", "Java", "Selenium", "Git", "Agile"], ["PSM I (Professional Scrum Master)", "TOEIC 750+"]),
            ("Performance Test Engineer", "TMA Solutions", "Ho Chi Minh", 16000000, 30000000, "Junior", "Full-time", "Cao đẳng / Tự học", "Load and performance testing", "TopCV",
             ["Python", "Java", "Linux", "Docker", "Git"], []),

            # Security
            ("Security Engineer", "VNPT Technology", "Ha Noi", 22000000, 45000000, "Mid", "Full-time", "Kỹ sư (Engineer)", "Network security and penetration testing", "TopCV",
             ["Python", "Linux", "Docker", "AWS", "Git"], ["CCNA (Cisco Certified Network Associate)", "CompTIA Security+", "CEH (Certified Ethical Hacker)"]),

            # Management / Lead
            ("Technical Lead (Python)", "NashTech Vietnam", "Ho Chi Minh", 40000000, 70000000, "Senior", "Full-time", "Đại học (Bachelor)", "Lead Python development team", "ITviec",
             ["Python", "Django", "AWS", "Docker", "PostgreSQL"], ["AWS Certified Solutions Architect", "PMP (Project Management Professional)", "IELTS 6.5+"]),
            ("Engineering Manager", "Shopee Vietnam", "Ho Chi Minh", 50000000, 90000000, "Senior", "Full-time", "Thạc sĩ (Master)", "Manage engineering teams", "ITviec",
             ["Python", "Java", "AWS", "Agile", "Scrum"], ["PMP (Project Management Professional)", "PSM I (Professional Scrum Master)", "IELTS 7.5+"]),

            # Additional roles
            ("PHP Developer", "TMA Solutions", "Ho Chi Minh", 12000000, 25000000, "Junior", "Full-time", "Cao đẳng / Tự học", "Web development with Laravel", "TopCV",
             ["PHP", "JavaScript", "MySQL", "Git", "Docker"], []),
            ("Ruby on Rails Developer", "Axon Active Vietnam", "Da Nang", 20000000, 40000000, "Mid", "Full-time", "Đại học (Bachelor)", "Full-stack Ruby development", "ITviec",
             ["Ruby", "JavaScript", "PostgreSQL", "Docker", "Git"], ["PSM I (Professional Scrum Master)"]),
            ("Rust Systems Developer", "Grab Vietnam", "Ho Chi Minh", 40000000, 75000000, "Senior", "Full-time", "Kỹ sư (Engineer)", "High-performance systems", "ITviec",
             ["Rust", "Go", "Linux", "Docker", "Kubernetes"], ["CKA (Certified Kubernetes Administrator)", "IELTS 6.5+"]),
            ("GCP Cloud Architect", "FPT Software", "Ha Noi", 35000000, 65000000, "Senior", "Full-time", "Đại học (Bachelor)", "Google Cloud architecture", "TopCV",
             ["GCP", "Kubernetes", "Docker", "Terraform", "Python"], ["Google Cloud Certified Professional Cloud Architect", "TOEIC 850+"]),
            ("Database Administrator", "VNPT Technology", "Ha Noi", 15000000, 30000000, "Mid", "Full-time", "Đại học (Bachelor)", "Database management and optimization", "TopCV",
             ["MySQL", "PostgreSQL", "Redis", "Linux", "Python"], ["AWS Certified Solutions Architect"]),
            ("Blockchain Developer", "VNG Corporation", "Ho Chi Minh", 30000000, 60000000, "Mid", "Full-time", "Đại học (Bachelor)", "Smart contract development", "ITviec",
             ["JavaScript", "Python", "Go", "Docker", "Git"], ["AWS Certified Developer"]),
            ("Scrum Master", "KMS Technology", "Ho Chi Minh", 25000000, 45000000, "Mid", "Full-time", "Đại học (Bachelor)", "Agile project facilitation", "ITviec",
             ["Agile", "Scrum", "Git", "Python", "SQL"], ["PSM I (Professional Scrum Master)", "PMI-ACP (Agile Certified Practitioner)", "IELTS 6.5+"]),
            ("Junior Python Developer", "CMC Global", "Ha Noi", 8000000, 15000000, "Junior", "Full-time", "Cao đẳng / Tự học", "Entry-level Python programming", "TopCV",
             ["Python", "Git", "SQL", "Linux", "Flask"], ["TOEIC 750+"]),
            ("Senior Java Developer", "FPT Software", "Ha Noi", 30000000, 55000000, "Senior", "Full-time", "Đại học (Bachelor)", "Microservices with Spring Boot", "ITviec",
             ["Java", "Spring Boot", "Docker", "Kubernetes", "PostgreSQL"], ["Oracle Certified Professional: Java SE", "AWS Certified Solutions Architect", "JLPT N2"]),
        ]

        for job in jobs:
            title, company, location, sal_min, sal_max, exp, jtype, deg_req, desc, source, skill_names, cert_names = job
            company_id = company_map.get(company)
            if not company_id:
                continue

            self.cursor.execute('''
                INSERT INTO Jobs (title, company_id, location, salary_min, salary_max,
                                  salary_currency, experience_level, job_type, degree_required, description, source)
                VALUES (?, ?, ?, ?, ?, 'VND', ?, ?, ?, ?, ?)
            ''', (title, company_id, location, sal_min, sal_max, exp, jtype, deg_req, desc, source))
            job_id = self.cursor.lastrowid

            for skill_name in skill_names:
                skill_id = skill_map.get(skill_name)
                if skill_id:
                    self.cursor.execute(
                        'INSERT OR IGNORE INTO JobSkills (job_id, skill_id) VALUES (?, ?)',
                        (job_id, skill_id)
                    )

            for cert_name in cert_names:
                cert_id = cert_map.get(cert_name)
                if cert_id:
                    self.cursor.execute(
                        'INSERT OR IGNORE INTO JobCertificates (job_id, cert_id, is_required) VALUES (?, ?, 1)',
                        (job_id, cert_id)
                    )

        self.conn.commit()
        print(f"✅ Inserted {len(jobs)} job listings with skills, degrees & certificates into the database.")

    # ── User Authentication & Profile Methods ────────────────────────

    def create_user(self, username, email, password, full_name='', role='JobSeeker', skills='', certificates='', degree='Đại học (Bachelor)', experience_level='Junior'):
        """Register a new user in the database."""
        try:
            pwd_hash = hash_password(password)
            self.cursor.execute('''
                INSERT INTO Users (username, email, password_hash, full_name, role, skills, certificates, degree, experience_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username.strip(), email.strip().lower(), pwd_hash, full_name.strip(), role, skills.strip(), certificates.strip(), degree.strip(), experience_level.strip()))
            self.conn.commit()
            return self.get_user_by_id(self.cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            return {"error": "Tên đăng nhập hoặc email đã tồn tại trên hệ thống!"}
        except Exception as e:
            return {"error": str(e)}

    def authenticate_user(self, username_or_email, password):
        """Authenticate user credentials and return user record if valid."""
        self.cursor.execute('''
            SELECT * FROM Users
            WHERE username = ? OR email = ?
        ''', (username_or_email.strip(), username_or_email.strip().lower()))
        row = self.cursor.fetchone()
        if not row:
            return None

        user_dict = dict(row)
        if verify_password(password, user_dict['password_hash']):
            user_dict.pop('password_hash', None)
            return user_dict
        return None

    def get_user_by_id(self, user_id):
        """Get user details by ID (excluding password hash)."""
        self.cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
        row = self.cursor.fetchone()
        if row:
            d = dict(row)
            d.pop('password_hash', None)
            return d
        return None

    def get_user_by_username(self, username):
        """Get user details by username."""
        self.cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
        row = self.cursor.fetchone()
        if row:
            d = dict(row)
            d.pop('password_hash', None)
            return d
        return None

    def update_user_profile(self, user_id, full_name=None, skills=None, certificates=None, degree=None, experience_level=None):
        """Update profile settings for an existing user."""
        fields = []
        params = []
        if full_name is not None:
            fields.append("full_name = ?")
            params.append(full_name.strip())
        if skills is not None:
            fields.append("skills = ?")
            params.append(skills.strip())
        if certificates is not None:
            fields.append("certificates = ?")
            params.append(certificates.strip())
        if degree is not None:
            fields.append("degree = ?")
            params.append(degree.strip())
        if experience_level is not None:
            fields.append("experience_level = ?")
            params.append(experience_level.strip())

        if not fields:
            return self.get_user_by_id(user_id)

        params.append(user_id)
        query = f"UPDATE Users SET {', '.join(fields)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.get_user_by_id(user_id)

    # ── Certificate Methods ──────────────────────────────────────────

    def get_all_certificates(self):
        """Get list of all certificates with metadata."""
        self.cursor.execute('SELECT * FROM Certificates ORDER BY category, name')
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_certificate_names(self):
        """Get unique certificate names."""
        self.cursor.execute('SELECT name FROM Certificates ORDER BY name')
        return [row[0] for row in self.cursor.fetchall()]

    def get_certificates_by_category(self):
        """Group certificates by category."""
        self.cursor.execute('SELECT * FROM Certificates ORDER BY category, name')
        rows = self.cursor.fetchall()
        result = {}
        for row in rows:
            cat = row['category'] or 'Khác'
            if cat not in result:
                result[cat] = []
            result[cat].append(dict(row))
        return result

    # ── Query Methods for Analytics & Jobs ───────────────────────────

    def get_all_jobs(self, limit=100, offset=0, search=None):
        """Get all jobs with company names, skills, and certificates."""
        query = '''
            SELECT j.id, j.title, c.name as company, c.industry, j.location,
                   j.salary_min, j.salary_max, j.salary_currency, j.experience_level,
                   j.job_type, j.degree_required, j.source, j.date_scraped,
                   (SELECT GROUP_CONCAT(s.name, ', ') FROM JobSkills js JOIN Skills s ON js.skill_id = s.id WHERE js.job_id = j.id) as skills,
                   (SELECT GROUP_CONCAT(cert.name, ', ') FROM JobCertificates jc JOIN Certificates cert ON jc.cert_id = cert.id WHERE jc.job_id = j.id) as certificates
            FROM Jobs j
            LEFT JOIN Companies c ON j.company_id = c.id
        '''
        params = []
        if search:
            query += " WHERE j.title LIKE ? OR c.name LIKE ? OR j.description LIKE ?"
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])

        query += " ORDER BY j.id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_job_by_id(self, job_id):
        """Get details for a single job by ID including skills and certificates."""
        self.cursor.execute('''
            SELECT j.*, c.name as company, c.industry,
                   (SELECT GROUP_CONCAT(s.name, ', ') FROM JobSkills js JOIN Skills s ON js.skill_id = s.id WHERE js.job_id = j.id) as skills,
                   (SELECT GROUP_CONCAT(cert.name, ', ') FROM JobCertificates jc JOIN Certificates cert ON jc.cert_id = cert.id WHERE jc.job_id = j.id) as certificates
            FROM Jobs j
            LEFT JOIN Companies c ON j.company_id = c.id
            WHERE j.id = ?
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

    def get_certificate_frequency(self, limit=20):
        """Get top certificates demanded by employers."""
        self.cursor.execute('''
            SELECT cert.name, cert.category, cert.issuer, COUNT(jc.job_id) as frequency
            FROM Certificates cert
            JOIN JobCertificates jc ON cert.id = jc.cert_id
            GROUP BY cert.id
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
        """Get all skills per job as comma-separated strings."""
        self.cursor.execute('''
            SELECT GROUP_CONCAT(s.name, ', ') as skills
            FROM Jobs j
            JOIN JobSkills js ON j.id = js.job_id
            JOIN Skills s ON js.skill_id = s.id
            GROUP BY j.id
        ''')
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_jobs_with_meta(self):
        """Get all jobs with full skills, certificates, degree requirements for recommendation engine."""
        self.cursor.execute('''
            SELECT j.id, j.title, c.name as company, c.industry, j.location,
                   j.salary_min, j.salary_max, j.experience_level, j.job_type,
                   j.degree_required, j.source,
                   (SELECT GROUP_CONCAT(s.name, ', ') FROM JobSkills js JOIN Skills s ON js.skill_id = s.id WHERE js.job_id = j.id) as skills,
                   (SELECT GROUP_CONCAT(cert.name, ', ') FROM JobCertificates jc JOIN Certificates cert ON jc.cert_id = cert.id WHERE jc.job_id = j.id) as certificates
            FROM Jobs j
            LEFT JOIN Companies c ON j.company_id = c.id
        ''')
        return [dict(row) for row in self.cursor.fetchall()]

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