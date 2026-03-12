import streamlit as st
import os
import json
import pandas as pd
from crewai import Crew, Process
from agents import create_recruiter, create_evaluator, create_coordinator
from tasks import jd_parsing_task, resume_eval_task, outreach_email_task
import PyPDF2
import tempfile
import sys
import io
import re

st.set_page_config(page_title="Talent Flow AI", page_icon="🤖", layout="wide")

# --- Custom Streamlit Stdout Capturer for "Live Thought Trace" ---
class StreamlitCapture(io.StringIO):
    def __init__(self, st_placeholder):
        super().__init__()
        self.st_placeholder = st_placeholder
        self.text = ""

    def write(self, string):
        self.text += string
        clean_text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', self.text)
        self.st_placeholder.code(clean_text[-3000:], language='text')

def extract_pdf_text(uploaded_files):
    """Extract text from all uploaded PDF files and return as a single string."""
    all_text = []
    for file in uploaded_files:
        try:
            pdf = PyPDF2.PdfReader(file)
            text = "".join(page.extract_text() or "" for page in pdf.pages)
            all_text.append(f"--- Resume File: {file.name} ---\n{text}\n")
        except Exception as e:
            all_text.append(f"--- Resume File: {file.name} ---\nError reading file: {e}\n")
    return "\n".join(all_text)

st.title("🤖 Autonomous Agent Recruitment System")
st.markdown("Transform a Job Description and a folder of PDF resumes into a ranked leaderboard and personalized outreach campaigns using CrewAI.")

# --- Sidebar Configuration ---
with st.sidebar:
    st.header("⚙️ Architecture Settings")
    st.markdown("Select an LLM for orchestrating the multi-agent system:")
    api_provider = st.radio("Provider", ["Groq (Fast)", "OpenAI (Deep)"])
    api_key = st.text_input(f"{api_provider.split()[0]} API Key", type="password")
    if api_key:
        if "Groq" in api_provider:
            os.environ["GROQ_API_KEY"] = api_key
            os.environ.pop("OPENAI_API_KEY", None)  # Clear OpenAI key to prevent fallback
        else:
            os.environ["OPENAI_API_KEY"] = api_key
            os.environ.pop("GROQ_API_KEY", None)

# --- Input Area ---
st.header("Step 1. Job Details & Resumes")
col1, col2 = st.columns(2)

with col1:
    jd_text = st.text_area("Job Description (JD)", height=300,
                            placeholder="Paste the job description (responsibilities, requirements)...")

with col2:
    uploaded_files = st.file_uploader("Upload PDF Resumes", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        st.success(f"{len(uploaded_files)} resume(s) uploaded.")

# State Management
if 'rankings' not in st.session_state:
    st.session_state.rankings = None
if 'resumes_text' not in st.session_state:
    st.session_state.resumes_text = ""

# --- Execution Button 1: Parsing & Evaluating ---
if st.button("🚀 Analyze & Rank Candidates"):
    if not jd_text or not uploaded_files:
        st.warning("Please provide a Job Description and at least one PDF Resume.")
    elif not api_key:
        st.warning("Please configure your API Key in the sidebar.")
    else:
        # Extract all PDF text BEFORE running agents (avoids unreliable tool-calling)
        with st.spinner("Extracting resume text..."):
            resumes_text = extract_pdf_text(uploaded_files)
            st.session_state.resumes_text = resumes_text

        st.markdown("### 🧠 Live Agent Thought Trace")
        trace_placeholder = st.empty()

        original_stdout = sys.stdout
        sys.stdout = StreamlitCapture(trace_placeholder)

        try:
            recruiter = create_recruiter()
            evaluator = create_evaluator()

            t1 = jd_parsing_task(recruiter, jd_text)
            t2 = resume_eval_task(evaluator, resumes_text, t1)

            crew = Crew(
                agents=[recruiter, evaluator],
                tasks=[t1, t2],
                process=Process.sequential,
                verbose=True
            )

            result = crew.kickoff()
            res_str = str(result)

            # Parse JSON out of the result (handles extra markdown backticks from LLM)
            json_match = re.search(r'\[.*\]', res_str, re.DOTALL)
            if json_match:
                st.session_state.rankings = json.loads(json_match.group(0))
            else:
                st.session_state.rankings = [{"filename": "Result", "score": "N/A", "justification": res_str}]

            st.success("Analysis Complete!")

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
        finally:
            sys.stdout = original_stdout

# --- Results & Leaderboard ---
if st.session_state.rankings is not None:
    st.markdown("---")
    st.header("Step 2. Evaluation Results (Leaderboard)")

    df = pd.DataFrame(st.session_state.rankings)
    if 'score' in df.columns:
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        df = df.sort_values(by="score", ascending=False).reset_index(drop=True)

    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Save Rankings to CSV", data=csv_data,
                       file_name="ai_talent_rankings.csv", mime="text/csv")

    st.markdown("---")
    st.header("Step 3. Human-In-The-Loop Approval")
    st.info("Review the leaderboard above. Click below to have the Talent Coordinator draft personalized outreach emails for the top 3 candidates.")

    if st.button("✉️ Approve & Generate Top 3 Outreach Emails"):
        st.markdown("### 🧠 Live Agent Thought Trace (Coordinator)")
        coord_trace = st.empty()

        original_stdout = sys.stdout
        sys.stdout = StreamlitCapture(coord_trace)

        try:
            coordinator = create_coordinator()
            email_task = outreach_email_task(
                coordinator,
                json.dumps(st.session_state.rankings),
                st.session_state.resumes_text
            )

            email_crew = Crew(
                agents=[coordinator],
                tasks=[email_task],
                process=Process.sequential,
                verbose=True
            )

            final_emails = email_crew.kickoff()
            st.success("Drafts generated!")

            st.markdown("### Final Outreach Emails")
            st.write(final_emails.raw if hasattr(final_emails, 'raw') else str(final_emails))

        except Exception as e:
            st.error(f"Error generating outreach emails: {str(e)}")
        finally:
            sys.stdout = original_stdout
