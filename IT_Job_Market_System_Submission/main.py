"""
IT Job Market Intelligence System - Main Integration Script (Member 1 - SP3)
Orchestrates the full pipeline: Scraper → Processor → Database → Analysis → Recommendation
"""

import time
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.static_scraper import ITViecScraper
from scraper.dynamic_scraper import DynamicScraper
from database.db_manager import DBManager
from analysis.data_processor import DataProcessor
from analysis.recommendation import CareerRecommender
from analysis.analytics import MarketAnalytics


def main():
    """Main system workflow: integrates all components."""
    print("=" * 65)
    print("   IT JOB MARKET INTELLIGENCE SYSTEM")
    print("   Project TEC004/03 - Group 3")
    print("=" * 65)

    # ── Step 1: Initialize Database ──────────────────────────────
    print("\n📦 [1/5] Initializing Database...")
    db = DBManager('database/data.db')
    db.setup_tables()
    db.insert_mock_data()
    print(f"   Total jobs in DB: {db.get_job_count()}")
    print(f"   Total companies: {db.get_company_count()}")

    # ── Step 2: Run Scrapers ─────────────────────────────────────
    print("\n🕷️  [2/5] Running Web Scrapers...")

    # Static Scraper (ITviec - BeautifulSoup)
    print("\n   --- Static Scraper (ITviec) ---")
    static_scraper = ITViecScraper("https://itviec.com")
    static_jobs = static_scraper.run_scraper(max_pages=3)
    if static_jobs:
        static_scraper.save_to_csv('scraper/raw_itviec.csv')

    # Dynamic Scraper (TopCV - Selenium)
    print("\n   --- Dynamic Scraper (TopCV) ---")
    dynamic_scraper = DynamicScraper("https://topcv.vn")
    dynamic_jobs = dynamic_scraper.run_scraper(max_pages=3)
    if dynamic_jobs:
        dynamic_scraper.save_to_csv('scraper/raw_topcv.csv')

    # ── Step 3: Process & Clean Data ─────────────────────────────
    print("\n🔧 [3/5] Processing & Cleaning Scraped Data...")
    processor = DataProcessor()

    all_scraped = static_jobs + dynamic_jobs
    if all_scraped:
        processor.load_from_list(all_scraped)
        cleaned = processor.clean_data()
        if cleaned is not None:
            summary = processor.get_summary()
            print(f"   Processed: {summary['total_records']} records")
            print(f"   Unique companies: {summary['unique_companies']}")
            # Insert cleaned data into DB
            processor.insert_into_db(db)

    # ── Step 4: Generate Analytics ───────────────────────────────
    print("\n📊 [4/5] Generating Market Analytics...")
    analytics = MarketAnalytics(db)
    report = analytics.get_full_report()
    print(f"   Total jobs analyzed: {report['total_jobs']}")
    print(f"   Average salary: {report['avg_salary']:,} VND")

    # Generate Matplotlib charts
    print("\n   Generating charts...")
    charts = analytics.generate_all_charts()
    print(f"   Charts generated: {len(charts)}")

    # ── Step 5: Demo Recommendation ──────────────────────────────
    print("\n🎯 [5/5] Running Career Recommendation Demo...")
    recommender = CareerRecommender(db)

    demo_skills = "Python, C++, Verilog"
    print(f"\n   Demo input skills: {demo_skills}")
    result = recommender.recommend(demo_skills)
    print(f"   Match Rate: {result['match_rate']}")
    print(f"   Top Missing Skill: {result['missing_skill']}")
    print(f"   Matched Skills: {', '.join(result['matched_skills'])}")
    print(f"   Summary: {result['recommendation_summary']}")

    # ── Complete ─────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("   ✅ SYSTEM EXECUTION COMPLETED SUCCESSFULLY!")
    print("=" * 65)
    print("\n   To start the web dashboard, run:")
    print("   python app.py")
    print(f"   Then open: http://localhost:5000")

    db.close()


if __name__ == "__main__":
    main()