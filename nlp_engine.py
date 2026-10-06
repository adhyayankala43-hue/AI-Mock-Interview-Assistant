import os
import json
import re
import datetime
from typing import Tuple, List, Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import spacy
from textblob import TextBlob
from google import genai
from google.genai import types

# ─── Initialize spaCy ────────────────────────────────────────────────────────
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None
    print("[WARNING] spaCy model 'en_core_web_sm' not found.")

# ─── Initialize Gemini Client ─────────────────────────────────────────────────
_api_key = os.environ.get("GEMINI_API_KEY")
if not _api_key:
    raise EnvironmentError(
        "\n\n❌  GEMINI_API_KEY not set!\n"
        "   1. Get a free key at: https://aistudio.google.com/app/apikey\n"
        "   2. Create a .env file in the project root:\n"
        "      GEMINI_API_KEY=your_key_here\n"
        "   3. Restart the server.\n"
    )
gemini_client = genai.Client(api_key=_api_key)

# Preferred fast models with fallback hierarchy
GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
]

# ─── Linguistic Constants ─────────────────────────────────────────────────────
FILLER_PATTERNS = [
    r"\bum\b", r"\buh\b", r"\ber\b", r"\bah\b", r"\blike\b",
    r"\bbasically\b", r"\bactually\b", r"\bliterally\b",
    r"\byou know\b", r"\bi mean\b", r"\bsort of\b", r"\bkind of\b",
    r"\bright\b(?=,|$|\s+right\b)"
]

HESITATION_PATTERNS = [
    r"\bi think\b", r"\bi guess\b", r"\bmaybe\b", r"\bperhaps\b",
    r"\bprobably\b", r"\bi('m| am) not sure\b", r"\bnot totally sure\b",
    r"\bmight be\b", r"\bi suppose\b", r"\bkinda\b", r"\bsorta\b"
]

ASSERTIVE_KEYWORDS = [
    "implemented", "engineered", "architected", "designed", "optimized",
    "achieved", "solved", "analyzed", "delivered", "spearheaded",
    "resolved", "scaled", "debugged", "formulated", "established",
    "definitely", "specifically", "demonstrated", "ensured", "prioritized"
]

INTERVIEWER_SYSTEM_PROMPT = """You are an elite principal interviewer and executive career coach.
You evaluate candidate interview answers with extreme accuracy, rigorous technical depth, constructive kindness, and clarity.
Always produce strictly valid JSON matching the exact schema requested, with no markdown fences, no conversational preamble, and no trailing notes."""


# ─── Keyword Extraction with spaCy ───────────────────────────────────────────
def extract_keywords_with_spacy(user_response: str, expected_keywords: List[str]) -> Tuple[List[str], List[str]]:
    """
    Extract and match expected technical keywords and concepts using spaCy lemmatization
    and raw sub-phrase scanning.
    """
    if not expected_keywords:
        return [], []

    raw_lower = user_response.lower()
    user_lemmas = set()

    if nlp is not None:
        doc = nlp(raw_lower)
        user_lemmas = {token.lemma_ for token in doc if not token.is_stop and not token.is_punct}
        # Include noun chunks as phrases
        noun_chunks = {chunk.text.strip().lower() for chunk in doc.noun_chunks}
    else:
        noun_chunks = set()

    matched = []
    missing = []

    for kw in expected_keywords:
        kw_clean = kw.strip()
        kw_lower = kw_clean.lower()

        # Multi-word match: substring or noun chunk
        if " " in kw_lower:
            if kw_lower in raw_lower or kw_lower in noun_chunks:
                matched.append(kw_clean)
            else:
                missing.append(kw_clean)
        else:
            # Single word match: lemma or raw word boundary
            kw_lemma = kw_lower
            if nlp is not None:
                kw_doc = nlp(kw_lower)
                if len(kw_doc) > 0:
                    kw_lemma = kw_doc[0].lemma_

            pattern = r"\b" + re.escape(kw_lower) + r"\b"
            if kw_lower in user_lemmas or kw_lemma in user_lemmas or re.search(pattern, raw_lower):
                matched.append(kw_clean)
            else:
                missing.append(kw_clean)

    return matched, missing


# ─── Filler & Fluency NLP Analysis ────────────────────────────────────────────
def analyze_fluency_and_fillers(text: str) -> Dict[str, Any]:
    """
    Detect filler words, hesitations, word count, sentence count, and compute fluency metrics.
    """
    clean_text = text.strip()
    words = re.findall(r"\b[\w'-]+\b", clean_text)
    total_words = len(words)
    text_lower = clean_text.lower()

    # Detect filler words
    detected_fillers = []
    total_filler_count = 0
    for pat in FILLER_PATTERNS:
        matches = re.findall(pat, text_lower)
        if matches:
            count = len(matches)
            total_filler_count += count
            clean_token = pat.replace(r"\b", "").replace(r"\s+", " ").replace("(?=,|$| right)", "")
            detected_fillers.append({"word": clean_token, "count": count})

    # Detect hesitation phrases
    detected_hesitations = []
    total_hesitation_count = 0
    for pat in HESITATION_PATTERNS:
        matches = re.findall(pat, text_lower)
        if matches:
            count = len(matches)
            total_hesitation_count += count
            detected_hesitations.append(matches[0])

    # Assertive verbs count
    assertive_count = sum(1 for kw in ASSERTIVE_KEYWORDS if re.search(r"\b" + kw + r"\b", text_lower))

    # Sentence count
    if nlp is not None and clean_text:
        doc = nlp(clean_text)
        sentences = list(doc.sents)
        sentence_count = max(len(sentences), 1)
    else:
        sentences = re.split(r"[.!?]+", clean_text)
        sentence_count = max(len([s for s in sentences if s.strip()]), 1)

    avg_sentence_len = round(total_words / sentence_count, 1) if sentence_count else 0
    unique_words = len(set(w.lower() for w in words))
    lexical_diversity = round(unique_words / max(total_words, 1), 2)

    return {
        "word_count": total_words,
        "sentence_count": sentence_count,
        "avg_sentence_len": avg_sentence_len,
        "lexical_diversity": lexical_diversity,
        "filler_count": total_filler_count,
        "fillers_detected": detected_fillers,
        "hesitation_count": total_hesitation_count,
        "hesitations_detected": detected_hesitations,
        "assertive_count": assertive_count,
    }


# ─── Sentiment Analysis ───────────────────────────────────────────────────────
def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment polarity, subjectivity, and delivery tone using TextBlob.
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 2)       # -1.0 to +1.0
    subjectivity = round(blob.sentiment.subjectivity, 2) # 0.0 to 1.0

    # Categorize label
    if polarity >= 0.25:
        label = "Positive & Enthusiastic"
        tone = "Enthusiastic"
    elif polarity >= 0.05:
        label = "Constructive & Professional"
        tone = "Confident"
    elif polarity >= -0.1:
        label = "Objective & Balanced"
        tone = "Analytical"
    else:
        label = "Critical / Hesitant"
        tone = "Cautious"

    # Nuance based on subjectivity
    if subjectivity > 0.6 and polarity >= 0.1:
        tone_description = "Engaging and personal with strong expressive passion."
    elif subjectivity < 0.3:
        tone_description = "Data-driven, precise, and highly professional."
    elif polarity < 0:
        tone_description = "Reflective or cautious; ensure answers frame challenges towards proactive solutions."
    else:
        tone_description = "Clear, professional, and well-balanced communication style."

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "label": label,
        "tone": tone,
        "description": tone_description,
    }


# ─── Confidence Scoring ───────────────────────────────────────────────────────
def calculate_confidence_score(fluency: Dict[str, Any], sentiment: Dict[str, Any], keyword_ratio: float) -> Dict[str, Any]:
    """
    Calculate an objective candidate confidence score (0-100) based on linguistic assertiveness,
    filler word density, answer length, and keyword grasp.
    """
    words = fluency.get("word_count", 0)
    fillers = fluency.get("filler_count", 0)
    hesitations = fluency.get("hesitation_count", 0)
    assertive = fluency.get("assertive_count", 0)

    # Base confidence score
    score = 72.0

    # Adequate response length bonus
    if 45 <= words <= 300:
        score += 8.0
    elif words < 25:
        score -= 15.0  # Too brief
    elif words > 400:
        score -= 5.0   # Rambling

    # Keyword grasp bonus
    score += (keyword_ratio * 12.0)

    # Assertive language bonus
    score += min(assertive * 3.0, 10.0)

    # Filler word penalty (-2.5 points per filler, capped at -20)
    filler_penalty = min(fillers * 2.5, 20.0)
    score -= filler_penalty

    # Hesitation phrase penalty (-3.5 points per phrase, capped at -15)
    hesitation_penalty = min(hesitations * 3.5, 15.0)
    score -= hesitation_penalty

    # Sentiment adjustment
    if sentiment.get("polarity", 0) > 0.15:
        score += 4.0
    elif sentiment.get("polarity", 0) < -0.15:
        score -= 4.0

    final_score = int(max(15, min(98, round(score))))

    if final_score >= 82:
        level = "High"
        advice = "Excellent vocal clarity and authority! You speak with conviction and concise terminology."
    elif final_score >= 65:
        level = "Moderate"
        advice = "Good foundational presence. Try cutting back on filler words and state your conclusions more directly."
    else:
        level = "Needs Conviction"
        advice = "Focus on replacing hedging phrases ('I think', 'maybe') with active declarations ('I designed', 'we solved')."

    return {
        "score": final_score,
        "level": level,
        "filler_count": fillers,
        "hesitation_count": hesitations,
        "advice": advice,
    }


# ─── Speech Pattern & Delivery Analysis ──────────────────────────────────────
def analyze_speech_patterns(
    fluency: Dict[str, Any],
    text: str,
    duration_seconds: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Evaluates speech delivery metrics:
    - Words Per Minute (WPM) cadence
    - Filler word rate (Fillers Per Minute - FPM)
    - Hesitation frequency
    - Delivery energy & assertiveness
    - Actionable vocal coaching recommendations
    """
    word_count = fluency.get("word_count", len(text.split()))
    filler_count = fluency.get("filler_count", 0)
    hesitation_count = fluency.get("hesitation_count", 0)
    assertive_count = fluency.get("assertive_count", 0)

    is_estimated = False
    if duration_seconds is None or duration_seconds <= 0:
        is_estimated = True
        # Standard interview conversational speaking rate is ~135 WPM
        duration_seconds = max(round((word_count / 135.0) * 60, 1), 6.0)

    duration_min = max(duration_seconds / 60.0, 0.08)
    wpm = int(round(word_count / duration_min))

    # Evaluate speaking pace
    if wpm < 105:
        pace_label = "Deliberate / Slow"
        pace_status = "warning"
        pace_advice = f"Your pacing is {wpm} WPM (ideal is 120-160 WPM). Aim to speak with more momentum and vocal energy to keep the interviewer engaged."
    elif 105 <= wpm <= 165:
        pace_label = "Optimal Cadence"
        pace_status = "success"
        pace_advice = f"Outstanding interview pace at {wpm} WPM. Clear, structured, and easy for the interviewer to follow and take notes."
    elif 166 <= wpm <= 190:
        pace_label = "Brisk / Fast"
        pace_status = "warning"
        pace_advice = f"Pacing is on the faster side ({wpm} WPM). Ensure complex system design and technical terms are given adequate pauses."
    else:
        pace_label = "Too Rapid / Rushed"
        pace_status = "danger"
        pace_advice = f"Rapid delivery at {wpm} WPM. Take measured breaths between sentences so key achievements don't sound hurried."

    # Fillers Per Minute (FPM) & density
    fpm = round(filler_count / duration_min, 1)
    filler_density_pct = round((filler_count / max(word_count, 1)) * 100, 1)

    if fpm < 1.5:
        filler_rating = "Pristine"
        filler_status = "success"
    elif fpm <= 4.0:
        filler_rating = "Acceptable"
        filler_status = "info"
    else:
        filler_rating = "Frequent Fillers"
        filler_status = "warning"

    # Delivery Energy Index (0-100)
    energy_score = 74.0
    if 115 <= wpm <= 155:
        energy_score += 10.0
    elif wpm < 95 or wpm > 185:
        energy_score -= 8.0

    energy_score += min(assertive_count * 4.0, 15.0)
    energy_score -= min(hesitation_count * 3.0, 15.0)
    energy_score -= min(filler_count * 2.0, 12.0)
    energy_score = int(max(20, min(98, round(energy_score))))

    if energy_score >= 82:
        energy_level = "High Conviction & Authority"
    elif energy_score >= 68:
        energy_level = "Steady & Professional"
    else:
        energy_level = "Tentative / Needs Conviction"

    return {
        "duration_seconds": round(duration_seconds, 1),
        "is_estimated_duration": is_estimated,
        "wpm": wpm,
        "pace_label": pace_label,
        "pace_status": pace_status,
        "pace_advice": pace_advice,
        "vocal_advice": pace_advice,
        "fpm": fpm,
        "fillers_per_minute": fpm,
        "filler_density_pct": filler_density_pct,
        "filler_rating": filler_rating,
        "filler_status": filler_status,
        "filler_count": filler_count,
        "energy_score": energy_score,
        "delivery_energy_score": energy_score,
        "energy_level": energy_level,
        "hesitation_count": hesitation_count,
        "assertive_count": assertive_count,
    }


# ─── STAR Framework NLP Analysis ─────────────────────────────────────────────
def analyze_star_framework(text: str, domain: str = "") -> Dict[str, Any]:
    """
    Evaluates alignment with the STAR (Situation, Task, Action, Result) response model.
    Crucial for behavioral, leadership, and structured technical scenario responses.
    """
    text_lower = text.lower()

    # Situation cues
    s_cues = [
        "when i was", "at my previous", "in my last role", "in our team",
        "our company was", "we faced", "we had an issue", "the situation was",
        "context was", "at company", "during the project", "in our architecture",
        "in a project where", "our system was", "at the time"
    ]
    situation_found = any(cue in text_lower for cue in s_cues)

    # Task cues
    t_cues = [
        "my task was", "my responsibility", "the goal was", "i was responsible",
        "i was tasked with", "the challenge was", "we needed to", "the objective was",
        "required to", "had to solve", "had to deliver"
    ]
    task_found = any(cue in text_lower for cue in t_cues)

    # Action cues
    a_cues = [
        "i implemented", "i designed", "i built", "i architected", "i decided",
        "i created", "i engineered", "i developed", "i refactored", "i introduced",
        "i led", "i optimized", "i wrote", "we implemented", "we architected"
    ]
    action_found = any(cue in text_lower for cue in a_cues)

    # Result cues
    r_cues = [
        "as a result", "resulting in", "the outcome", "we achieved", "reduced by",
        "increased by", "improved by", "saved", "saving", "successfully delivered",
        "which allowed us", "this reduced", "this improved", "this resulted in",
        "which helped", "impact was"
    ]
    result_found = any(cue in text_lower for cue in r_cues)

    star_components = {
        "situation": {"detected": situation_found, "label": "Situation / Context"},
        "task":      {"detected": task_found,      "label": "Task / Objective"},
        "action":    {"detected": action_found,    "label": "Action / Execution"},
        "result":    {"detected": result_found,    "label": "Result / Impact"}
    }

    count = sum(1 for v in star_components.values() if v["detected"])
    star_pct = round((count / 4.0) * 100)

    if count == 4:
        feedback = "Exceptional STAR alignment: Context, Objective, Concrete Action, and Measurable Outcome all present."
    elif count == 3:
        missing = [k.capitalize() for k, v in star_components.items() if not v["detected"]]
        feedback = f"Strong structure. Adding explicit emphasis on {', '.join(missing)} will make this an elite response."
    elif count >= 1:
        detected = [k.capitalize() for k, v in star_components.items() if v["detected"]]
        feedback = f"Partial STAR adherence ({', '.join(detected)} detected). Structure the story step-by-step from context to result."
    else:
        feedback = "Consider framing this scenario with the STAR method (Situation -> Task -> Action -> Measurable Result)."

    detected_map = {
        "s": star_components["situation"]["detected"],
        "t": star_components["task"]["detected"],
        "a": star_components["action"]["detected"],
        "r": star_components["result"]["detected"]
    }

    return {
        "score": star_pct,
        "star_score": star_pct,
        "components": star_components,
        "detected": detected_map,
        "detected_count": count,
        "feedback": feedback
    }


# ─── Quantitative Impact & Metrics NLP ───────────────────────────────────────
def analyze_quantitative_impact(text: str) -> Dict[str, Any]:
    """
    Detects concrete metrics, scale indicators, percentages, and financial impact.
    Top engineering and product interview answers always back claims with data.
    """
    text_lower = text.lower()
    
    metric_patterns = [
        r"\b\d+(?:\.\d+)?%\b",
        r"\b\d+x\b",
        r"\b\d+[\d,]*\s*(?:ms|milliseconds|seconds|mins|hours)\b",
        r"\b\$\s*\d+[\d,]*\s*(?:k|m|million|thousand|billion)?\b",
        r"\b\d+[\d,]*\s*(?:users|qps|rps|tps|req/s|requests|events|nodes|pods|services|endpoints|db|records)\b",
        r"\b\d+[\d,]*\s*(?:gb|tb|mb|pb)\b"
    ]
    
    detected_metrics = []
    for pat in metric_patterns:
        matches = re.findall(pat, text_lower)
        for m in matches:
            if m not in detected_metrics:
                detected_metrics.append(m)

    has_metrics = len(detected_metrics) > 0
    impact_score = min(len(detected_metrics) * 25, 100)

    if len(detected_metrics) >= 2:
        impact_advice = f"Superb quantitative substantiation! You backed your claims with clear metrics ({', '.join(detected_metrics[:3])})."
    elif len(detected_metrics) == 1:
        impact_advice = f"Good data grounding ({detected_metrics[0]}). Try reinforcing with another metric like latency or cost."
    else:
        impact_advice = "No explicit numbers or percentages detected. Top candidates quantify results (e.g., 'reduced latency by 35%', 'scaled to 50k QPS')."

    return {
        "has_metrics": has_metrics,
        "has_quantified_impact": has_metrics,
        "count": len(detected_metrics),
        "metric_count": len(detected_metrics),
        "metrics": detected_metrics,
        "score": impact_score,
        "advice": impact_advice
    }


# ─── Response Relevance & Prompt Alignment ────────────────────────────────────
def analyze_relevance_and_quality(
    user_response: str,
    question_text: str,
    expected_keywords: List[str],
    matched_keywords: List[str]
) -> Dict[str, Any]:
    """
    Evaluates response relevance and prompt alignment:
    - Overlap with core prompt entities
    - Directness vs wandering off-topic
    - Keyword coverage ratio
    """
    q_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", question_text.lower()))
    r_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", user_response.lower()))

    stop_words = {"what", "when", "where", "which", "would", "could", "should", "your", "explain", "describe", "difference", "between", "applied"}
    substantive_q = q_words - stop_words

    overlap = substantive_q.intersection(r_words)
    overlap_ratio = len(overlap) / max(len(substantive_q), 1)

    kw_ratio = (len(matched_keywords) / max(len(expected_keywords), 1)) if expected_keywords else 0.5
    
    relevance_score = int(round((overlap_ratio * 0.4 + kw_ratio * 0.6) * 100))
    relevance_score = max(25, min(99, relevance_score))

    if relevance_score >= 80:
        label = "Direct & Highly Relevant"
        desc = "Your answer directly tackles the heart of the interviewer's question without drifting."
    elif relevance_score >= 60:
        label = "Relevant with Good Focus"
        desc = "Answer is on-topic. Sharpen the connection to the core question prompt."
    else:
        label = "Partially Tangential"
        desc = "Answer addresses some points but drifts away from the primary problem statement."

    return {
        "score": relevance_score,
        "label": label,
        "description": desc,
        "prompt_terms_addressed": list(overlap)[:6]
    }


# ─── Multi-Dimensional Score Calculation ──────────────────────────────────────
def calculate_composite_score(
    keyword_match_ratio: float,
    technical_raw: int,
    fluency: Dict[str, Any],
    confidence_score: int,
) -> Dict[str, Any]:
    """
    Computes a transparent 4-part score breakdown:
    1. Keyword & Concept Coverage: 25%
    2. Technical Depth & Substance: 35%
    3. Communication Structure & Conciseness: 20%
    4. Delivery & Confidence: 20%
    Total: 100%
    """
    # 1. Keyword coverage (0-25)
    kw_score = round(keyword_match_ratio * 25.0, 1)

    # 2. Technical depth (0-35)
    tech_score = round((technical_raw / 100.0) * 35.0, 1)

    # 3. Communication structure (0-20)
    words = fluency.get("word_count", 0)
    fillers = fluency.get("filler_count", 0)
    comm_base = 15.0
    if 40 <= words <= 250:
        comm_base += 4.0
    elif words < 20:
        comm_base -= 8.0
    comm_base -= min(fillers * 1.0, 5.0)
    comm_score = round(max(3.0, min(20.0, comm_base)), 1)

    # 4. Confidence & Delivery (0-20)
    conf_score = round((confidence_score / 100.0) * 20.0, 1)

    total = int(round(kw_score + tech_score + comm_score + conf_score))
    total = max(5, min(100, total))

    if total >= 85:
        grade = "Excellent"
    elif total >= 70:
        grade = "Good"
    elif total >= 50:
        grade = "Fair"
    else:
        grade = "Needs Improvement"

    return {
        "total": total,
        "grade": grade,
        "breakdown": {
            "keyword_coverage": {"score": kw_score, "max": 25, "pct": round((kw_score / 25.0) * 100)},
            "technical_depth": {"score": tech_score, "max": 35, "pct": round((tech_score / 35.0) * 100)},
            "communication_structure": {"score": comm_score, "max": 20, "pct": round((comm_score / 20.0) * 100)},
            "confidence_delivery": {"score": conf_score, "max": 20, "pct": round((conf_score / 20.0) * 100)},
        }
    }


# ─── Gemini LLM Evaluation ───────────────────────────────────────────────────
def call_gemini_with_fallback(prompt: str, system_instruction: str = INTERVIEWER_SYSTEM_PROMPT) -> str:
    """
    Attempts to call Gemini across available models with automatic fallback.
    """
    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                top_p=0.9,
            )
            response = gemini_client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            last_error = e
            print(f"[INFO] Gemini model '{model_name}' unavailable ({e}), trying next...")
            continue

    raise RuntimeError(f"All Gemini models exhausted. Last error: {last_error}")


def evaluate_response_with_gemini(
    question_text: str,
    user_response: str,
    expected_keywords: List[str],
    domain: str,
    previous_interaction_id: Optional[str] = None,
    duration_seconds: Optional[float] = None
) -> Dict[str, Any]:
    """
    Complete NLP Evaluation Pipeline:
    1. spaCy keyword extraction (matched / missing)
    2. Fluency & filler analysis
    3. Sentiment analysis (TextBlob)
    4. Confidence scoring
    5. Speech pattern & delivery analysis (WPM, FPM, pacing, cadence)
    6. STAR framework alignment analysis
    7. Quantitative impact analysis
    8. Prompt relevance & quality analysis
    9. Gemini LLM assessment with multi-model fallback
    10. Intelligent local fallback if API is overloaded
    """
    # 1. spaCy Keyword Analysis
    matched_keywords, missing_keywords = extract_keywords_with_spacy(user_response, expected_keywords)
    keyword_ratio = (len(matched_keywords) / max(len(expected_keywords), 1)) if expected_keywords else 0.5

    # 2. Fluency & Fillers
    fluency = analyze_fluency_and_fillers(user_response)

    # 3. Sentiment Analysis
    sentiment = analyze_sentiment(user_response)

    # 4. Confidence Score
    confidence = calculate_confidence_score(fluency, sentiment, keyword_ratio)

    # 5. Speech Pattern & Delivery Analysis
    speech_analysis = analyze_speech_patterns(fluency, user_response, duration_seconds=duration_seconds)

    # 6. STAR Framework Analysis
    star_analysis = analyze_star_framework(user_response, domain=domain)

    # 7. Quantitative Impact Analysis
    impact_analysis = analyze_quantitative_impact(user_response)

    # 8. Prompt Relevance & Quality Analysis
    relevance = analyze_relevance_and_quality(user_response, question_text, expected_keywords, matched_keywords)

    prompt = f"""You are evaluating an interview answer for a candidate practicing "{domain}".

Question: "{question_text}"
Candidate Answer: "{user_response}"

spaCy & NLP Analysis Metrics:
- Matched Technical Keywords: {json.dumps(matched_keywords)}
- Missing Expected Concepts: {json.dumps(missing_keywords)}
- Word Count: {fluency['word_count']} words | Speaking Pace: {speech_analysis['wpm']} WPM ({speech_analysis['pace_label']})
- Filler Words Count: {fluency['filler_count']} ({speech_analysis['fpm']} FPM)
- Sentiment Tone: {sentiment['tone']} ({sentiment['label']})
- Delivery Energy: {speech_analysis['energy_level']} ({speech_analysis['energy_score']}/100)
- STAR Framework Score: {star_analysis['score']}% ({star_analysis['feedback']})
- Quantitative Data Grounding: {'Yes (' + ', '.join(impact_analysis['metrics']) + ')' if impact_analysis['has_metrics'] else 'None detected'}
- Prompt Relevance Index: {relevance['score']}% ({relevance['label']})

Evaluate technical accuracy, problem-solving reasoning, completeness, and clarity.
Provide:
1. "technical_depth_raw": integer 0-100 reflecting pure technical accuracy and depth.
2. "feedback": 2-3 concise, constructive sentences highlighting what was strong and what critical points were missed.
3. "strengths": 2-3 specific bullet points citing parts of their answer done well.
4. "improvements": 2-3 actionable, concrete improvement recommendations for this specific question.
5. "recommendations": 2-3 specific study concepts or industry best-practice patterns to review.
6. "model_answer": A pristine, benchmark 2-4 sentence ideal answer to this exact question.
7. "follow_up": A natural, probing follow-up question an interviewer would ask next.

Respond ONLY with a valid JSON object matching this exact schema:
{{
    "technical_depth_raw": <integer 0-100>,
    "feedback": "<executive summary feedback>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "improvements": ["<actionable recommendation 1>", "<actionable recommendation 2>"],
    "recommendations": ["<concept/pattern to study 1>", "<concept/pattern to study 2>"],
    "model_answer": "<ideal benchmark answer>",
    "follow_up": "<probing follow-up question>"
}}"""

    try:
        raw_output = call_gemini_with_fallback(prompt)

        # Clean JSON fences if any
        clean_json = raw_output
        if "```" in clean_json:
            matches = re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", clean_json)
            if matches:
                clean_json = matches[0].strip()

        parsed = json.loads(clean_json)
        tech_raw = int(parsed.get("technical_depth_raw", 70))

        # Composite score calculation
        scoring = calculate_composite_score(keyword_ratio, tech_raw, fluency, confidence["score"])

        return {
            "score": scoring["total"],
            "grade": scoring["grade"],
            "score_breakdown": scoring["breakdown"],
            "matched": matched_keywords,
            "missing": missing_keywords,
            "feedback": parsed.get("feedback", "Good effort. Review the technical points below."),
            "strengths": parsed.get("strengths", ["Answer addressed the prompt."]),
            "improvements": parsed.get("improvements", ["Expand on technical depth."]),
            "recommendations": parsed.get("recommendations", ["Review foundational design principles."]),
            "model_answer": parsed.get("model_answer", "A comprehensive answer incorporates the core keywords and practical trade-offs."),
            "follow_up": parsed.get("follow_up", "Can you explain how this behaves in a high-scale production setting?"),
            "sentiment": sentiment,
            "confidence": confidence,
            "fluency": fluency,
            "speech_analysis": speech_analysis,
            "star_analysis": star_analysis,
            "impact_analysis": impact_analysis,
            "relevance": relevance,
            "engine": "gemini-ai",
        }

    except Exception as e:
        print(f"[WARN] Gemini evaluation failed or overloaded ({e}). Using intelligent local NLP engine.")
        return _local_nlp_fallback_evaluation(
            question_text=question_text,
            user_response=user_response,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
            keyword_ratio=keyword_ratio,
            fluency=fluency,
            sentiment=sentiment,
            confidence=confidence,
            speech_analysis=speech_analysis,
            star_analysis=star_analysis,
            impact_analysis=impact_analysis,
            relevance=relevance,
            domain=domain,
        )


def _local_nlp_fallback_evaluation(
    question_text: str,
    user_response: str,
    matched_keywords: List[str],
    missing_keywords: List[str],
    keyword_ratio: float,
    fluency: Dict[str, Any],
    sentiment: Dict[str, Any],
    confidence: Dict[str, Any],
    speech_analysis: Dict[str, Any],
    star_analysis: Dict[str, Any],
    impact_analysis: Dict[str, Any],
    relevance: Dict[str, Any],
    domain: str,
) -> Dict[str, Any]:
    """
    Intelligent local NLP evaluation fallback when the Gemini API is offline or busy.
    Ensures 100% application reliability.
    """
    words = fluency["word_count"]

    # Estimate technical depth raw score from keyword match ratio + vocabulary length
    tech_base = keyword_ratio * 75.0
    if words >= 40:
        tech_base += 15.0
    elif words >= 20:
        tech_base += 8.0
    tech_raw = int(min(95, max(20, round(tech_base))))

    scoring = calculate_composite_score(keyword_ratio, tech_raw, fluency, confidence["score"])

    # Construct dynamic strengths
    strengths = []
    if matched_keywords:
        strengths.append(f"Successfully incorporated key domain concepts: {', '.join(matched_keywords[:3])}.")
    if words >= 45:
        strengths.append("Provided a well-developed explanation with adequate detail.")
    if confidence["score"] >= 70:
        strengths.append(f"Maintained an authoritative, {sentiment['tone'].lower()} delivery.")
    if impact_analysis.get("has_metrics"):
        strengths.append(f"Substantiated answer with quantitative metrics ({', '.join(impact_analysis['metrics'][:2])}).")
    if not strengths:
        strengths.append("Engaged with the question and stated an initial solution.")

    # Construct dynamic improvement recommendations
    improvements = []
    if missing_keywords:
        improvements.append(f"Incorporate missing core concepts such as: {', '.join(missing_keywords[:3])}.")
    if fluency["filler_count"] > 2:
        improvements.append(f"Reduce filler words (detected {fluency['filler_count']} instances like '{fluency['fillers_detected'][0]['word']}').")
    if not impact_analysis.get("has_metrics"):
        improvements.append("Quantify outcomes with numbers or scale metrics (e.g. latency reduction, request volume).")
    if words < 35:
        improvements.append("Elaborate further with a concrete real-world implementation example or trade-off analysis.")
    if not improvements:
        improvements.append("Discuss edge cases and performance trade-offs to demonstrate senior-level mastery.")

    recommendations = [
        f"Brush up on {domain.replace('_', ' ')} industry best practices and architecture patterns.",
        "Practice structuring responses using the STAR method (Situation, Task, Action, Result).",
    ]

    return {
        "score": scoring["total"],
        "grade": scoring["grade"],
        "score_breakdown": scoring["breakdown"],
        "matched": matched_keywords,
        "missing": missing_keywords,
        "feedback": f"Your response demonstrated good familiarity with the topic. You covered {len(matched_keywords)} out of {len(matched_keywords)+len(missing_keywords)} key concepts. Addressing the missing technical points will elevate your score.",
        "strengths": strengths,
        "improvements": improvements,
        "recommendations": recommendations,
        "model_answer": "An exemplary response clearly defines the foundational concept, outlines architectural trade-offs, and illustrates practical experience with a concise metric-driven example.",
        "follow_up": f"How would you optimize this approach if your system had to handle 10x the current load?",
        "sentiment": sentiment,
        "confidence": confidence,
        "fluency": fluency,
        "speech_analysis": speech_analysis,
        "star_analysis": star_analysis,
        "impact_analysis": impact_analysis,
        "relevance": relevance,
        "engine": "local-nlp",
    }


# ─── Streamed Verbal Reaction ────────────────────────────────────────────────
def get_streamed_feedback(
    question_text: str,
    user_response: str,
    domain: str,
):
    """
    Stream a human-like 2-sentence conversational interviewer reaction.
    Generator yields SSE string events.
    """
    prompt = f"""As a technical interviewer for the domain "{domain}", give a brief 2-sentence warm but direct reaction to this candidate's answer.
Question: "{question_text}"
Candidate Answer: "{user_response}"
Respond in plain conversational text only."""

    for model_name in GEMINI_MODELS:
        try:
            for chunk in gemini_client.models.generate_content_stream(
                model=model_name,
                contents=prompt,
            ):
                if chunk.text:
                    yield f"data: {json.dumps({'text': chunk.text})}\n\n"
            yield "data: [DONE]\n\n"
            return
        except Exception as e:
            print(f"[INFO] Streaming failed on model '{model_name}': {e}")
            continue

    # Fallback reaction if streaming unavailable
    reaction = "Thank you for sharing your thoughts on this question. Let's analyze your response in detail below."
    yield f"data: {json.dumps({'text': reaction})}\n\n"
    yield "data: [DONE]\n\n"


# ─── Audio Transcription (Speech-to-Text via Gemini) ─────────────────────────
def transcribe_audio_with_gemini(audio_bytes: bytes, mime_type: str = "audio/webm") -> str:
    """
    Transcribes audio bytes into text using Gemini multimodal capabilities.
    """
    audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)
    prompt = "Transcribe the following interview answer verbatim into clear English text. Do not add commentary or punctuation that was not spoken."

    for model_name in GEMINI_MODELS:
        try:
            response = gemini_client.models.generate_content(
                model=model_name,
                contents=[audio_part, prompt],
            )
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"[INFO] Audio transcription with {model_name} failed: {e}")
            continue

    raise RuntimeError("Audio transcription unavailable on Gemini models.")


def analyze_audio_and_transcribe(audio_bytes: bytes, mime_type: str = "audio/webm") -> Dict[str, Any]:
    """
    Transcribes uploaded audio and computes speech delivery metrics (WPM, fillers, pacing).
    """
    duration = None
    try:
        if "wav" in mime_type.lower() or audio_bytes[:4] == b"RIFF":
            import wave
            import io
            with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                if rate > 0:
                    duration = round(frames / float(rate), 2)
    except Exception:
        pass

    transcription = transcribe_audio_with_gemini(audio_bytes, mime_type=mime_type)
    fluency = analyze_fluency_and_fillers(transcription)
    speech_analysis = analyze_speech_patterns(fluency, transcription, duration_seconds=duration)

    return {
        "text": transcription,
        "duration_seconds": speech_analysis["duration_seconds"],
        "speech_analysis": speech_analysis,
        "fluency": fluency,
    }
