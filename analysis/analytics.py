"""
Analytics & Visualization Module (Member 5 - SP4 & SP5)
Performs statistical analysis on job market data and generates
high-resolution charts using Matplotlib.
"""

import os
from datetime import datetime


class MarketAnalytics:
    """
    Market Analytics engine.
    - SQL queries → Pandas for statistical analysis
    - Skill frequency analysis
    - Salary distribution by experience
    - Top companies hiring
    - Chart generation with Matplotlib
    """

    def __init__(self, db_manager):
        self.db = db_manager
        self.charts_dir = 'static/charts'
        os.makedirs(self.charts_dir, exist_ok=True)

    def get_full_report(self):
        """Generate a comprehensive market analysis report as JSON."""
        return {
            "generated_at": datetime.now().isoformat(),
            "skill_demand": self.db.get_skill_frequency(20),
            "salary_by_experience": self.db.get_salary_by_experience(),
            "top_companies": self.db.get_top_companies(10),
            "jobs_by_source": self.db.get_jobs_by_source(),
            "skills_by_category": self.db.get_skills_by_category(),
            "jobs_by_location": self.db.get_jobs_by_location(),
            "total_jobs": self.db.get_job_count(),
            "total_companies": self.db.get_company_count(),
            "avg_salary": self.db.get_avg_salary(),
        }

    def generate_all_charts(self):
        """Generate all analysis charts and save as PNG files."""
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            import matplotlib.ticker as ticker
        except ImportError:
            print("Matplotlib not available. Charts will be served via Chart.js on the frontend.")
            return []

        charts_generated = []

        # Set global style
        plt.rcParams.update({
            'figure.facecolor': '#0f172a',
            'axes.facecolor': '#1e293b',
            'axes.edgecolor': '#475569',
            'text.color': '#f8fafc',
            'axes.labelcolor': '#94a3b8',
            'xtick.color': '#94a3b8',
            'ytick.color': '#94a3b8',
            'font.size': 11,
            'axes.titlesize': 14,
            'axes.titleweight': 'bold',
        })

        # Chart 1: Top Skills Demand (Horizontal Bar)
        try:
            skills = self.db.get_skill_frequency(15)
            if skills:
                fig, ax = plt.subplots(figsize=(10, 6))
                names = [s['name'] for s in reversed(skills)]
                counts = [s['frequency'] for s in reversed(skills)]

                colors = plt.cm.viridis([i / len(names) for i in range(len(names))])
                bars = ax.barh(names, counts, color=colors, edgecolor='none', height=0.7)
                ax.set_title('Top 15 Most In-Demand Skills', pad=15)
                ax.set_xlabel('Number of Job Listings')

                for bar, count in zip(bars, counts):
                    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                            str(count), va='center', color='#f8fafc', fontsize=10)

                plt.tight_layout()
                path = os.path.join(self.charts_dir, 'skill_demand.png')
                fig.savefig(path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                charts_generated.append(path)
        except Exception as e:
            print(f"Error generating skill demand chart: {e}")

        # Chart 2: Salary Distribution by Experience
        try:
            salary_data = self.db.get_salary_by_experience()
            if salary_data:
                fig, ax = plt.subplots(figsize=(10, 6))
                levels = [s['experience_level'] for s in salary_data]
                avg_min = [s['avg_min'] / 1000000 for s in salary_data]
                avg_max = [s['avg_max'] / 1000000 for s in salary_data]

                x = range(len(levels))
                width = 0.35
                bars1 = ax.bar([i - width / 2 for i in x], avg_min, width,
                               label='Avg Min Salary', color='#3b82f6', alpha=0.8)
                bars2 = ax.bar([i + width / 2 for i in x], avg_max, width,
                               label='Avg Max Salary', color='#10b981', alpha=0.8)

                ax.set_title('Salary Distribution by Experience Level', pad=15)
                ax.set_ylabel('Salary (Million VND)')
                ax.set_xticks(list(x))
                ax.set_xticklabels(levels)
                ax.legend(facecolor='#334155', edgecolor='#475569')
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{x:.0f}M'))

                plt.tight_layout()
                path = os.path.join(self.charts_dir, 'salary_distribution.png')
                fig.savefig(path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                charts_generated.append(path)
        except Exception as e:
            print(f"Error generating salary chart: {e}")

        # Chart 3: Top Companies (Bar)
        try:
            companies = self.db.get_top_companies(10)
            if companies:
                fig, ax = plt.subplots(figsize=(10, 6))
                names = [c['name'] for c in reversed(companies)]
                counts = [c['job_count'] for c in reversed(companies)]

                colors = plt.cm.plasma([i / len(names) for i in range(len(names))])
                ax.barh(names, counts, color=colors, edgecolor='none', height=0.7)
                ax.set_title('Top 10 Companies by Job Listings', pad=15)
                ax.set_xlabel('Number of Listings')

                plt.tight_layout()
                path = os.path.join(self.charts_dir, 'top_companies.png')
                fig.savefig(path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                charts_generated.append(path)
        except Exception as e:
            print(f"Error generating companies chart: {e}")

        # Chart 4: Skills by Category (Pie)
        try:
            categories = self.db.get_skills_by_category()
            if categories:
                fig, ax = plt.subplots(figsize=(8, 8))
                labels = [c['category'] for c in categories]
                sizes = [c['job_count'] for c in categories]

                colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                          '#06b6d4', '#f97316', '#ec4899', '#84cc16', '#6366f1']
                explode = [0.05] * len(labels)

                wedges, texts, autotexts = ax.pie(
                    sizes, labels=labels, autopct='%1.1f%%',
                    colors=colors[:len(labels)], explode=explode[:len(labels)],
                    textprops={'color': '#f8fafc', 'fontsize': 10},
                    pctdistance=0.85
                )
                for autotext in autotexts:
                    autotext.set_fontsize(9)

                ax.set_title('Job Market Share by Skill Category', pad=20)
                plt.tight_layout()
                path = os.path.join(self.charts_dir, 'skill_categories.png')
                fig.savefig(path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                charts_generated.append(path)
        except Exception as e:
            print(f"Error generating category chart: {e}")

        # Chart 5: Jobs by Location
        try:
            locations = self.db.get_jobs_by_location()
            if locations:
                fig, ax = plt.subplots(figsize=(8, 6))
                names = [l['location'] for l in locations]
                counts = [l['count'] for l in locations]

                colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
                bars = ax.bar(names, counts, color=colors[:len(names)],
                              edgecolor='none', width=0.6)
                ax.set_title('Job Distribution by Location', pad=15)
                ax.set_ylabel('Number of Jobs')

                for bar, count in zip(bars, counts):
                    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                            str(count), ha='center', color='#f8fafc', fontsize=11)

                plt.tight_layout()
                path = os.path.join(self.charts_dir, 'jobs_by_location.png')
                fig.savefig(path, dpi=150, bbox_inches='tight')
                plt.close(fig)
                charts_generated.append(path)
        except Exception as e:
            print(f"Error generating location chart: {e}")

        print(f"✅ Generated {len(charts_generated)} charts in {self.charts_dir}/")
        return charts_generated
