from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AnalyzeRequest(BaseModel):
    job_description: str
    resume: str


class CoverLetterRequest(BaseModel):
    job_description: str
    resume: str
    company_name: str
    role: str


@router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    """Analyze how well a resume matches a job description."""
    try:
        prompt = f"""
You are a recruiter. Analyze how well this resume matches the job description.

JOB DESCRIPTION:
{req.job_description}

RESUME:
{req.resume}

Respond in this exact JSON format (no markdown, no code blocks):
{{
  "score": <number 0-100>,
  "feedback": [
    "<strength or gap point 1>",
    "<strength or gap point 2>",
    "<strength or gap point 3>"
  ],
  "summary": "<one sentence overall assessment>"
}}
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cover-letter")
async def cover_letter(req: CoverLetterRequest):
    """Generate a tailored cover letter."""
    try:
        prompt = f"""
Write a concise, professional cover letter for this job application.

ROLE: {req.role} at {req.company_name}

JOB DESCRIPTION:
{req.job_description}

RESUME:
{req.resume}

Guidelines:
- 3 short paragraphs max
- Specific to the role and company
- Confident, not generic
- No "Dear Hiring Manager" clichés — use "Hello {req.company_name} Team,"
- End with a clear call to action

Return only the cover letter text, nothing else.
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return {"cover_letter": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
