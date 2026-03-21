def _format_bullets(items):
    if not items:
        return "- None identified"
    return "\n".join(f"- {item}" for item in items)


def build_resume_prompt(session):
    return f"""Act as a professional resume writer and hiring advisor.

Task:
Rewrite the resume so it better matches the target job without adding false information.

Requirements:
- Improve clarity, professionalism, and impact
- Align the resume with the target role: {session['target_role']}
- Strengthen bullet points using measurable, action-oriented wording
- Emphasize the matching skills already present in the resume

Constraints:
- Do not invent projects, tools, or experience
- Keep the resume suitable for a beginner or early-career candidate
- Focus on truthful improvement only
- Try to address these missing job keywords when they are genuinely supported by the resume
{_format_bullets(session['missing_keywords'])}

Output Format:
- Give a rewritten professional summary
- Give 4 to 6 improved resume bullet points
- Give a short list of suggested skills to highlight

Context:
- Match score: {session['match_score']}%
- Matched job keywords:
{_format_bullets(session['matched_keywords'])}
"""


def build_cover_letter_prompt(session):
    return f"""Act as a professional career assistant.

Task:
Write a short cover letter tailored to the target job.

Requirements:
- Use a professional but simple tone
- Mention the role: {session['target_role']}
- Connect the candidate's background to the job needs
- Highlight the most relevant matching skills

Constraints:
- Do not invent achievements or qualifications
- Keep the cover letter concise
- Keep the language natural and beginner-friendly

Output Format:
- Greeting
- 3 short body paragraphs
- Closing paragraph

Context:
- Matched job keywords:
{_format_bullets(session['matched_keywords'])}
- Missing job keywords:
{_format_bullets(session['missing_keywords'])}
"""


def build_interview_prompt(session):
    return f"""Act as an interview coach.

Task:
Generate likely interview questions and short sample answers for this candidate and target role.

Requirements:
- Focus on beginner-level interview preparation
- Base the questions on the resume and job description
- Include technical and HR-style questions

Constraints:
- Do not assume experience that is not present
- Keep answers realistic and concise

Output Format:
- 5 interview questions
- A short sample answer for each
- A final section called "What to improve before the interview"

Context:
- Target role: {session['target_role']}
- Match score: {session['match_score']}%
- Missing job keywords:
{_format_bullets(session['missing_keywords'])}
"""
