import json
from pathlib import Path

from prompt_templates import (
    build_cover_letter_prompt,
    build_interview_prompt,
    build_resume_prompt,
)
from text_analysis import compare_resume_to_job


DATA_FILE = Path("resume_sessions.json")


def normalize_session(session):
    resume_text = str(session.get("resume_text", "")).strip()
    job_text = str(session.get("job_text", "")).strip()

    if resume_text and job_text and "resume_keywords" not in session:
        analysis = compare_resume_to_job(resume_text, job_text)
    else:
        analysis = {
            "match_score": int(session.get("match_score", 0)),
            "resume_keywords": session.get("resume_keywords", []),
            "job_keywords": session.get("job_keywords", []),
            "exact_matches": session.get("exact_matches", session.get("matched_keywords", [])),
            "fuzzy_matches": session.get("fuzzy_matches", []),
            "matched_keywords": session.get("matched_keywords", []),
            "missing_keywords": session.get("missing_keywords", []),
        }

    return {
        "title": str(session.get("title", "Untitled Session")).strip() or "Untitled Session",
        "target_role": str(session.get("target_role", "General Role")).strip() or "General Role",
        "resume_text": resume_text,
        "job_text": job_text,
        "match_score": analysis["match_score"],
        "resume_keywords": analysis["resume_keywords"],
        "job_keywords": analysis["job_keywords"],
        "exact_matches": analysis["exact_matches"],
        "fuzzy_matches": analysis["fuzzy_matches"],
        "matched_keywords": analysis["matched_keywords"],
        "missing_keywords": analysis["missing_keywords"],
    }


def load_sessions():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [normalize_session(item) for item in data if isinstance(item, dict)]


def save_sessions(sessions):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(sessions, file, indent=2)


def read_multiline_input(label):
    print(f"\nPaste {label}. Type END on a new line when finished.")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def format_keywords(items):
    if not items:
        return "None"
    return ", ".join(items)


def show_analysis(session):
    print(f"\nTitle: {session['title']}")
    print(f"Target Role: {session['target_role']}")
    print(f"Match Score: {session['match_score']}%")
    print(f"Matched Keywords: {format_keywords(session['matched_keywords'])}")
    print(f"Exact Matches: {format_keywords(session['exact_matches'])}")
    if session["fuzzy_matches"]:
        print(f"Near Matches: {format_keywords(session['fuzzy_matches'])}")
    print(f"Missing Keywords: {format_keywords(session['missing_keywords'])}")


def show_saved_sessions(sessions):
    if not sessions:
        print("\nNo saved sessions found.")
        return

    print("\nSaved Sessions:")
    for index, session in enumerate(sessions, start=1):
        print(f"{index}. {session['title']} ({session['target_role']})")


def get_session_index(sessions, action_text):
    show_saved_sessions(sessions)
    if not sessions:
        return None

    try:
        number = int(input(f"Enter session number to {action_text}: ").strip())
        if 1 <= number <= len(sessions):
            return number - 1
    except ValueError:
        pass

    print("Invalid session number.")
    return None


def create_new_session(sessions):
    print("\nNew Resume Analysis")
    title = input("Enter a session title: ").strip() or "Untitled Session"
    target_role = input("Enter the target role: ").strip() or "General Role"
    resume_text = read_multiline_input("your resume text")
    job_text = read_multiline_input("the job description")

    if not resume_text or not job_text:
        print("Resume text and job description are required.")
        return

    analysis = compare_resume_to_job(resume_text, job_text)
    session = {
        "title": title,
        "target_role": target_role,
        "resume_text": resume_text,
        "job_text": job_text,
        "match_score": analysis["match_score"],
        "resume_keywords": analysis["resume_keywords"],
        "job_keywords": analysis["job_keywords"],
        "exact_matches": analysis["exact_matches"],
        "fuzzy_matches": analysis["fuzzy_matches"],
        "matched_keywords": analysis["matched_keywords"],
        "missing_keywords": analysis["missing_keywords"],
    }

    sessions.append(session)
    save_sessions(sessions)
    print("\nSession saved.")
    show_analysis(session)


def view_session_details(sessions):
    session_index = get_session_index(sessions, "view")
    if session_index is None:
        return

    show_analysis(sessions[session_index])


def show_generated_prompts(sessions):
    session_index = get_session_index(sessions, "use")
    if session_index is None:
        return

    session = sessions[session_index]
    print("\nResume Improvement Prompt:\n")
    print(build_resume_prompt(session))
    print("\nCover Letter Prompt:\n")
    print(build_cover_letter_prompt(session))
    print("\nInterview Practice Prompt:\n")
    print(build_interview_prompt(session))


def delete_session(sessions):
    session_index = get_session_index(sessions, "delete")
    if session_index is None:
        return

    deleted = sessions.pop(session_index)
    save_sessions(sessions)
    print(f"Deleted: {deleted['title']}")


def main():
    sessions = load_sessions()

    while True:
        print("\nResume Job Assistant")
        print("1. New resume-job analysis")
        print("2. View saved sessions")
        print("3. View session details")
        print("4. Generate advanced prompts")
        print("5. Delete session")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "":
            continue
        if choice == "1":
            create_new_session(sessions)
        elif choice == "2":
            show_saved_sessions(sessions)
        elif choice == "3":
            view_session_details(sessions)
        elif choice == "4":
            show_generated_prompts(sessions)
        elif choice == "5":
            delete_session(sessions)
        elif choice == "6":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
