"""
IT Job Market Intelligence System - Flask Web Application
Provides API routes, user authentication, and serves the premium web dashboard.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory, session

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from database.db_manager import DBManager
from analysis.recommendation import CareerRecommender
from analysis.analytics import MarketAnalytics
from analysis.data_processor import DataProcessor
from scraper.static_scraper import ITViecScraper
from scraper.dynamic_scraper import DynamicScraper

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'it_job_market_intelligence_system_secret_key_2026')

# ── Initialize Database on startup ────────────────────────────────
db = DBManager('database/data.db')
db.setup_tables()

# Check if DB has data, if not insert mock data
if db.get_job_count() == 0:
    db.insert_mock_data()
    print("✅ Database initialized with mock data, certificates, and demo accounts.")

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


# ── Authentication & User Profile Routes ──────────────────────────

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    full_name = data.get('full_name', '').strip()
    skills = data.get('skills', '').strip()
    certificates = data.get('certificates', '').strip()
    degree = data.get('degree', 'Đại học (Bachelor)').strip()
    experience_level = data.get('experience_level', 'Junior').strip()

    if not username or len(username) < 3:
        return jsonify({"error": "Tên đăng nhập phải có ít nhất 3 ký tự!"}), 400
    if not email or '@' not in email:
        return jsonify({"error": "Email không hợp lệ!"}), 400
    if not password or len(password) < 6:
        return jsonify({"error": "Mật khẩu phải có ít nhất 6 ký tự!"}), 400

    result = db.create_user(
        username=username,
        email=email,
        password=password,
        full_name=full_name or username,
        skills=skills,
        certificates=certificates,
        degree=degree,
        experience_level=experience_level
    )

    if not result or 'error' in result:
        err_msg = result.get('error', 'Đăng ký thất bại!') if isinstance(result, dict) else 'Đăng ký thất bại!'
        return jsonify({"error": err_msg}), 400

    session['user_id'] = result['id']
    return jsonify({"success": True, "user": result, "message": "Đăng ký tài khoản thành công!"})


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate and log in user."""
    data = request.get_json() or {}
    username_or_email = data.get('username_or_email', '').strip()
    password = data.get('password', '')

    if not username_or_email or not password:
        return jsonify({"error": "Vui lòng nhập đầy đủ tên đăng nhập/email và mật khẩu!"}), 400

    user = db.authenticate_user(username_or_email, password)
    if not user:
        return jsonify({"error": "Tên đăng nhập hoặc mật khẩu không chính xác!"}), 401

    session['user_id'] = user['id']
    return jsonify({"success": True, "user": user, "message": "Đăng nhập thành công!"})


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log out current user."""
    session.pop('user_id', None)
    return jsonify({"success": True, "message": "Đã đăng xuất thành công!"})


@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    """Get currently logged-in user profile."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"logged_in": False, "user": None})

    user = db.get_user_by_id(user_id)
    if not user:
        session.pop('user_id', None)
        return jsonify({"logged_in": False, "user": None})

    return jsonify({"logged_in": True, "user": user})


@app.route('/api/auth/profile', methods=['POST'])
def update_profile():
    """Update profile and saved preferences for current user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Bạn cần đăng nhập để thực hiện chức năng này!"}), 401

    data = request.get_json() or {}
    user = db.update_user_profile(
        user_id=user_id,
        full_name=data.get('full_name'),
        skills=data.get('skills'),
        certificates=data.get('certificates'),
        degree=data.get('degree'),
        experience_level=data.get('experience_level')
    )
    return jsonify({"success": True, "user": user, "message": "Cập nhật hồ sơ thành công!"})


# ── Metadata API ──────────────────────────────────────────────────

@app.route('/api/metadata', methods=['GET'])
def get_metadata():
    """Get metadata for autocomplete and quick-select badges."""
    try:
        skills = db.get_all_skill_names()
        certificates = db.get_all_certificates()
        certs_by_cat = db.get_certificates_by_category()
        degrees = [
            "Đại học (Bachelor)",
            "Kỹ sư (Engineer)",
            "Thạc sĩ (Master)",
            "Tiến sĩ (PhD)",
            "Cao đẳng (Associate)",
            "Tự học / Khác"
        ]
        experience_levels = ["Intern", "Fresher", "Junior", "Mid", "Senior", "Lead / Manager"]
        return jsonify({
            "skills": skills,
            "certificates": certificates,
            "certificates_by_category": certs_by_cat,
            "degrees": degrees,
            "experience_levels": experience_levels
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Dashboard & Job API Routes ────────────────────────────────────

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


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job_detail(job_id):
    """Get full details of a specific job."""
    try:
        job = db.get_job_by_id(job_id)
        if job:
            return jsonify(job)
        return jsonify({"error": "Job not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_skills():
    """Analyze user skills, certificates, degree and return career recommendations."""
    data = request.get_json() or {}
    user_skills = data.get('skills', '')
    user_certs = data.get('certificates', '')
    user_degree = data.get('degree', 'Đại học (Bachelor)')
    user_experience = data.get('experience_level', 'Junior')
    lang = data.get('lang', 'vi')

    if not user_skills.strip() and not user_certs.strip():
        err_msg = "Please enter at least one skill or certification to analyze!" if lang == "en" else "Vui lòng nhập ít nhất một kỹ năng hoặc chứng chỉ để phân tích!"
        return jsonify({"error": err_msg}), 400

    try:
        result = recommender.recommend(
            user_skills_string=user_skills,
            user_certificates_string=user_certs,
            user_degree=user_degree,
            user_experience=user_experience,
            lang=lang
        )
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