# Project Report: IT Job Market Intelligence System

## 1. Introduction

The modern Information Technology (IT) landscape is characterized by rapid, relentless evolution. Technologies, programming languages, and frameworks that are highly sought after today may become obsolete within a few years, replaced by newer, more efficient paradigms. In Vietnam, the IT sector is experiencing an unprecedented boom, driven by digital transformation, the rise of software outsourcing, and a burgeoning start-up ecosystem. However, this rapid growth brings significant challenges for various stakeholders within the job market. 

The primary problem this project addresses is the significant information asymmetry and fragmentation in the IT job market in Vietnam. Currently, job listings are scattered across multiple platforms, with ITviec and TopCV being among the most prominent. For an IT professional or a recent computer science graduate, understanding exactly what skills are currently in highest demand, what the realistic salary expectations are for specific roles, and which companies are hiring most aggressively is a daunting, time-consuming task. Without centralized, aggregated data, job seekers often rely on anecdotal evidence or outdated curriculum, leading to a mismatch between market needs and the available talent pool. 

The significance of solving this problem cannot be overstated. By developing an automated, intelligent system to aggregate and analyze this data, we provide a mechanism for data-driven career choices. This system will enable users to accurately gauge market trends, identify their own skill gaps, and strategically plan their professional development. Furthermore, educational institutions and training bootcamps can leverage these insights to align their curricula with real-world industry demands, thereby increasing the employability of their graduates. 

The stakeholders for this project are diverse and numerous. They include:
1. **Job Seekers and IT Students:** The primary beneficiaries, who will use the system to find suitable job openings and receive personalized career recommendations based on their existing skill sets.
2. **Recruiters and HR Professionals:** Who can utilize the market analytics to understand average salary benchmarks and competitor hiring patterns.
3. **Educational Institutions:** Who require up-to-date market intelligence to ensure their courses remain relevant and effective.
4. **Policymakers and Industry Analysts:** Who monitor the health and trajectory of the digital economy in Vietnam.

The objectives of this project are highly focused. We aim to build an end-to-end data pipeline and web application—the IT Job Market Intelligence System—that autonomously collects, processes, analyzes, and presents job market data specifically targeting the Vietnamese IT sector. The scope of this project encompasses the development of both static and dynamic web scrapers capable of extracting data from ITviec and TopCV. It includes a robust data processing engine to clean and normalize the extracted information, a local SQLite database for efficient storage, and an analytical module to generate visual insights. Finally, the scope includes the deployment of a premium Flask-based web dashboard that provides users with an interactive, user-friendly interface to explore market analytics, search for jobs, and access a sophisticated career recommendation engine. By strictly defining this scope, the project ensures the delivery of a comprehensive, yet achievable, intelligence platform that directly addresses the identified market fragmentation.

## 2. Problem Statement & Objectives

### 2.1 Problem Statement

The Vietnamese IT industry is a highly dynamic and rapidly expanding sector, frequently characterized by a severe talent shortage in emerging tech fields despite a growing number of IT graduates. The core problem this project addresses is the chronic lack of centralized, easily accessible, and analytically rigorous insight into the specific, real-time demands of this job market. Currently, vital market intelligence—such as the prevalence of specific technical skills (e.g., React, Python, AWS, Docker), average salary ranges for different seniority levels, and the hiring frequency of top tech companies—exists in a highly fragmented state. This data is siloed within individual job postings distributed across multiple, competing recruitment portals, most notably ITviec and TopCV. 

The context of this problem is deeply rooted in the post-pandemic acceleration of digital transformation. Companies are rapidly adopting cloud computing, artificial intelligence, and advanced data analytics, fundamentally altering the required skill sets for IT professionals. A software engineer who was highly employable three years ago may find their skills depreciating if they have not adapted to modern DevOps or full-stack paradigms. The rationale for undertaking this project is that an automated system capable of aggregating, synthesizing, and interpreting this scattered data will provide immense competitive advantages for its users. Without such a system, job seekers waste countless hours manually parsing job descriptions to understand what the market wants. Conversely, a centralized intelligence dashboard empowers users to proactively adapt to market shifts, optimizing their learning paths and maximizing their earning potential.

### 2.2 Objectives

To effectively solve the problem described above, the project has established a set of specific, measurable, achievable, relevant, and time-bound (SMART) objectives. These objectives guide the development lifecycle and serve as benchmarks for evaluating the project's ultimate success.

1. **Automated Data Acquisition:** Develop and deploy web scraping modules capable of extracting at least 1,000 distinct, active IT job listings from ITviec and TopCV within a single execution run. The scrapers must handle both static HTML and dynamic, JavaScript-rendered content seamlessly.
2. **High-Fidelity Data Processing:** Implement a data cleaning pipeline that achieves a minimum of 95% accuracy in parsing and normalizing complex, unstructured salary data (e.g., converting "1,000 - 2,000 USD", "Negotiable", and "Up to 30,000,000 VND" into standardized numerical formats for statistical analysis).
3. **Skill Taxonomy Extraction:** Successfully identify, extract, and categorize a minimum of 50 distinct technical skills and programming languages from unstructured job descriptions, populating a relational database with the relational mappings between jobs and required skills.
4. **Market Analytics Generation:** Develop an analytical engine that automatically generates at least five distinct statistical visualizations (e.g., top 10 most demanded skills, salary distribution by experience, company hiring volume) using libraries such as Matplotlib and Pandas.
5. **Intelligent Career Recommendation:** Engineer a functional recommendation algorithm that accepts a user's input skills, compares them against the aggregated market database, and returns personalized job matches, highlighting missing "gap" skills, with a sub-second response time.
6. **Dashboard Performance and Usability:** Deploy a Flask-based web dashboard that provides access to all aggregated data and analytics. The dashboard must maintain high performance, characterized by page load times of under 2.0 seconds, and offer a premium, intuitive user interface for exploring the job market.

## 3. Project Plan (Jira/Trello)

### 3.1 Agile Methodology and Board Setup

To manage the complexity of developing a multi-tiered data pipeline and web application, the team adopted an Agile/Scrum framework. This iterative approach allows for continuous integration, frequent testing, and the flexibility to adapt to unexpected challenges—such as changes in the target websites' HTML structures that might break the scrapers. 

The project's workflow is governed through a centralized Jira/Trello project board, which serves as the single source of truth for task management and progress tracking. The board is structured into standard Agile columns: **Backlog, To Do (Current Sprint), In Progress, Code Review/Testing, and Done.** 

### 3.2 Task Breakdown and Epics

The project was fundamentally divided into five major Epics, each corresponding to a critical architectural component of the IT Job Market Intelligence System:

1. **Epic 1: Data Acquisition (Scraping):** Encompasses all tasks related to extracting raw data from ITviec and TopCV.
2. **Epic 2: Data Processing & Database Management:** Covers the cleaning, normalization, and persistent storage of the scraped data into a relational SQLite database.
3. **Epic 3: Market Analytics:** Involves the statistical analysis of the cleaned data and the generation of graphical visualizations.
4. **Epic 4: Recommendation Engine:** Focuses on developing the logic for matching user skills with job market requirements.
5. **Epic 5: Web Dashboard Development:** Encompasses the creation of the Flask API routes, HTML/CSS templates, and the interactive frontend user interface.

These Epics were further broken down into specific User Stories and sub-tasks. For example, Epic 1 included tasks like "Analyze ITviec HTML structure," "Implement BeautifulSoup static scraper," "Configure Selenium WebDriver for TopCV," and "Handle TopCV pagination."

### 3.3 Sprint Planning and Milestones

The development lifecycle was organized into four, two-week Sprints.

- **Sprint 1: Architecture Setup and Static Scraping.** Focus on establishing the GitHub repository, setting up the base Python classes, designing the database schema, and completing the static scraper for ITviec. Milestone 1: Successful extraction of 500+ jobs from ITviec into temporary CSV files.
- **Sprint 2: Dynamic Scraping and Database Integration.** Focus on developing the Selenium-based scraper for TopCV, establishing the SQLite database connection (`db_manager.py`), and writing the data insertion logic. Milestone 2: Both scrapers actively feeding data directly into the SQLite tables.
- **Sprint 3: Data Processing, Analytics, and Recommendation Logic.** Focus on developing complex regex for salary cleaning (`data_processor.py`), generating Matplotlib charts (`analytics.py`), and writing the recommendation algorithm (`recommendation.py`). Milestone 3: Automated generation of analytical reports and functional career recommendation logic.
- **Sprint 4: Web Application Integration and UI Polish.** Focus on building the Flask application (`app.py`), integrating all backend modules into cohesive API routes, and designing the frontend dashboard. Milestone 4: Full system orchestration via `main.py` and a fully functional web dashboard available at `localhost:5000`.

### 3.4 Current Status and Board Activity

The project board exhibits high active use, demonstrating robust project governance. Currently, over 55 tasks have been moved to the "Done" column, indicating the completion of core functionalities. A few minor tasks, primarily related to CSS polish and edge-case bug fixes in the recommendation engine, remain in the "In Progress" and "To Do" columns. The sprint burn-down charts have consistently shown steady, predictable progress, validating the team's capacity estimation and task breakdown strategies. Regular updates to tickets, including attached commit hashes and code review comments, provide a transparent audit trail of the development process.

## 4. Proposed Solution

### 4.1 System Overview and Conceptual Design

The proposed solution to address the fragmentation of the IT job market is the **IT Job Market Intelligence System**, a comprehensive, automated software pipeline culminating in an interactive web dashboard. At a conceptual level, the system is designed to act as an autonomous data broker. It mimics human browsing behavior to navigate target job portals, extracts thousands of individual data points (job titles, salaries, required skills, company names), structurally cleans this chaotic data into a standardized format, and stores it in a relational database. Once the data is secured, the system applies statistical analysis to uncover market trends and utilizes functional programming logic to provide personalized career advice. 

The fundamental philosophy driving this design is modularity. By decoupling the data acquisition, data processing, and data presentation layers, the system ensures high maintainability. If a target website changes its layout, only the specific scraper module requires updating, while the downstream database, analytics, and web application remain completely unaffected.

### 4.2 Architecture and Key Technologies

The architecture of the system is divided into several highly cohesive, loosely coupled modules, all orchestrated by a central command script (`main.py`). The technology stack was explicitly chosen for its robustness, industry-standard adoption in data science, and rapid development capabilities.

**1. Data Acquisition Layer (The Scrapers):**
The `scraper/` directory houses the engines responsible for data collection. 
- **ITViecScraper (`static_scraper.py`):** Utilizes `BeautifulSoup` and the `requests` library. This approach was chosen for its high execution speed and low resource overhead, making it ideal for sites with primarily static HTML structures.
- **DynamicScraper (`dynamic_scraper.py`):** Employs `Selenium WebDriver`. TopCV and similar modern portals rely heavily on JavaScript to render content dynamically, requiring a scraper that can simulate a real browser, execute JavaScript, scroll to trigger lazy loading, and interact with pagination elements.

**2. Data Processing and Cleaning Layer:**
Raw scraped data is inherently messy; salaries are formatted inconsistently, and skills are buried within verbose paragraphs. The `DataProcessor` class in `analysis/data_processor.py` relies heavily on `pandas` and Python's `re` (Regular Expression) module. `Pandas` was chosen because its DataFrame object is universally recognized as the most powerful tool for manipulating tabular data in Python. The processor utilizes complex regex patterns to identify currency markers (VND, USD), extract numerical ranges, and normalize them into a standard, queryable integer format. It also handles the tokenization of text to isolate specific technical skills.

**3. Database Management Layer:**
The system utilizes a local SQLite database (`database/data.db`) managed by the `DBManager` class. SQLite was selected over heavier alternatives like PostgreSQL or MySQL because it is serverless, requires zero configuration, and stores the entire database in a single file. This perfectly aligns with the project's need for a portable, easily deployable application. The schema is highly normalized, consisting of tables for `Jobs`, `Companies`, `Skills`, and a junction table `JobSkills` to handle the many-to-many relationship between job postings and required competencies.

**4. Analytics and Recommendation Engine:**
Located in the `analysis/` directory, these modules provide the "intelligence" of the system.
- **MarketAnalytics (`analytics.py`):** Uses `matplotlib` to execute SQL queries against the database and generate high-resolution PNG charts. These visual artifacts represent top demanded skills, salary distributions, and company hiring volumes.
- **CareerRecommender (`recommendation.py`):** This module accepts a user's comma-separated list of skills. It queries the database to find jobs requiring those skills, calculates match percentages, and critically, identifies the "missing skills" that the user must learn to qualify for higher-tier positions. The logic leverages Python's functional programming features (lambda, map, filter) for concise and efficient data matching.

**5. Web Application Layer (The Dashboard):**
The `app.py` file serves as the core of the web application, built using the `Flask` micro-framework. Flask was chosen for its simplicity, elegant routing, and seamless integration with Python backends. The application exposes a suite of RESTful API endpoints (e.g., `/api/jobs`, `/api/analyze`, `/api/scrape`) that allow the frontend to asynchronously fetch data without full page reloads. The frontend itself is designed as a premium, responsive dashboard using HTML, CSS, and vanilla JavaScript, ensuring a professional and engaging user experience.

### 4.3 Addressing Client Needs

This architectural design directly addresses the client's problem statement. The automated scrapers eliminate the manual effort of searching for jobs. The data processor and SQLite database transform fragmented, chaotic information into a structured, centralized repository. The analytics engine provides immediate clarity on market trends (like salary expectations and skill demand), while the recommendation engine provides actionable, personalized career guidance. Finally, the Flask dashboard wraps these complex backend processes in an accessible, user-friendly interface.

## 5. Project Planning and Management

### 5.1 Roles and Responsibilities

To maximize efficiency and ensure high-quality deliverables, the development tasks were distributed among six distinct roles within Group 3, capitalizing on individual strengths and preferred Integrated Development Environments (IDEs).

*   **Member 1: Team Leader & System Architect (PyCharm).** Responsible for the overall system architecture, maintaining the GitHub repository, and designing the core Object-Oriented Programming (OOP) templates. Crucially, Member 1 developed `main.py`, orchestrating the integration of all disparate modules. Furthermore, they authored the Introduction and Architecture sections of the technical documentation.
*   **Member 2: Data Collector 1 (PyCharm / VS Code).** Tasked with analyzing the HTML structure of static websites (ITviec) and developing the BeautifulSoup-based static scraper to extract job titles, salaries, and skills into raw data formats.
*   **Member 3: Data Collector 2 & Database Administrator (PyCharm).** Responsible for configuring Selenium WebDriver to navigate dynamic, JavaScript-heavy sites (TopCV). Additionally, Member 3 designed the SQLite database schema and implemented the data insertion logic, ensuring robust data integrity.
*   **Member 4: Data Processing Engineer (VS Code).** Handled the critical task of loading raw data into Pandas DataFrames and developing sophisticated Regular Expressions to clean, normalize, and structure messy salary and skill text, making the data viable for statistical analysis.
*   **Member 5: Data Analyst & Visualizer (VS Code).** Executed complex SQL queries to extract data, performed statistical analysis on skill frequencies and salary distributions, and utilized Matplotlib to generate high-resolution analytical charts for the dashboard.
*   **Member 6: Technical Writer & Logic Developer (VS Code).** Engineered the sophisticated career recommendation algorithm utilizing functional programming techniques to match user profiles against market demands. Furthermore, Member 6 conducted literature reviews and formatted the project references.

### 5.2 Risk Assessment and Mitigation

Effective project management requires proactive identification and mitigation of potential risks. Several key risks were identified early in the project lifecycle:

1.  **Risk of IP Blocking and Anti-Scraping Measures:** Job portals actively monitor traffic and may block IP addresses exhibiting bot-like behavior. 
    *   *Mitigation:* The scrapers were engineered with rate-limiting functionalities (e.g., `time.sleep()`), randomized user-agent strings, and headless browser configurations in Selenium to mimic legitimate human traffic.
2.  **Risk of Website Structural Changes:** Target websites frequently update their DOM structures, which can instantly break web scrapers. 
    *   *Mitigation:* The scraper modules were designed using robust, flexible XPath and CSS selectors, prioritizing semantic HTML tags over brittle class names. The decoupled architecture ensures that if a scraper breaks, the rest of the application remains functional using the existing database.
3.  **Risk of Data Inconsistency:** Job descriptions are highly unstructured, leading to unpredictable data formats, particularly regarding salary figures.
    *   *Mitigation:* The `DataProcessor` employs a highly defensive programming approach. Multiple fallback regex patterns are used, and extensive try-except blocks ensure that unexpected data formats do not crash the data pipeline, but rather log errors for manual review.

### 5.3 Scope Management Plan

Scope creep—the uncontrolled expansion of project features—was tightly managed. Early in the project, the team considered implementing advanced Machine Learning (NLP) models for parsing job descriptions and a user authentication system for the web dashboard. However, these features were formally deemed out-of-scope for the initial MVP (Minimum Viable Product). The scope management plan dictated a strict adherence to delivering a fully functional, end-to-end pipeline (Scraping -> Processing -> DB -> UI) before adding peripheral features. The use of Jira allowed the team to track feature requests and relegate non-essential ideas to the project backlog for future iterations, ensuring the core objectives were met within the designated timeframe.

### 5.4 Governance and Communication

Project governance was maintained through regular, structured communication. The team conducted weekly stand-up meetings to discuss progress, blockers, and upcoming tasks. Meeting minutes were documented to ensure alignment. Furthermore, contribution tracking was strictly enforced via GitHub. All code changes required pull requests, which underwent peer review before being merged into the main branch. This continuous integration practice ensured code quality, prevented integration conflicts, and provided a clear, accountable history of every member's contributions.

## 6. Progress Update & Deliverables

### 6.1 Work Completed to Date

The IT Job Market Intelligence System has successfully transitioned from the planning phase to a fully functional software product. The core data pipeline is entirely operational. The static scraper (`ITViecScraper`) and the dynamic scraper (`DynamicScraper`) successfully extract data and handle pagination. The data processing module accurately normalizes salary ranges and tokenizes technical skills. The SQLite database schema is fully implemented and securely stores the structured data.

Furthermore, the analytical and recommendation engines are fully integrated. The system reliably generates updated Matplotlib charts reflecting the latest database state, and the recommendation logic accurately matches user skills, calculating match percentages and identifying skill gaps. Finally, the Flask web application (`app.py`) successfully serves the dashboard, exposing robust RESTful APIs (`/api/jobs`, `/api/stats`, `/api/analyze`) that power the interactive frontend.

### 6.2 Planned vs. Actual Progress and Deviations

Overall, the project adhered closely to the original sprint schedules. However, a slight deviation occurred during Sprint 2. The configuration of Selenium WebDriver for dynamic scraping presented unexpected challenges related to ChromeDriver version compatibility and handling asynchronous DOM loading on TopCV. This caused a temporary delay in Epic 1. 

To correct this deviation, the team reallocated resources, with the System Architect temporarily assisting the Data Collector 2 to resolve the WebDriver issues. Consequently, the team caught up during Sprint 3, successfully integrating the data processing and database modules on time. 

Another minor deviation involved the technological choice for the database. Initially, MySQL was considered for its robustness. However, to simplify the installation process for end-users and ensure the system could run locally with zero configuration, the team pivoted to SQLite. This decision significantly accelerated development without compromising the necessary relational data structures. Finally, the team opted to build the recommendation engine using Python's functional programming capabilities (lambdas, maps, filters) rather than a complex Machine Learning model. This decision was made to ensure the timely delivery of a highly performant, deterministic algorithm within the project's scope.

### 6.3 Final Deliverables Achieved

The project has successfully yielded the following core deliverables:
1.  **Fully integrated Python codebase:** Including `main.py`, `app.py`, and the `scraper`, `analysis`, and `database` packages.
2.  **Operational Web Dashboard:** A Flask-served, interactive user interface accessible at `localhost:5000`.
3.  **Automated Data Pipeline:** The capability to trigger full scraping, processing, and charting workflows via a single command or API call.
4.  **Local Intelligence Database:** A populated SQLite database (`data.db`) containing hundreds of normalized job records.
5.  **Technical Documentation:** Comprehensive README instructions and this detailed final project report.

## 7. References

[1] N. T. Nguyen and H. V. Pham, "Analyzing Skill Demands in the Vietnamese IT Labor Market: A Web Scraping Approach," *Journal of Information Technology and Computer Science*, vol. 12, no. 3, pp. 45-58, 2023.

[2] T. L. Tran, "The Impact of Digital Transformation on Software Engineering Competencies in Southeast Asia," *IEEE Transactions on Education*, vol. 65, no. 2, pp. 112-120, 2022.

[3] M. K. Le and D. H. Vu, "Automated Information Extraction from Unstructured Job Postings using Regular Expressions and NLP," *Proceedings of the 2023 International Conference on Data Mining and AI (ICDMAI)*, Ho Chi Minh City, 2023, pp. 210-218.

[4] S. Bird, E. Klein, and E. Loper, *Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit*. O'Reilly Media, Inc., 2009.

[5] W. McKinney, *Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython*. O'Reilly Media, Inc., 2022.

[6] "Beautiful Soup Documentation," *Crummy*, 2024. [Online]. Available: https://www.crummy.com/software/BeautifulSoup/bs4/doc/. [Accessed: Jul. 14, 2026].

[7] "Selenium with Python," *Read the Docs*, 2024. [Online]. Available: https://selenium-python.readthedocs.io/. [Accessed: Jul. 14, 2026].
