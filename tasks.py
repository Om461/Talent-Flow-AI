from crewai import Task
from textwrap import dedent

def jd_parsing_task(recruiter, jd_text):
    return Task(
        description=dedent(f"""
            Analyze the following Job Description (JD):
            
            {jd_text}
            
            Expected action:
            Extract and output a structured JSON object containing EXACTLY:
            {{
                "top_5_hard_skills": ["skill1", "skill2", ...],
                "top_3_soft_skills": ["skill1", "skill2", ...],
                "candidate_persona": "Brief description of the ideal candidate"
            }}
            Ensure your final output is ONLY valid JSON.
        """),
        expected_output="A valid JSON object detailing the top skills and candidate persona.",
        agent=recruiter
    )

def resume_eval_task(evaluator, resumes_text, jd_task):
    return Task(
        description=dedent(f"""
            The following is the full extracted text from a set of candidate resumes.
            Each resume is separated by a header line like "--- Resume File: filename.pdf ---".
            
            RESUMES TEXT:
            {resumes_text}
            
            Using the JD criteria identified by the recruiter (provided as context), evaluate each resume.
            
            CRITICAL INSTRUCTIONS:
            - Assign a score from 0-100 for each candidate based strictly on technical merit and alignment with the JD.
            - BIAS-FREE FEATURE: Explicitly ignore names, gender, and geographic locations. Use only the filename as identifier.
            - Provide a brief 1-2 sentence justification for each score.
            
            Format your final output as a valid JSON array. Example:
            [
                {{"filename": "resume1.pdf", "score": 85, "justification": "Strong Python skills but lacks AWS experience."}},
                ...
            ]
            Output ONLY valid JSON, no extra text.
        """),
        expected_output="A ranked JSON array of candidates with scores and justifications.",
        agent=evaluator,
        context=[jd_task]
    )

def outreach_email_task(coordinator, rankings_json, resumes_text):
    return Task(
        description=dedent(f"""
            Based on the following evaluation results, select the top 3 scoring candidates.
            
            EVALUATION RESULTS (JSON):
            {rankings_json}
            
            ORIGINAL RESUMES TEXT (use this to find specific achievements):
            {resumes_text}
            
            Draft a high-conversion, personalized outreach email for each of the top 3 candidates.
            CRITICAL CONSTRAINT: You MUST mention a specific project or professional achievement found in the candidate's actual resume to prove this is not a generic template.
            
            Output the final emails clearly separated by headers like "=== EMAIL FOR [filename] ===" for each candidate.
        """),
        expected_output="Three personalized outreach emails for the top 3 candidates, each referencing a specific achievement from their resume.",
        agent=coordinator
    )
