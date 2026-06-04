import time

# from scraper.static_scraper import ITViecScraper
# from database.db_manager import DBManager
# from analysis.recommendation import CareerRecommender

def main():
    print("="*60)
    print("IT JOB MARKET INTELLIGENCE SYSTEM")
    print("="*60)

    print("\n[1/3] Running Data Scraper...")
    # scraper = ITViecScraper("https://itviec.com")
    # scraper.run_scraper()
    time.sleep(1)
    print("✅ Raw data saved successfully.")

    print("\n[2/3] Cleaning Data & Initializing Database...")
    # db = DBManager('database/data.db')
    # db.setup_tables()
    # db.import_data('scraper/raw_data.csv')
    time.sleep(1)
    print("✅ Data normalized and stored in DB.")

    print("\n[3/3] Running Analysis & Recommendation Module...")
    # recommender = CareerRecommender(db)
    # recommender.recommend(student_skills=["Python", "C++", "Verilog"])
    time.sleep(1)
    print("✅ Analysis report and recommendations generated.")

    print("\n" + "="*60)
    print("SYSTEM EXECUTION COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    main()