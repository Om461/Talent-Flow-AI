"""
Script to generate realistic mock PDF resumes for Talent Flow AI demo.
Uses only built-in Python + PyPDF2 approach via reportlab or fpdf2.
"""
from fpdf import FPDF
import os

RESUMES_DIR = os.path.join(os.path.dirname(__file__), "mock_resumes")
os.makedirs(RESUMES_DIR, exist_ok=True)

RESUMES = [
    {
        "filename": "Alice_Chen_ML_Engineer.pdf",
        "name": "A. Chen",
        "title": "Senior Machine Learning Engineer",
        "summary": "7+ years of experience in building and deploying production ML systems at scale. Expert in deep learning, NLP, and MLOps pipelines.",
        "skills": "Python, PyTorch, TensorFlow, Kubernetes, Apache Spark, Airflow, AWS SageMaker, SQL, Docker, Git",
        "experience": [
            ("ML Engineer", "DataScale Inc.", "2020–2024",
             "- Built a real-time fraud detection model reducing false positives by 40%\n"
             "- Deployed transformer-based NLP pipeline processing 5M documents/day\n"
             "- Led team of 4 ML engineers on customer churn prediction project (ROI: $2M)"),
            ("Junior Data Scientist", "TechVision Ltd.", "2017–2020",
             "- Developed recommendation engine increasing user engagement by 25%\n"
             "- Automated feature engineering pipeline saving 20 hrs/week of manual work"),
        ],
        "education": "M.Sc. Computer Science (ML Specialization) – Stanford University",
        "projects": ["Open-source contributor to Hugging Face Transformers (500+ GitHub stars)", "LLM fine-tuning toolkit for enterprise RAG (published on arXiv)"]
    },
    {
        "filename": "Bob_Martinez_Data_Engineer.pdf",
        "name": "B. Martinez",
        "title": "Data Engineer",
        "summary": "5 years of experience building scalable ETL pipelines and data infrastructure. Passionate about data reliability and observability.",
        "skills": "Python, SQL, dbt, Apache Kafka, Spark, Snowflake, Airflow, GCP BigQuery, Terraform, Looker",
        "experience": [
            ("Senior Data Engineer", "StreamCo", "2021–2024",
             "- Designed and built a real-time data lake ingesting 10TB/day using Kafka + Spark Streaming\n"
             "- Reduced pipeline failure rate by 60% via dbt testing and Great Expectations integration\n"
             "- Migrated legacy ETL to cloud-native stack (Snowflake + dbt), cutting costs by 35%"),
            ("Data Engineer", "RetailTech", "2019–2021",
             "- Maintained SQL data warehouse for 50+ internal stakeholders\n"
             "- Built automated reporting dashboards in Looker"),
        ],
        "education": "B.Sc. Information Systems – University of Texas",
        "projects": ["Built open-source dbt package for Snowflake monitoring (200+ GitHub stars)", "Speaker at Data Council 2023 on data observability"]
    },
    {
        "filename": "Carol_Kim_MLOps.pdf",
        "name": "C. Kim",
        "title": "MLOps Engineer",
        "summary": "4 years of experience bridging the gap between ML research and production, specializing in CI/CD for ML and model monitoring.",
        "skills": "Python, MLflow, Kubeflow, Docker, Kubernetes, GCP Vertex AI, Prometheus, Grafana, FastAPI, Terraform",
        "experience": [
            ("MLOps Engineer", "NeuralSystems Corp.", "2021–2024",
             "- Implemented automated model retraining pipeline with drift detection, reducing model degradation by 50%\n"
             "- Built model serving infrastructure handling 50K+ requests/second on Kubernetes\n"
             "- Developed ML experiment tracking system now used by 30 data scientists"),
            ("DevOps Engineer", "SaaSPlatform", "2020–2021",
             "- Managed CI/CD pipelines for 15 microservices\n"
             "- Reduced deployment time from 2 hours to 12 minutes"),
        ],
        "education": "B.Sc. Software Engineering – Georgia Tech",
        "projects": ["Author of 'MLOps Patterns' blog (20K monthly readers)", "Built open-source Prometheus exporter for MLflow tracking"]
    },
    {
        "filename": "David_Okafor_Backend_Dev.pdf",
        "name": "D. Okafor",
        "title": "Backend Software Engineer",
        "summary": "3 years of backend development experience. Comfortable with REST APIs and microservices but limited ML exposure.",
        "skills": "Java, Python (beginner), Spring Boot, REST APIs, PostgreSQL, Redis, RabbitMQ, Docker",
        "experience": [
            ("Backend Engineer", "FinTech Solutions", "2021–2024",
             "- Built payment processing API handling $100M/month transactions\n"
             "- Designed microservices architecture for customer authentication service\n"
             "- Reduced API latency by 30% via Redis caching layer"),
        ],
        "education": "B.Sc. Computer Science – University of Lagos",
        "projects": ["Built personal expense tracker app using Spring Boot and PostgreSQL", "Open source contributor to Apache Kafka (minor bug fix)"]
    },
    {
        "filename": "Eva_Singh_AI_Researcher.pdf",
        "name": "E. Singh",
        "title": "AI Research Scientist",
        "summary": "PhD-level research background in computer vision and generative models. Published 8 papers in top-tier venues (NeurIPS, ICML, CVPR).",
        "skills": "Python, PyTorch, JAX, CUDA, NumPy, Scikit-learn, Hugging Face, W&B, LaTeX, Linux",
        "experience": [
            ("Research Scientist", "AI Research Lab", "2022–2024",
             "- First-authored paper on efficient diffusion model training accepted at NeurIPS 2023\n"
             "- Developed novel attention mechanism resulting in 15% benchmark improvement on ImageNet\n"
             "- Mentored 3 junior researchers and led weekly reading group of 20 researchers"),
            ("Research Intern", "MegaCorp AI", "2021",
             "- Implemented and benchmarked 5 SOTA object detection models\n"
             "- Co-authored a workshop paper at CVPR"),
        ],
        "education": "Ph.D. Artificial Intelligence – MIT (2022)",
        "projects": ["8 peer-reviewed publications (h-index: 12, 1200+ citations)", "Released open-source diffusion model fine-tuning toolkit (3K+ GitHub stars)"]
    },
]

class ResumePDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "Talent Flow AI - Mock Resume (Demo Only)", align="C")

def sanitize(text):
    """Replace common Unicode punctuation with ASCII equivalents so fpdf latin-1 fonts work."""
    replacements = {
        '\u2013': '-',   # en dash
        '\u2014': '-',   # em dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2026': '...',  # ellipsis
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    # Final fallback: encode to latin-1 ignoring unrepresentable chars
    return text.encode('latin-1', errors='replace').decode('latin-1')


def write_section(pdf, title):
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(60, 100, 170)
    pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(60, 100, 170)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 175, pdf.get_y())
    pdf.ln(2)
    pdf.set_text_color(30, 30, 30)

def create_resume_pdf(data):
    pdf = ResumePDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Name and Title ---
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, sanitize(data["name"]), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, sanitize(data["title"]), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # --- Summary ---
    write_section(pdf, "PROFESSIONAL SUMMARY")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 5, sanitize(data["summary"]))
    pdf.ln(4)

    # --- Skills ---
    write_section(pdf, "CORE SKILLS")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, sanitize(data["skills"]))
    pdf.ln(4)

    # --- Experience ---
    write_section(pdf, "PROFESSIONAL EXPERIENCE")
    for title, company, period, bullets in data["experience"]:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(20, 20, 20)
        pdf.cell(120, 6, sanitize(f"{title} - {company}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 5, sanitize(period), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 5, sanitize(bullets))
        pdf.ln(3)

    # --- Education ---
    write_section(pdf, "EDUCATION")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, sanitize(data["education"]))
    pdf.ln(4)

    # --- Notable Projects ---
    write_section(pdf, "NOTABLE PROJECTS & CONTRIBUTIONS")
    pdf.set_font("Helvetica", "", 10)
    for project in data["projects"]:
        pdf.multi_cell(0, 5, sanitize(f"* {project}"))

        pdf.ln(1)

    # Save to disk
    out_path = os.path.join(RESUMES_DIR, data["filename"])
    pdf.output(out_path)
    print(f"Created: {out_path}")

if __name__ == "__main__":
    print("Installing fpdf2 if needed...")
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pip", "install", "fpdf2", "-q"])
    
    from fpdf import FPDF
    print(f"\nGenerating {len(RESUMES)} mock resumes in '{RESUMES_DIR}'...\n")
    for resume_data in RESUMES:
        create_resume_pdf(resume_data)
    print(f"\n✅ Done! {len(RESUMES)} PDF resumes created in: {RESUMES_DIR}")
