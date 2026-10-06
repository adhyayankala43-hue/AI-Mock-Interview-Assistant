from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import datetime
import os
import random
from typing import Dict, List, Any

from nlp_engine import (
    evaluate_response_with_gemini,
    get_streamed_feedback,
    transcribe_audio_with_gemini,
    analyze_audio_and_transcribe,
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max for audio uploads

# ─── Load questions DB ────────────────────────────────────────────────────────
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions.json')
HISTORY_FILE   = os.path.join(os.path.dirname(__file__), 'history.json')

DOMAIN_LABELS = {
    "software_engineering": "Software Engineering",
    "data_science": "Data Science",
    "product_management": "Product Management",
    "behavioral": "Behavioral",
    "python_developer": "Python Developer",
    "forensic_science": "Forensic Science",
}

def load_questions_db() -> Dict[str, Any]:
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load questions: {e}")
        return {}

def save_questions_db(db: Dict[str, Any]):
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2)

# ─── Helper: load/save history ────────────────────────────────────────────────
def load_history() -> List[Dict[str, Any]]:
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_to_history(record: Dict[str, Any]):
    history = load_history()
    history.append(record)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

# ─── Web Page Routes ──────────────────────────────────────────────────────────
@app.route('/')
def index():
    questions_db = load_questions_db()
    domains = [
        {"key": k, "label": DOMAIN_LABELS.get(k, k.replace("_", " ").title())}
        for k in questions_db.keys()
    ]
    return render_template('index.html', domains=domains)

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/history')
def history_page():
    return render_template('history.html')

# ─── API: Questions ───────────────────────────────────────────────────────────
@app.route('/api/questions/<domain>')
def get_questions(domain: str):
    questions_db = load_questions_db()
    if domain not in questions_db:
        return jsonify({"error": "Domain not found"}), 404

    questions = questions_db[domain]
    difficulty = request.args.get('difficulty')
    if difficulty and difficulty.lower() != 'all':
        questions = [q for q in questions if q.get('difficulty', '').lower() == difficulty.lower()]

    return jsonify(questions)

@app.route('/api/questions/random', methods=['GET'])
def get_random_question():
    questions_db = load_questions_db()
    domain = request.args.get('domain')
    if domain and domain in questions_db:
        domain_list = [(domain, q) for q in questions_db[domain]]
    else:
        domain_list = [(d, q) for d, q_list in questions_db.items() for q in q_list]

    if not domain_list:
        return jsonify({"error": "No questions available"}), 404

    chosen_domain, question = random.choice(domain_list)
    return jsonify({
        "domain": chosen_domain,
        "domain_label": DOMAIN_LABELS.get(chosen_domain, chosen_domain.title()),
        "question": question
    })

@app.route('/api/questions/add', methods=['POST'])
def add_custom_question():
    data = request.json or {}
    domain = data.get('domain', 'software_engineering')
    text = data.get('text', '').strip()
    keywords = [k.strip() for k in data.get('keywords', []) if k.strip()]
    difficulty = data.get('difficulty', 'Medium')
    tips = data.get('tips', 'Be clear, concise, and structured.')
    model_answer = data.get('model_answer', 'A strong answer covers core concepts and trade-offs.')

    if not text:
        return jsonify({"error": "Question text is required"}), 400

    questions_db = load_questions_db()
    if domain not in questions_db:
        questions_db[domain] = []

    # Deduplicate: if an identical question already exists in this domain, return it without appending duplicates
    existing = next((q for q in questions_db[domain] if q.get('text', '').strip().lower() == text.lower()), None)
    if existing:
        return jsonify({"success": True, "question": existing, "duplicate": True})

    q_id = f"{domain[:2]}_custom_{len(questions_db[domain]) + 1}"
    new_q = {
        "id": q_id,
        "text": text,
        "difficulty": difficulty,
        "keywords": keywords or ["overview", "concept", "solution"],
        "tips": tips,
        "model_answer": model_answer
    }
    questions_db[domain].append(new_q)
    save_questions_db(questions_db)

    return jsonify({"success": True, "question": new_q})

# ─── API: Evaluate Response ───────────────────────────────────────────────────
@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json or {}
    user_response      = data.get('response', '').strip()
    question_id        = data.get('question_id', '')
    question_text      = data.get('question_text', '')
    expected_keywords  = data.get('expected_keywords', [])
    domain             = data.get('domain', 'software_engineering')
    prev_interaction   = data.get('previous_interaction_id')
    duration_seconds   = data.get('duration_seconds')

    if duration_seconds is not None:
        try:
            duration_seconds = float(duration_seconds)
        except (ValueError, TypeError):
            duration_seconds = None

    if not user_response:
        return jsonify({"error": "Candidate response cannot be empty"}), 400

    result = evaluate_response_with_gemini(
        question_text=question_text,
        user_response=user_response,
        expected_keywords=expected_keywords,
        domain=DOMAIN_LABELS.get(domain, domain),
        previous_interaction_id=prev_interaction,
        duration_seconds=duration_seconds,
    )

    # Ensure impact_analysis aliases are present
    if "impact_analysis" in result and isinstance(result["impact_analysis"], dict):
        result["impact_analysis"]["has_quantified_impact"] = result["impact_analysis"].get("has_quantified_impact", result["impact_analysis"].get("has_metrics", False))
        result["impact_analysis"]["metric_count"] = result["impact_analysis"].get("metric_count", result["impact_analysis"].get("count", 0))

    # Persist rich session record to history
    record = {
        "id": f"sess_{int(datetime.datetime.now().timestamp()*1000)}",
        "timestamp": datetime.datetime.now().isoformat(),
        "domain": domain,
        "domain_label": DOMAIN_LABELS.get(domain, domain.replace('_', ' ').title()),
        "question_id": question_id,
        "question": question_text,
        "response": user_response,
        "score": result.get("score", 0),
        "grade": result.get("grade", "N/A"),
        "score_breakdown": result.get("score_breakdown", {}),
        "sentiment": result.get("sentiment", {}),
        "confidence": result.get("confidence", {}),
        "speech_analysis": result.get("speech_analysis", {}),
        "star_analysis": result.get("star_analysis", {}),
        "impact_analysis": result.get("impact_analysis", {}),
        "relevance": result.get("relevance", {}),
        "duration_seconds": result.get("speech_analysis", {}).get("duration_seconds", 0),
        "wpm": result.get("speech_analysis", {}).get("wpm", 0),
        "feedback": result.get("feedback", ""),
        "strengths": result.get("strengths", []),
        "improvements": result.get("improvements", []),
        "recommendations": result.get("recommendations", []),
        "model_answer": result.get("model_answer", ""),
        "follow_up": result.get("follow_up", ""),
        "matched": result.get("matched", []),
        "missing": result.get("missing", []),
        "word_count": result.get("fluency", {}).get("word_count", len(user_response.split())),
        "engine": result.get("engine", "gemini-ai")
    }
    save_to_history(record)

    return jsonify(result)

# ─── API: Stream Verbal Feedback (SSE) ────────────────────────────────────────
@app.route('/api/stream_feedback', methods=['POST'])
def stream_feedback():
    data          = request.json or {}
    question_text = data.get('question_text', '')
    user_response = data.get('response', '')
    domain        = data.get('domain', 'software_engineering')

    return Response(
        stream_with_context(
            get_streamed_feedback(
                question_text=question_text,
                user_response=user_response,
                domain=DOMAIN_LABELS.get(domain, domain)
            )
        ),
        mimetype='text/event-stream'
    )

# ─── API: Audio Speech-to-Text Transcription ──────────────────────────────────
@app.route('/api/transcribe_audio', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided in request"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    mime_type = audio_file.content_type or 'audio/webm'
    audio_bytes = audio_file.read()

    if not audio_bytes:
        return jsonify({"error": "Audio file is empty"}), 400

    try:
        audio_result = analyze_audio_and_transcribe(audio_bytes, mime_type=mime_type)
        return jsonify({
            "success": True,
            "text": audio_result["text"],
            "duration_seconds": audio_result["duration_seconds"],
            "speech_analysis": audio_result["speech_analysis"],
        })
    except Exception as e:
        print(f"[ERROR] Audio transcription failed: {e}")
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500

# ─── API: History Management ──────────────────────────────────────────────────
@app.route('/api/history')
def get_history():
    history = load_history()
    domain_filter = request.args.get('domain')
    search_q = request.args.get('q', '').lower().strip()

    filtered = history
    if domain_filter and domain_filter != 'all':
        filtered = [h for h in filtered if h.get('domain') == domain_filter]
    if search_q:
        filtered = [
            h for h in filtered
            if search_q in h.get('question', '').lower()
            or search_q in h.get('response', '').lower()
            or search_q in h.get('feedback', '').lower()
        ]

    # Return newest first, capped at 100 entries
    return jsonify(list(reversed(filtered))[:100])

@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)
    return jsonify({"success": True})

@app.route('/api/history/export')
def export_history():
    history = load_history()
    return Response(
        json.dumps(history, indent=2),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=interviewai_history.json'}
    )

# ─── API: Dashboard Stats ─────────────────────────────────────────────────────
@app.route('/api/dashboard/stats')
def get_dashboard_stats():
    history = load_history()
    if not history:
        return jsonify({
            "total_answers": 0,
            "avg_score": 0,
            "best_score": 0,
            "avg_confidence": 0,
            "avg_wpm": 0,
            "avg_fpm": 0,
            "avg_star_score": 0,
            "readiness_index": 0,
            "domains_mastery": {},
            "trends": [],
            "skill_breakdown": {
                "keyword_coverage": 0,
                "technical_depth": 0,
                "communication_structure": 0,
                "confidence_delivery": 0
            },
            "sentiment_counts": {},
            "common_strengths": [],
            "common_improvements": [],
            "recent_activity": []
        })

    scores = [h.get('score', 0) for h in history if isinstance(h.get('score'), (int, float))]
    avg_score = round(sum(scores) / len(scores)) if scores else 0
    best_score = max(scores) if scores else 0

    # Confidences
    confidences = [
        h.get('confidence', {}).get('score', 70)
        for h in history
        if isinstance(h.get('confidence', {}), dict) and 'score' in h.get('confidence', {})
    ]
    avg_confidence = round(sum(confidences) / len(confidences)) if confidences else 70

    # Domain mastery
    domain_data: Dict[str, Dict[str, Any]] = {}
    for h in history:
        d = h.get('domain', 'general')
        if d not in domain_data:
            domain_data[d] = {
                "name": DOMAIN_LABELS.get(d, d.replace('_', ' ').title()),
                "count": 0,
                "scores": [],
                "best": 0
            }
        sc = h.get('score', 0)
        domain_data[d]["count"] += 1
        domain_data[d]["scores"].append(sc)
        if sc > domain_data[d]["best"]:
            domain_data[d]["best"] = sc

    domains_mastery = {}
    for d, info in domain_data.items():
        domains_mastery[d] = {
            "name": info["name"],
            "count": info["count"],
            "avg": round(sum(info["scores"]) / len(info["scores"])),
            "best": info["best"]
        }

    # Readiness Index Calculation (0-100)
    # Combines average score (50%), domain diversity (25%), and session volume consistency (25%)
    diversity_factor = min(len(domains_mastery) / 4.0, 1.0) * 25.0
    volume_factor = min(len(history) / 10.0, 1.0) * 25.0
    score_factor = (avg_score / 100.0) * 50.0
    readiness_index = int(round(score_factor + diversity_factor + volume_factor))
    readiness_index = max(10, min(99, readiness_index))

    # Trend line (chronological order)
    trends = []
    for h in history[-20:]:  # last 20 sessions
        ts = h.get('timestamp', '')
        date_str = ts[:10] if len(ts) >= 10 else "Practice"
        trends.append({
            "date": date_str,
            "score": h.get('score', 0),
            "confidence": h.get('confidence', {}).get('score', 70) if isinstance(h.get('confidence'), dict) else 70,
            "domain": DOMAIN_LABELS.get(h.get('domain'), h.get('domain'))
        })

    # Skill breakdown averages (percentages)
    breakdowns = [h.get('score_breakdown', {}) for h in history if isinstance(h.get('score_breakdown'), dict)]
    skill_breakdown = {
        "keyword_coverage": 70,
        "technical_depth": 70,
        "communication_structure": 75,
        "confidence_delivery": 70
    }
    if breakdowns:
        kw_pcts = [b.get('keyword_coverage', {}).get('pct', 70) for b in breakdowns if 'keyword_coverage' in b]
        tech_pcts = [b.get('technical_depth', {}).get('pct', 70) for b in breakdowns if 'technical_depth' in b]
        comm_pcts = [b.get('communication_structure', {}).get('pct', 75) for b in breakdowns if 'communication_structure' in b]
        conf_pcts = [b.get('confidence_delivery', {}).get('pct', 70) for b in breakdowns if 'confidence_delivery' in b]

        if kw_pcts: skill_breakdown["keyword_coverage"] = round(sum(kw_pcts) / len(kw_pcts))
        if tech_pcts: skill_breakdown["technical_depth"] = round(sum(tech_pcts) / len(tech_pcts))
        if comm_pcts: skill_breakdown["communication_structure"] = round(sum(comm_pcts) / len(comm_pcts))
        if conf_pcts: skill_breakdown["confidence_delivery"] = round(sum(conf_pcts) / len(conf_pcts))

    # Sentiment distribution
    sentiment_counts: Dict[str, int] = {}
    for h in history:
        tone = h.get('sentiment', {}).get('tone', 'Neutral') if isinstance(h.get('sentiment'), dict) else 'Neutral'
        sentiment_counts[tone] = sentiment_counts.get(tone, 0) + 1

    # Speech delivery pacing metrics (WPM and FPM)
    wpms = [
        h.get('speech_analysis', {}).get('wpm', h.get('wpm', 0))
        for h in history
        if (isinstance(h.get('speech_analysis'), dict) and h.get('speech_analysis', {}).get('wpm'))
        or (isinstance(h.get('wpm'), (int, float)) and h.get('wpm', 0) > 0)
    ]
    avg_wpm = round(sum(wpms) / len(wpms)) if wpms else 135

    fpms = [
        h.get('speech_analysis', {}).get('fpm', 0)
        for h in history
        if isinstance(h.get('speech_analysis'), dict) and 'fpm' in h.get('speech_analysis')
    ]
    avg_fpm = round(sum(fpms) / len(fpms), 1) if fpms else 1.2

    # STAR compliance average
    star_scores = [
        h.get('star_analysis', {}).get('score', 65)
        for h in history
        if isinstance(h.get('star_analysis'), dict) and 'score' in h.get('star_analysis')
    ]
    avg_star_score = round(sum(star_scores) / len(star_scores)) if star_scores else 70

    # Readiness Tier
    if readiness_index >= 85:
        readiness_tier = "Staff / Principal Caliber"
        tier_color = "#10b981"
        next_milestone = "Peak Mastery Achieved"
    elif readiness_index >= 70:
        readiness_tier = "Senior Engineer Ready"
        tier_color = "#6366f1"
        next_milestone = "85% for Staff Caliber"
    elif readiness_index >= 50:
        readiness_tier = "Mid-Level Competitive"
        tier_color = "#06b6d4"
        next_milestone = "70% for Senior Caliber"
    else:
        readiness_tier = "Foundational Preparation"
        tier_color = "#f59e0b"
        next_milestone = "50% for Mid-Level Benchmark"

    # Aggregated common strengths and improvements
    strengths_all = []
    improvements_all = []
    for h in history:
        for s in h.get('strengths', []):
            if len(s) > 10 and s not in strengths_all:
                strengths_all.append(s)
        for i in h.get('improvements', []):
            if len(i) > 10 and i not in improvements_all:
                improvements_all.append(i)

    # Recent activity
    recent_activity = list(reversed(history))[:6]

    return jsonify({
        "total_answers": len(history),
        "avg_score": avg_score,
        "best_score": best_score,
        "avg_confidence": avg_confidence,
        "avg_wpm": avg_wpm,
        "avg_fpm": avg_fpm,
        "avg_star_score": avg_star_score,
        "readiness_index": readiness_index,
        "readiness_tier": readiness_tier,
        "tier_color": tier_color,
        "next_milestone": next_milestone,
        "domains_mastery": domains_mastery,
        "trends": trends,
        "skill_breakdown": skill_breakdown,
        "sentiment_counts": sentiment_counts,
        "common_strengths": strengths_all[:4],
        "common_improvements": improvements_all[:4],
        "recent_activity": recent_activity
    })


# ─── API: Full Interview Simulation Round Summary ─────────────────────────────
@app.route('/api/simulation/summary', methods=['POST'])
def get_simulation_summary():
    data = request.json or {}
    session_ids = data.get('session_ids', [])
    history = load_history()

    round_records = []
    if session_ids:
        round_records = [h for h in history if h.get('id') in session_ids]
    else:
        limit = int(data.get('count', 100))
        round_records = history[-limit:] if history else []

    if not round_records:
        return jsonify({
            "total_questions": 0,
            "average_score": 0,
            "recommendation": "Inconclusive",
            "recommendation_color": "#94a3b8",
            "summary_text": "No questions completed in this interview simulation round.",
            "strengths": [],
            "growth_areas": [],
            "questions": []
        })

    scores = [r.get('score', 0) for r in round_records]
    avg_score = round(sum(scores) / len(scores))

    confidences = [
        r.get('confidence', {}).get('score', 70)
        for r in round_records
        if isinstance(r.get('confidence'), dict)
    ]
    avg_conf = round(sum(confidences) / len(confidences)) if confidences else 70

    wpms = [
        r.get('speech_analysis', {}).get('wpm', r.get('wpm', 135))
        for r in round_records
    ]
    avg_wpm = round(sum(wpms) / len(wpms)) if wpms else 135

    # Recommendation rubric
    if avg_score >= 85 and avg_conf >= 75:
        recommendation = "STRONG HIRE"
        rec_color = "#10b981"
        summary_text = "Candidate demonstrated exceptional domain mastery, crisp structural communication, authoritative delivery, and strong technical depth across all questions."
    elif avg_score >= 70:
        recommendation = "HIRE"
        rec_color = "#6366f1"
        summary_text = "Solid technical competency with clear problem solving. Minor improvements recommended in quantifying results and eliminating filler pauses."
    elif avg_score >= 50:
        recommendation = "LEANING HIRE"
        rec_color = "#f59e0b"
        summary_text = "Good foundational understanding, but inconsistent depth and occasional hesitation on complex architectural questions."
    else:
        recommendation = "NO HIRE / NEEDS PRACTICE"
        rec_color = "#ef4444"
        summary_text = "Significant gaps in core domain terminology, hesitant delivery, and incomplete architectural reasoning. Further practice recommended."

    # Aggregate strengths & improvements
    strengths = []
    growth_areas = []
    for r in round_records:
        for s in r.get('strengths', []):
            if s not in strengths:
                strengths.append(s)
        for i in r.get('improvements', []):
            if i not in growth_areas:
                growth_areas.append(i)

    return jsonify({
        "total_questions": len(round_records),
        "questions_completed": len(round_records),
        "average_score": avg_score,
        "avg_score": avg_score,
        "average_confidence": avg_conf,
        "avg_confidence": avg_conf,
        "average_wpm": avg_wpm,
        "avg_wpm": avg_wpm,
        "recommendation": recommendation,
        "hiring_recommendation": recommendation,
        "recommendation_color": rec_color,
        "summary_text": summary_text,
        "executive_summary": summary_text,
        "strengths": strengths[:4],
        "growth_areas": growth_areas[:4],
        "questions": [
            {
                "id": r.get('id'),
                "question": r.get('question'),
                "score": r.get('score'),
                "grade": r.get('grade'),
                "domain": r.get('domain_label')
            }
            for r in round_records
        ],
        "question_breakdown": [
            {
                "id": r.get('id'),
                "question_text": r.get('question'),
                "score": r.get('score'),
                "grade": r.get('grade'),
                "wpm": r.get('speech_analysis', {}).get('wpm', r.get('wpm', 135)),
                "domain": r.get('domain_label')
            }
            for r in round_records
        ]
    })


if __name__ == '__main__':
    app.run(debug=False, port=5000)
