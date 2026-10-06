import unittest
import json
from app import app

class TestMockInterviewApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_routes_exist(self):
        # 1. Index
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'AI Mock Interview Assistant', res.data)
        self.assertIn(b'DATA ALCOTT || SYSTEMS', res.data)

        # 2. Dashboard
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Progress Dashboard', res.data)

        # 3. History
        res = self.client.get('/history')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Practice Session History', res.data)

    def test_questions_api(self):
        res = self.client.get('/api/questions/software_engineering')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(len(data) > 0)
        self.assertIn('text', data[0])
        self.assertIn('keywords', data[0])
        self.assertIn('difficulty', data[0])

    def test_random_question_api(self):
        res = self.client.get('/api/questions/random?domain=software_engineering')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('question', data)
        self.assertIn('text', data['question'])

    def test_add_custom_question(self):
        payload = {
            "domain": "software_engineering",
            "difficulty": "Hard",
            "text": "How do you handle distributed transactions across microservices using the Saga pattern?",
            "keywords": ["saga", "choreography", "orchestration", "compensating transaction", "idempotency"]
        }
        res = self.client.post('/api/questions/add', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data.get('success'))

    def test_evaluate_api(self):
        payload = {
            "domain": "software_engineering",
            "question_id": "se_1",
            "question_text": "Explain SOLID principles",
            "expected_keywords": ["single responsibility", "dependency inversion", "open closed"],
            "response": "In our team I applied Single Responsibility and Dependency Inversion to build modular payment adapters, ensuring low coupling and high testability.",
            "duration_seconds": 45
        }
        res = self.client.post('/api/evaluate', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('score', data)
        self.assertIn('grade', data)
        self.assertIn('score_breakdown', data)
        self.assertIn('sentiment', data)
        self.assertIn('confidence', data)
        self.assertIn('strengths', data)
        self.assertIn('improvements', data)
        self.assertIn('model_answer', data)
        self.assertIn('speech_analysis', data)
        self.assertIn('star_analysis', data)
        self.assertIn('impact_analysis', data)
        self.assertIn('relevance', data)
        
        # Verify speech analysis fields
        speech = data['speech_analysis']
        self.assertIn('wpm', speech)
        self.assertIn('pace_label', speech)
        self.assertIn('fillers_per_minute', speech)
        self.assertIn('delivery_energy_score', speech)
        self.assertIn('vocal_advice', speech)
        
        # Verify STAR analysis fields
        star = data['star_analysis']
        self.assertIn('star_score', star)
        self.assertIn('detected', star)
        self.assertIn('s', star['detected'])
        self.assertIn('t', star['detected'])
        self.assertIn('a', star['detected'])
        self.assertIn('r', star['detected'])

        print("\nEvaluation Response Summary:")
        print(f"  Score: {data['score']}/100 ({data['grade']})")
        print(f"  Speech WPM: {speech['wpm']} ({speech['pace_label']})")
        print(f"  STAR Score: {star['star_score']}%")
        print(f"  Sentiment Tone: {data['sentiment']['tone']} ({data['sentiment']['label']})")
        print(f"  Confidence: {data['confidence']['score']}% ({data['confidence']['level']})")

    def test_simulation_summary_api(self):
        # First ensure there's at least one evaluated session
        eval_payload = {
            "domain": "software_engineering",
            "question_id": "se_sim_1",
            "question_text": "How do you design a high-throughput messaging queue?",
            "expected_keywords": ["partitioning", "kafka", "backpressure"],
            "response": "In our previous architecture, we deployed Kafka partitions with producer backpressure and reduced latency by 40% across 50,000 req/sec.",
            "duration_seconds": 38
        }
        eval_res = self.client.post('/api/evaluate', json=eval_payload)
        eval_data = json.loads(eval_res.data)
        session_id = eval_data.get('session_id')

        # Request simulation summary
        sim_res = self.client.post('/api/simulation/summary', json={"session_ids": [session_id] if session_id else []})
        self.assertEqual(sim_res.status_code, 200)
        sim_data = json.loads(sim_res.data)
        self.assertIn('hiring_recommendation', sim_data)
        self.assertIn('avg_score', sim_data)
        self.assertIn('avg_confidence', sim_data)
        self.assertIn('avg_wpm', sim_data)
        self.assertIn('strengths', sim_data)
        self.assertIn('growth_areas', sim_data)
        self.assertIn('executive_summary', sim_data)
        print("\nSimulation Round Summary:")
        print(f"  Hiring Recommendation: {sim_data['hiring_recommendation']}")
        print(f"  Avg Score: {sim_data['avg_score']}/100")
        print(f"  Avg Cadence: {sim_data['avg_wpm']} WPM")
        print(f"  Executive Summary: {sim_data['executive_summary']}")

    def test_dashboard_stats_api(self):
        res = self.client.get('/api/dashboard/stats')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertIn('total_answers', data)
        self.assertIn('avg_score', data)
        self.assertIn('readiness_index', data)
        self.assertIn('avg_wpm', data)
        self.assertIn('avg_star_score', data)
        self.assertIn('readiness_tier', data)
        self.assertIn('domains_mastery', data)
        self.assertIn('skill_breakdown', data)
        print("\nDashboard Stats Summary:")
        print(f"  Total Answers: {data['total_answers']}")
        print(f"  Avg Score: {data['avg_score']}%")
        print(f"  Avg WPM: {data['avg_wpm']}")
        print(f"  Readiness Index: {data['readiness_index']}% ({data['readiness_tier']})")

    def test_history_api(self):
        res = self.client.get('/api/history')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(isinstance(data, list))

    def test_export_history_api(self):
        res = self.client.get('/api/history/export')
        self.assertEqual(res.status_code, 200)
        self.assertIn('application/json', res.headers.get('Content-Type', ''))
        data = json.loads(res.data)
        self.assertTrue(isinstance(data, list))

if __name__ == '__main__':
    unittest.main()
