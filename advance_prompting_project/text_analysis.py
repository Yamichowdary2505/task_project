from collections import Counter
from difflib import SequenceMatcher
import re


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
    "will",
    "your",
    "you",
    "our",
    "we",
    "this",
    "their",
    "they",
    "using",
    "use",
    "used",
    "into",
    "than",
    "can",
    "job",
    "role",
    "work",
    "team",
    "ability",
    "experience",
    "skills",
    "skill",
    "looking",
    "hiring",
    "required",
    "responsible",
    "responsibilities",
    "candidate",
    "preferred",
    "strong",
    "good",
    "knowledge",
    "about",
    "across",
    "among",
    "through",
    "engineer",
    "engineering",
    "developer",
    "development",
    "built",
    "project",
    "projects",
    "tool",
    "tools",
    "worked",
    "simple",
    "gen",
    "btech",
    "technology",
}

PHRASE_KEYWORDS = (
    "artificial intelligence",
    "generative ai",
    "gen ai",
    "prompt engineering",
    "machine learning",
    "deep learning",
    "data science",
    "data analysis",
    "computer vision",
    "natural language processing",
    "large language model",
    "api integration",
    "problem solving",
    "web development",
)

TERM_ALIASES = {
    "apis": "api",
    "api": "api",
    "llms": "llm",
    "llm": "llm",
    "graduates": "graduate",
    "graduated": "graduate",
    "graduate": "graduate",
    "gradtuate": "graduate",
    "btech": "btech",
    "tech": "technology",
    "gen ai": "generative ai",
    "artificial intelligence": "ai",
    "natural language processing": "nlp",
}

FUZZY_MATCH_THRESHOLD = 0.84


def normalize_term(term):
    cleaned = re.sub(r"[^a-z0-9+#\s-]", "", term.lower()).strip()
    if (
        cleaned.endswith("s")
        and len(cleaned) > 4
        and cleaned not in TERM_ALIASES
        and not cleaned.endswith(("ics", "ss"))
    ):
        cleaned = cleaned[:-1]
    return TERM_ALIASES.get(cleaned, cleaned)


def tokenize_text(text):
    raw_words = re.findall(r"[A-Za-z][A-Za-z0-9+#-]*", text.lower())
    normalized_words = []

    for word in raw_words:
        normalized_word = normalize_term(word)
        if len(normalized_word) > 2 and normalized_word not in STOPWORDS:
            normalized_words.append(normalized_word)

    return normalized_words


def extract_phrase_keywords(text):
    lowered_text = text.lower()
    phrases = []

    for phrase in PHRASE_KEYWORDS:
        if phrase in lowered_text:
            phrases.append(normalize_term(phrase))

    return phrases


def extract_keywords(text, limit=15):
    phrase_keywords = extract_phrase_keywords(text)
    ignored_phrase_parts = {
        normalize_term(part)
        for phrase in phrase_keywords
        for part in phrase.split()
        if len(normalize_term(part)) > 2
    }

    token_keywords = [
        token for token in tokenize_text(text) if token not in ignored_phrase_parts
    ]
    combined_terms = token_keywords + phrase_keywords
    counts = Counter(combined_terms)
    return [word for word, _ in counts.most_common(limit)]


def find_fuzzy_matches(resume_keywords, job_keywords):
    fuzzy_matches = []
    used_resume_keywords = set()

    for job_keyword in job_keywords:
        if job_keyword in resume_keywords:
            continue

        best_resume_keyword = None
        best_ratio = 0

        for resume_keyword in resume_keywords:
            if resume_keyword in used_resume_keywords:
                continue

            similarity_ratio = SequenceMatcher(None, job_keyword, resume_keyword).ratio()
            if similarity_ratio > best_ratio:
                best_ratio = similarity_ratio
                best_resume_keyword = resume_keyword

        if best_resume_keyword and best_ratio >= FUZZY_MATCH_THRESHOLD:
            fuzzy_matches.append(f"{job_keyword} -> {best_resume_keyword}")
            used_resume_keywords.add(best_resume_keyword)

    return fuzzy_matches


def compare_resume_to_job(resume_text, job_text):
    resume_keywords = extract_keywords(resume_text, limit=20)
    job_keywords = extract_keywords(job_text, limit=20)

    resume_keyword_set = set(resume_keywords)
    job_keyword_set = set(job_keywords)

    exact_matches = sorted(resume_keyword_set & job_keyword_set)
    fuzzy_matches = find_fuzzy_matches(resume_keywords, job_keywords)

    fuzzy_matched_job_keywords = {
        match.split(" -> ", maxsplit=1)[0] for match in fuzzy_matches
    }
    matched_keywords = sorted(set(exact_matches) | fuzzy_matched_job_keywords)
    missing_keywords = sorted(job_keyword_set - set(exact_matches) - fuzzy_matched_job_keywords)

    if not job_keyword_set:
        match_score = 0
    else:
        weighted_match_total = len(exact_matches) + (0.7 * len(fuzzy_matches))
        match_score = round((weighted_match_total / len(job_keyword_set)) * 100)

    return {
        "resume_keywords": sorted(resume_keyword_set),
        "job_keywords": sorted(job_keyword_set),
        "exact_matches": exact_matches,
        "fuzzy_matches": fuzzy_matches,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "match_score": min(match_score, 100),
    }
