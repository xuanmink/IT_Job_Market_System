"""
IT Job Market Intelligence System - Flask Web Application
Provides API routes and serves the premium web dashboard.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DBManager
from analysis.recommendation import CareerRecommender
from analysis.analytics import MarketAnalytics
from analysis.data_processor import DataProcessor
from scraper.static_scraper import ITViecScraper
from scraper.dynamic_scraper import DynamicScraper

app = Flask(__name__, static_folder='static')

# ── Initialize Database on startup ────────────────────────────────
db = DBManager('database/data.db')
db.setup_tables()

# Check if DB has data, if not insert mock data
if db.get_job_count() == 0:
    db.insert_mock_data()
    print("✅ Database initialized with mock data.")

recommender = CareerRecommender(db)
analytics = MarketAnalytics(db)

# Generate charts on startup
try:
    analytics.generate_all_charts()
except Exception as e:
    print(f"Chart generation skipped: {e}")


# ── Page Routes ───────────────────────────────────────────────────

@app.route('/')
def home():
    """Serve the main dashboard page."""
    return render_template('index.html')


# ── API Routes ────────────────────────────────────────────────────

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics."""
    try:
        skill_freq = db.get_skill_frequency(1)
        top_skill = skill_freq[0]['name'] if skill_freq else 'N/A'
        return jsonify({
            "total_jobs": db.get_job_count(),
            "total_companies": db.get_company_count(),
            "avg_salary": db.get_avg_salary(),
            "top_skill": top_skill,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get job listings with optional search."""
    search = request.args.get('search', None)
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    try:
        jobs = db.get_all_jobs(limit=limit, offset=offset, search=search)
        total = db.get_job_count()
        return jsonify({"jobs": jobs, "total": total})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_skills():
    """Analyze user skills and return career recommendations."""
    data = request.get_json()
    user_skills = data.get('skills', '')

    if not user_skills.strip():
        return jsonify({"error": "Please enter at least one skill!"}), 400

    try:
        result = recommender.recommend(user_skills)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Keep legacy endpoint for backward compatibility
@app.route('/analyze', methods=['POST'])
def analyze_skills_legacy():
    """Legacy analyze endpoint."""
    return analyze_skills()


@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get full analytics report."""
    try:
        report = analytics.get_full_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get all available skills for autocomplete."""
    try:
        skills = db.get_all_skill_names()
        return jsonify({"skills": skills})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    """Trigger a new scraping run."""
    try:
        source = request.json.get('source', 'itviec') if request.json else 'itviec'
        log = []

        if source == 'itviec':
            scraper = ITViecScraper("https://itviec.com")
            jobs = scraper.run_scraper(max_pages=3)
            log = scraper.get_log()
        elif source == 'topcv':
            scraper = DynamicScraper("https://topcv.vn")
            jobs = scraper.run_scraper(max_pages=3)
            log = scraper.get_log()
        else:
            # Run both
            s1 = ITViecScraper("https://itviec.com")
            jobs1 = s1.run_scraper(max_pages=3)
            s2 = DynamicScraper("https://topcv.vn")
            jobs2 = s2.run_scraper(max_pages=3)
            jobs = jobs1 + jobs2
            log = s1.get_log() + s2.get_log()

        # Process and insert into DB
        if jobs:
            processor = DataProcessor()
            processor.load_from_list(jobs)
            processor.clean_data()
            processor.insert_into_db(db)
            log.extend(processor.processing_log)

            # Regenerate charts
            try:
                analytics.generate_all_charts()
            except Exception:
                pass

        return jsonify({
            "success": True,
            "jobs_scraped": len(jobs) if jobs else 0,
            "log": log
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/charts/<filename>')
def serve_chart(filename):
    """Serve generated chart images."""
    return send_from_directory('static/charts', filename)


# ── Error Handlers ────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  IT Job Market Intelligence System")
    print("  Dashboard: http://localhost:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)