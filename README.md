# IT Job Market Intelligence System

![Dashboard](https://via.placeholder.com/800x400.png?text=IT+Job+Market+Intelligence+System)

The **IT Job Market Intelligence System** is an end-to-end data pipeline and web application designed to collect, process, analyze, and present job market data in Vietnam (specifically targeting ITviec and TopCV). It provides a premium web dashboard for exploring job trends, viewing analytics, and receiving career recommendations based on user skills.

## Features

- **Web Scraping:** 
  - Static scraping from [ITviec](https://itviec.com) using BeautifulSoup.
  - Dynamic scraping from [TopCV](https://topcv.vn) using Selenium.
- **Data Processing:** Cleaning, normalizing, and structuring scraped job data using `pandas`.
- **Database:** Local SQLite database for storing job listings, company data, and skill frequencies.
- **Market Analytics:** Generates insights such as average salaries, total jobs, company counts, and skill frequency, visualized with `matplotlib`.
- **Career Recommendation:** Analyzes a user's skills and suggests matching jobs, missing skills, and match rates.
- **Flask Dashboard:** A web interface serving analytics charts, search functionalities, and an interactive skills analyzer.

## Architecture

The system consists of several core modules:
- `scraper/`: Contains static and dynamic web scrapers.
- `analysis/`: Handles data processing (`data_processor.py`), recommendation engine (`recommendation.py`), and analytics (`analytics.py`).
- `database/`: Manages SQLite connections and queries (`db_manager.py`).
- `app.py`: The Flask web application.
- `main.py`: A CLI orchestrator that runs the full pipeline (Scraper → Processor → Database → Analysis → Recommendation).

## Prerequisites

- Python 3.8+
- Chrome/ChromeDriver (required for Selenium dynamic scraping)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd IT_Job_Market_System
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Required packages: `flask`, `beautifulsoup4`, `selenium`, `pandas`, `matplotlib`, `requests`.*

## Usage

### 1. Running the Full Pipeline (CLI)

To orchestrate the full system pipeline from scraping to data generation, run:
```bash
python main.py
```
This will:
1. Initialize the SQLite database.
2. Run both static and dynamic scrapers.
3. Process and clean the scraped data.
4. Insert data into the database.
5. Generate market analytics and charts.
6. Run a demo career recommendation.

### 2. Running the Web Dashboard

To start the Flask web application, run:
```bash
python app.py
```
The dashboard will be available at: [http://localhost:5000](http://localhost:5000)

## API Endpoints

The Flask application exposes the following main API routes:
- `GET /api/stats` - Retrieve dashboard statistics.
- `GET /api/jobs` - Get job listings (supports pagination and searching).
- `POST /api/analyze` - Analyze user skills for career recommendations.
- `GET /api/analytics` - Retrieve full market analytics report.
- `POST /api/scrape` - Trigger a new scraping run (supports specifying `source`: 'itviec' or 'topcv').
- `GET /api/skills` - Get available skills for autocomplete.

## License

This project is part of Project TEC004/03 - Group 3.