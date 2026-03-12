from crewai import Agent, LLM
import os


def get_llm():
    """
    Use crewai.LLM which wraps LiteLLM properly.
    Supports Groq natively via the 'groq/' model prefix.
    """
    groq_key = os.getenv("GROQ_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if groq_key:
        return LLM(
            model="groq/llama-3.3-70b-versatile",
            api_key=groq_key,
            temperature=0.3
        )
    elif openai_key:
        return LLM(
            model="gpt-4-turbo",
            api_key=openai_key,
            temperature=0.3
        )
    else:
        raise ValueError("No API key found. Set GROQ_API_KEY or OPENAI_API_KEY in the sidebar.")


def create_recruiter():
    return Agent(
        role='Lead Technical Recruiter',
        goal='Analyze the Job Description and extract key requirements, skills, and ideal candidate persona.',
        backstory='You are an expert technical recruiter with years of experience identifying top talent for elite tech companies. You excel at reading between the lines of a JD.',
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )


def create_evaluator():
    # No tools needed — PDF text is injected directly into the task prompt
    return Agent(
        role='Technical Evaluator',
        goal='Evaluate resumes against the JD criteria objectively and score them from 0-100 without bias.',
        backstory='You are a strict, unbiased AI technical evaluator. You ignore names, genders, and locations, focusing purely on skills, experience, and project impact.',
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )


def create_coordinator():
    return Agent(
        role='Talent Coordinator',
        goal='Draft highly personalized outreach emails for top-scoring candidates based on their specific resume achievements.',
        backstory="You are a master communicator and talent coordinator. Your outreach emails have a 90% response rate because you always highlight specific, impressive details from a candidate's past work.",
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )
