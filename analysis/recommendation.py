"""
Career Recommendation Module (Member 6 - SP6)
Advanced recommendation algorithm using lambda, filter, map.
Compares student skills against market demands and suggests learning paths.
"""


class CareerRecommender:
    """
    Career Recommendation Engine.
    Uses advanced Python functions (lambda, filter, map) to:
    - Analyze user skills against market demand
    - Calculate profile match rate
    - Identify skill gaps with priority ranking
    - Generate personalized learning roadmap
    """

    def __init__(self, db_manager):
        self.db = db_manager

    def recommend(self, user_skills_string):
        """
        Main recommendation method.
        Returns a comprehensive recommendation report as a dictionary.
        """
        # 1. Parse user skills using map() and filter()
        user_skills = set(
            filter(
                lambda s: len(s) > 0,
                map(lambda s: s.strip().upper(), user_skills_string.split(','))
            )
        )

        if not user_skills:
            return self._empty_result("Please enter at least one skill.")

        # 2. Get market data from database
        market_jobs = self.db.get_all_skills_from_db()
        if not market_jobs:
            return self._empty_result("No market data available.")

        # 3. Calculate skill frequency across all job listings
        skill_frequency = {}
        total_jobs = len(market_jobs)

        for job_skills_str in market_jobs:
            job_skills = list(
                map(lambda s: s.strip().upper(), job_skills_str.split(','))
            )
            for skill in job_skills:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1

        # 4. Find matching skills using filter()
        matched_skills = list(
            filter(lambda s: s in skill_frequency, user_skills)
        )

        # 5. Find missing skills (skills the market wants but user doesn't have)
        missing_skills = dict(
            filter(
                lambda item: item[0] not in user_skills,
                skill_frequency.items()
            )
        )

        # 6. Sort missing skills by market demand (most important first)
        sorted_missing = sorted(
            missing_skills.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # 7. Calculate match rate based on weighted skill coverage
        total_demand_points = sum(skill_frequency.values())
        matched_points = sum(
            map(
                lambda s: skill_frequency.get(s, 0),
                matched_skills
            )
        )
        match_rate = min(98, int((matched_points / total_demand_points) * 100)) if total_demand_points > 0 else 0

        # 8. Get top missing skill
        top_missing = sorted_missing[0][0] if sorted_missing else "None"

        # 9. Generate learning roadmap
        roadmap = self._generate_roadmap(sorted_missing, matched_skills)

        # 10. Get matching job titles
        matching_jobs = self._find_matching_jobs(user_skills)

        # 11. Skill category analysis
        skill_categories = self._categorize_skills(matched_skills, sorted_missing)

        return {
            "match_rate": f"{match_rate}%",
            "match_rate_value": match_rate,
            "missing_skill": top_missing,
            "all_missing_skills": list(map(lambda x: {"skill": x[0], "demand": x[1]}, sorted_missing[:10])),
            "matched_skills": list(matched_skills),
            "total_market_skills": len(skill_frequency),
            "total_jobs_analyzed": total_jobs,
            "roadmap": roadmap,
            "matching_jobs": matching_jobs,
            "skill_categories": skill_categories,
            "recommendation_summary": self._generate_summary(match_rate, top_missing, len(matched_skills))
        }

    def _generate_roadmap(self, sorted_missing, matched_skills):
        """Generate a personalized learning roadmap based on skill gaps."""
        roadmap = []

        if not sorted_missing:
            return [{"phase": "Expert Level", "title": "Stay Updated",
                     "description": "Your skills are well-aligned with the market. Focus on deepening expertise and staying current with trends.",
                     "duration": "Ongoing"}]

        # Phase 1: Foundation strengthening
        if len(matched_skills) < 3:
            roadmap.append({
                "phase": "Phase 1",
                "title": "Strengthen Core Foundations",
                "description": "Solidify your existing skills with practical projects and certifications.",
                "skills": list(matched_skills)[:3],
                "duration": "2-4 weeks"
            })

        # Phase 2: Learn most-demanded missing skill
        if len(sorted_missing) >= 1:
            top_skill = sorted_missing[0][0]
            roadmap.append({
                "phase": f"Phase {len(roadmap) + 1}",
                "title": f"Master {top_skill}",
                "description": f"{top_skill} is the most in-demand skill you're missing. "
                               f"It appears in {sorted_missing[0][1]} job listings.",
                "skills": [top_skill],
                "duration": "4-6 weeks"
            })

        # Phase 3: Learn complementary skills
        if len(sorted_missing) >= 3:
            complementary = list(map(lambda x: x[0], sorted_missing[1:4]))
            roadmap.append({
                "phase": f"Phase {len(roadmap) + 1}",
                "title": "Expand Skill Set",
                "description": f"Learn complementary skills to increase your market coverage: {', '.join(complementary)}",
                "skills": complementary,
                "duration": "6-8 weeks"
            })

        # Phase 4: Practical application
        roadmap.append({
            "phase": f"Phase {len(roadmap) + 1}",
            "title": "Build Real Projects",
            "description": "Apply your new skills in portfolio projects. Contribute to open source or build personal projects.",
            "skills": [],
            "duration": "4-8 weeks"
        })

        return roadmap

    def _find_matching_jobs(self, user_skills):
        """Find job titles that match user's skills."""
        try:
            jobs = self.db.get_all_jobs(limit=50)
            matching = []

            for job in jobs:
                if not job.get('skills'):
                    continue
                job_skills = set(
                    map(lambda s: s.strip().upper(), job['skills'].split(','))
                )
                overlap = user_skills.intersection(job_skills)
                if overlap:
                    match_pct = int((len(overlap) / len(job_skills)) * 100)
                    matching.append({
                        "title": job['title'],
                        "company": job['company'],
                        "match_percentage": match_pct,
                        "matching_skills": list(overlap),
                        "salary_range": f"{job.get('salary_min', 0):,} - {job.get('salary_max', 0):,} VND"
                    })

            # Sort by match percentage
            matching.sort(key=lambda x: x['match_percentage'], reverse=True)
            return matching[:10]
        except Exception:
            return []

    def _categorize_skills(self, matched, sorted_missing):
        """Categorize skills into strengths, gaps, and opportunities."""
        categories = {
            "strengths": list(matched),
            "critical_gaps": list(map(lambda x: x[0], sorted_missing[:3])),
            "nice_to_have": list(map(lambda x: x[0], sorted_missing[3:8])),
        }
        return categories

    def _generate_summary(self, match_rate, top_missing, matched_count):
        """Generate a human-readable recommendation summary."""
        if match_rate >= 80:
            return f"Excellent! Your profile is highly competitive with a {match_rate}% market match. " \
                   f"Consider learning {top_missing} to reach expert level."
        elif match_rate >= 50:
            return f"Good foundation! You match {match_rate}% of market demands with {matched_count} relevant skills. " \
                   f"Priority: learn {top_missing} to significantly boost your profile."
        elif match_rate >= 25:
            return f"Getting started! Your {matched_count} skills give you a {match_rate}% match. " \
                   f"Focus on {top_missing} as it's the most requested skill you're missing."
        else:
            return f"Your profile matches {match_rate}% of current market demands. " \
                   f"Start by learning {top_missing}, the most in-demand skill in the market."

    def _empty_result(self, message):
        """Return an empty result with an error message."""
        return {
            "match_rate": "0%",
            "match_rate_value": 0,
            "missing_skill": message,
            "all_missing_skills": [],
            "matched_skills": [],
            "total_market_skills": 0,
            "total_jobs_analyzed": 0,
            "roadmap": [],
            "matching_jobs": [],
            "skill_categories": {"strengths": [], "critical_gaps": [], "nice_to_have": []},
            "recommendation_summary": message
        }