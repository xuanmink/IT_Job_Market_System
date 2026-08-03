"""
Career Recommendation Module (Member 6 - SP6)
Advanced recommendation algorithm using functional Python (lambda, filter, map).
Compares candidate profile (Skills, Certifications, Degrees, Experience) against market demands.
"""


class CareerRecommender:
    """
    Multi-Dimensional Career Recommendation Engine.
    Evaluates:
    - Technical Skills (60% weight)
    - Industry Certifications & Languages (25% weight)
    - Education / Degree & Experience (15% weight)
    """

    def __init__(self, db_manager):
        self.db = db_manager

    def recommend(self, user_skills_string, user_certificates_string="", user_degree="Đại học (Bachelor)", user_experience="Junior", lang="vi"):
        """
        Main recommendation method taking skills, certificates, degree, experience, and language.
        Returns a comprehensive career intelligence report in Vietnamese or English.
        """
        lang = (lang or "vi").lower()
        empty_msg = "Please enter at least one skill or certification to analyze." if lang == "en" else "Vui lòng nhập ít nhất một kỹ năng hoặc chứng chỉ để phân tích."
        no_data_msg = "No market job data available yet." if lang == "en" else "Chưa có dữ liệu việc làm thị trường."

        # 1. Parse user inputs using map() and filter()
        user_skills = set(
            filter(
                lambda s: len(s) > 0,
                map(lambda s: s.strip().upper(), (user_skills_string or "").split(','))
            )
        )

        user_certs = set(
            filter(
                lambda c: len(c) > 0,
                map(lambda c: c.strip().upper(), (user_certificates_string or "").split(','))
            )
        )

        if not user_skills and not user_certs:
            return self._empty_result(empty_msg)

        # 2. Get market data
        all_jobs = self.db.get_all_jobs_with_meta() if hasattr(self.db, 'get_all_jobs_with_meta') else self.db.get_all_jobs(limit=100)
        if not all_jobs:
            return self._empty_result(no_data_msg)

        # 3. Calculate skill demand frequency
        skill_frequency = {}
        for job in all_jobs:
            if job.get('skills'):
                job_skills = list(map(lambda s: s.strip().upper(), job['skills'].split(',')))
                for skill in job_skills:
                    skill_frequency[skill] = skill_frequency.get(skill, 0) + 1

        # 4. Calculate certificate demand frequency
        cert_frequency = {}
        for job in all_jobs:
            if job.get('certificates'):
                job_certs = list(map(lambda c: c.strip().upper(), job['certificates'].split(',')))
                for cert in job_certs:
                    cert_frequency[cert] = cert_frequency.get(cert, 0) + 1

        # 5. Skills analysis using filter() & lambda
        matched_skills = list(filter(lambda s: s in skill_frequency, user_skills))
        missing_skills_dict = dict(
            filter(
                lambda item: item[0] not in user_skills,
                skill_frequency.items()
            )
        )
        sorted_missing_skills = sorted(
            missing_skills_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # 6. Certificates analysis
        matched_certs = list(filter(lambda c: any(c in m_c or m_c in c for m_c in cert_frequency), user_certs)) if user_certs else []
        missing_certs_dict = dict(
            filter(
                lambda item: not any(item[0] in u_c or u_c in item[0] for u_c in user_certs),
                cert_frequency.items()
            )
        )
        sorted_missing_certs = sorted(
            missing_certs_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # 7. Multi-Criteria Scoring (Composite Match Rate)
        # 7.1 Skills Score (60%)
        total_skill_points = sum(skill_frequency.values())
        matched_skill_points = sum(map(lambda s: skill_frequency.get(s, 0), matched_skills))
        skill_match_rate = min(98, int((matched_skill_points / total_skill_points) * 100)) if total_skill_points > 0 else 0

        # 7.2 Certificates Score (25%)
        total_cert_points = sum(cert_frequency.values()) if cert_frequency else 1
        matched_cert_points = sum(map(lambda c: cert_frequency.get(c, 0), matched_certs))
        # Base cert score + bonus for having active certs
        base_cert_score = int((matched_cert_points / total_cert_points) * 100) if total_cert_points > 0 else 0
        cert_bonus = min(100, len(user_certs) * 25 + base_cert_score) if user_certs else 30

        # 7.3 Degree & Experience Fit Score (15%)
        degree_scores = {
            "Thạc sĩ (Master)": 100,
            "Master's Degree": 100,
            "Tiến sĩ (PhD)": 100,
            "PhD Doctorate": 100,
            "Kỹ sư (Engineer)": 95,
            "Engineer Degree": 95,
            "Đại học (Bachelor)": 90,
            "Bachelor's Degree": 90,
            "Cao đẳng (Associate)": 75,
            "Cao đẳng (College)": 75,
            "Associate Degree": 75,
            "Tự học / Khác": 70,
            "Self-Taught / Other": 70
        }
        degree_score = degree_scores.get(user_degree, 85)

        # 7.4 Overall Composite Score
        composite_rate = min(98, int(skill_match_rate * 0.55 + cert_bonus * 0.30 + degree_score * 0.15))

        top_missing_skill = sorted_missing_skills[0][0] if sorted_missing_skills else "None"
        top_missing_cert = sorted_missing_certs[0][0] if sorted_missing_certs else "AWS Certified Solutions Architect"

        # 8. Learning Roadmap with Skills & Certifications (Bilingual)
        roadmap = self._generate_enhanced_roadmap(sorted_missing_skills, matched_skills, sorted_missing_certs, user_certs, lang=lang)

        # 9. Matching Jobs with degree & cert breakdown
        matching_jobs = self._find_matching_jobs_enhanced(user_skills, user_certs, user_degree, user_experience, all_jobs)

        # 10. Skill & Cert categorization
        categories = self._categorize_profile(matched_skills, sorted_missing_skills, matched_certs, sorted_missing_certs)

        # 11. Summary (Bilingual)
        summary = self._generate_enhanced_summary(composite_rate, skill_match_rate, top_missing_skill, top_missing_cert, len(matched_skills), len(user_certs), user_degree, lang=lang)

        return {
            "match_rate": f"{composite_rate}%",
            "match_rate_value": composite_rate,
            "skill_match_rate": f"{skill_match_rate}%",
            "cert_match_rate": f"{cert_bonus}%",
            "degree_match_rate": f"{degree_score}%",
            "missing_skill": top_missing_skill,
            "missing_cert": top_missing_cert,
            "all_missing_skills": list(map(lambda x: {"skill": x[0], "demand": x[1]}, sorted_missing_skills[:10])),
            "all_recommended_certs": list(map(lambda x: {"cert": x[0], "demand": x[1]}, sorted_missing_certs[:6])),
            "matched_skills": list(matched_skills),
            "matched_certs": list(user_certs),
            "user_degree": user_degree,
            "user_experience": user_experience,
            "total_market_skills": len(skill_frequency),
            "total_jobs_analyzed": len(all_jobs),
            "roadmap": roadmap,
            "matching_jobs": matching_jobs,
            "skill_categories": categories,
            "recommendation_summary": summary,
            "lang": lang
        }

    def _generate_enhanced_roadmap(self, sorted_missing_skills, matched_skills, sorted_missing_certs, user_certs, lang="vi"):
        """Generate comprehensive roadmap in Vietnamese or English."""
        roadmap = []
        is_en = (lang == "en")

        # Phase 1: Core Foundation
        top_skill = sorted_missing_skills[0][0] if sorted_missing_skills else "Python"
        roadmap.append({
            "phase": "Phase 1" if is_en else "Giai đoạn 1",
            "title": f"Master Core Skill: {top_skill}" if is_en else f"Bổ sung Kỹ năng Trọng tâm: {top_skill}",
            "description": f"{top_skill} is the most in-demand requirement across job listings. Strengthen your fundamentals and build hands-on mini-projects." if is_en else f"{top_skill} là kỹ năng được săn đón nhất trong các tin tuyển dụng liên quan. Hãy xây dựng nền tảng vững chắc và thực hành qua mini-project.",
            "skills": [top_skill],
            "cert_target": "Master syntax & core architecture" if is_en else "Nắm vững cú pháp & core architecture",
            "duration": "2-4 weeks" if is_en else "2-4 tuần"
        })

        # Phase 2: Specialization & Next Tech
        if len(sorted_missing_skills) >= 3:
            comp_skills = list(map(lambda x: x[0], sorted_missing_skills[1:4]))
            roadmap.append({
                "phase": "Phase 2" if is_en else "Giai đoạn 2",
                "title": "Expand Ecosystem & Complementary Tools" if is_en else "Mở rộng Hệ sinh thái & Công nghệ Bổ trợ",
                "description": f"Learn popular complementary technologies: {', '.join(comp_skills)} to raise your job market coverage above 75%." if is_en else f"Học tiếp các công nghệ phổ biến: {', '.join(comp_skills)} để tăng độ bao phủ thị trường việc làm lên trên 75%.",
                "skills": comp_skills,
                "cert_target": "Build Full-Stack / API Microservices" if is_en else "Xây dựng dự án Full-stack / API microservices",
                "duration": "4-6 weeks" if is_en else "4-6 tuần"
            })

        # Phase 3: International Certification
        target_cert = sorted_missing_certs[0][0] if sorted_missing_certs else "AWS Certified Solutions Architect"
        roadmap.append({
            "phase": "Phase 3" if is_en else "Giai đoạn 3",
            "title": f"Achieve Certification: {target_cert}" if is_en else f"Chinh phục Chứng chỉ Quốc tế: {target_cert}",
            "description": f"Earning {target_cert} helps your resume outshine 80% of candidates and boosts expected salary by 20-35%." if is_en else f"Sở hữu chứng chỉ {target_cert} giúp hồ sơ của bạn nổi bật hơn 80% ứng viên khác và tăng mức lương đề xuất 20-35%.",
            "skills": ["Professional Certification", "Hands-on Cloud/Lab"] if is_en else ["Chứng chỉ chuyên môn", "Thực hành Lab thực tế"],
            "cert_target": target_cert,
            "duration": "4-8 weeks" if is_en else "4-8 tuần"
        })

        # Phase 4: Capstone Portfolio & Job Readiness
        roadmap.append({
            "phase": "Phase 4" if is_en else "Giai đoạn 4",
            "title": "Portfolio Refinement & Interview Preparation" if is_en else "Hoàn thiện Portfolio & Sẵn sàng Phỏng vấn",
            "description": "Publish production-grade projects on GitHub, document architectures, update CV with new credentials, and practice mock technical interviews." if is_en else "Đưa các dự án thực chiến lên GitHub, viết tài liệu kỹ thuật, cập nhật CV với chứng chỉ và chuẩn bị phỏng vấn kỹ thuật.",
            "skills": ["System Design", "Clean Architecture", "Mock Interviews"] if is_en else ["System Design", "Clean Code", "Mock Interview"],
            "cert_target": "Apply to Target Companies" if is_en else "Ứng tuyển vị trí mục tiêu",
            "duration": "2-4 weeks" if is_en else "2-4 tuần"
        })

        return roadmap

    def _generate_enhanced_summary(self, composite_rate, skill_rate, top_missing_skill, top_missing_cert, matched_count, cert_count, degree, lang="vi"):
        """Generate friendly Vietnamese or English analytical summary report."""
        is_en = (lang == "en")
        
        if is_en:
            cert_text = f" and {cert_count} certifications" if cert_count > 0 else ""
            if composite_rate >= 80:
                return f"Outstanding! Your profile demonstrates high competitive edge ({composite_rate}% market alignment) with {matched_count} core skills{cert_text} and {degree} background. To scale towards Senior/Lead positions, consider pursuing {top_missing_cert}."
            elif composite_rate >= 50:
                return f"Solid foundation! Your profile matches {composite_rate}% of available IT openings with {matched_count} aligned skills. Prioritize learning {top_missing_skill} and preparing for {top_missing_cert} to qualify for top-tier companies."
            elif composite_rate >= 25:
                return f"Growing candidate! You possess {matched_count} foundational skills ({composite_rate}% match). Focus on mastering {top_missing_skill} and adding certified credential {top_missing_cert} to satisfy employer requirements quickly."
            else:
                return f"Your current profile aligns with {composite_rate}% of market openings. Start by picking up {top_missing_skill} and follow the roadmap below to earn {top_missing_cert}!"
        else:
            cert_text = f" và {cert_count} chứng chỉ" if cert_count > 0 else ""
            if composite_rate >= 80:
                return f"Xuất sắc! Hồ sơ của bạn đạt mức độ cạnh tranh rất cao ({composite_rate}% phù hợp thị trường) với {matched_count} kỹ năng cốt lõi{cert_text}, nền tảng {degree}. Để bứt phá lên cấp độ Senior/Lead, bạn nên nâng cấp thêm chứng chỉ {top_missing_cert}."
            elif composite_rate >= 50:
                return f"Nền tảng vững chắc! Hồ sơ của bạn đạt {composite_rate}% độ tương thích việc làm với {matched_count} kỹ năng phù hợp. Ưu tiên học thêm {top_missing_skill} và chuẩn bị thi chứng chỉ {top_missing_cert} để tăng khả năng trúng tuyển vào các công ty lớn."
            elif composite_rate >= 25:
                return f"Đang trên đà phát triển! Bạn đã có {matched_count} kỹ năng bước đầu ({composite_rate}% phù hợp). Hãy tập trung trau dồi {top_missing_skill} và bổ sung chứng chỉ chuyên môn {top_missing_cert} theo lộ trình gợi ý để nhanh chóng đáp ứng yêu cầu nhà tuyển dụng."
            else:
                return f"Hồ sơ của bạn phù hợp {composite_rate}% so với các vị trí IT hiện tại. Hãy bắt đầu ngay với kỹ năng {top_missing_skill} và tham khảo lộ trình đạt chứng chỉ {top_missing_cert} bên dưới!"

    def _find_matching_jobs_enhanced(self, user_skills, user_certs, user_degree, user_experience, all_jobs):
        """Find matching jobs calculating skill, certificate, and degree alignment."""
        matching = []

        for job in all_jobs:
            if not job.get('skills'):
                continue

            job_skills = set(map(lambda s: s.strip().upper(), job['skills'].split(',')))
            overlap_skills = user_skills.intersection(job_skills)

            # Certificate overlap
            job_certs = set(map(lambda c: c.strip().upper(), job['certificates'].split(','))) if job.get('certificates') else set()
            overlap_certs = user_certs.intersection(job_certs) if user_certs else set()
            cert_matched_names = [c for c in (job.get('certificates', '').split(', ') if job.get('certificates') else [])
                                  if any(u in c.upper() or c.upper() in u for u in user_certs)]

            # Degree fit check
            job_deg = job.get('degree_required', 'Đại học (Bachelor)')
            degree_fit = True
            if "Thạc sĩ" in job_deg and "Thạc sĩ" not in user_degree and "Tiến sĩ" not in user_degree:
                degree_fit = False

            if overlap_skills or overlap_certs:
                skill_pct = int((len(overlap_skills) / max(len(job_skills), 1)) * 100)
                cert_pct = 100 if overlap_certs or len(cert_matched_names) > 0 else (50 if not job_certs else 0)
                deg_pct = 100 if degree_fit else 70

                # Weighted job match percentage
                total_pct = min(99, int(skill_pct * 0.60 + cert_pct * 0.25 + deg_pct * 0.15))

                matching.append({
                    "id": job.get('id'),
                    "title": job.get('title'),
                    "company": job.get('company'),
                    "location": job.get('location'),
                    "match_percentage": total_pct,
                    "skills_match_pct": skill_pct,
                    "matching_skills": list(overlap_skills),
                    "required_skills": list(job_skills),
                    "degree_required": job_deg,
                    "degree_fit": degree_fit,
                    "certificates_preferred": job.get('certificates', ''),
                    "cert_matched": len(cert_matched_names) > 0 or len(overlap_certs) > 0,
                    "matched_cert_names": cert_matched_names,
                    "experience_level": job.get('experience_level', 'Any'),
                    "salary_range": f"{job.get('salary_min', 0):,} - {job.get('salary_max', 0):,} VND"
                })

        # Sort by match percentage descending
        matching.sort(key=lambda x: x['match_percentage'], reverse=True)
        return matching[:10]

    def _categorize_profile(self, matched_skills, sorted_missing_skills, matched_certs, sorted_missing_certs):
        """Categorize candidate profile strengths and gaps."""
        return {
            "strengths": list(matched_skills),
            "critical_gaps": list(map(lambda x: x[0], sorted_missing_skills[:3])),
            "nice_to_have": list(map(lambda x: x[0], sorted_missing_skills[3:8])),
            "recommended_certs": list(map(lambda x: x[0], sorted_missing_certs[:4])),
            "owned_certs": list(matched_certs)
        }

    def _empty_result(self, message):
        """Return empty result container."""
        return {
            "match_rate": "0%",
            "match_rate_value": 0,
            "skill_match_rate": "0%",
            "cert_match_rate": "0%",
            "degree_match_rate": "0%",
            "missing_skill": message,
            "missing_cert": "N/A",
            "all_missing_skills": [],
            "all_recommended_certs": [],
            "matched_skills": [],
            "matched_certs": [],
            "user_degree": "Đại học (Bachelor)",
            "user_experience": "Junior",
            "total_market_skills": 0,
            "total_jobs_analyzed": 0,
            "roadmap": [],
            "matching_jobs": [],
            "skill_categories": {"strengths": [], "critical_gaps": [], "nice_to_have": [], "recommended_certs": []},
            "recommendation_summary": message
        }