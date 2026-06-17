class CareerRecommender:
    def __init__(self, db_manager):
        self.db = db_manager

    def recommend(self, user_skills_string):
        # 1. Xử lý kỹ năng đầu vào của người dùng
        user_skills = set([s.strip().upper() for s in user_skills_string.split(',') if s.strip()])

        # 2. Lấy dữ liệu thị trường từ Database
        market_jobs = self.db.get_all_skills_from_db()
        if not market_jobs:
            return "0%", "Không có dữ liệu"

        skill_frequency = {}

        # 3. Tính toán tần suất kỹ năng thị trường cần
        for job_skills in market_jobs:
            skills = [s.strip().upper() for s in job_skills.split(',')]
            for skill in skills:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1

        # 4. Tìm kỹ năng người dùng còn thiếu
        missing_skills = {}
        for skill, count in skill_frequency.items():
            if skill not in user_skills:
                missing_skills[skill] = count

        # 5. Sắp xếp để lấy kỹ năng thiếu quan trọng nhất
        sorted_missing = sorted(missing_skills.items(), key=lambda x: x[1], reverse=True)
        top_missing_skill = sorted_missing[0][0] if sorted_missing else "Không có"

        # 6. Tính toán tỷ lệ khớp (Công thức giả lập cho demo)
        match_rate_value = min(95, len(user_skills) * 25)
        match_rate = f"{match_rate_value}%"

        return match_rate, top_missing_skill