import pytest
from week10.mini_project.core.question_bank import QuestionBank

def test_question_bank_loading():
    bank = QuestionBank()
    assert len(bank.questions) > 0
    # Check that keys conform to schema
    for q in bank.questions:
        assert "id" in q
        assert "role" in q
        assert "type" in q
        assert "question" in q
        assert "eval_points" in q
        assert "follow_up_hints" in q
        assert "model_answer_key" in q
        assert "min_answer_tokens" in q

def test_question_bank_filtering():
    bank = QuestionBank()
    
    # Filter for AI engineer technical questions
    ai_tech = bank.get_questions(role="ai_engineer", interview_type="technical")
    assert len(ai_tech) > 0
    for q in ai_tech:
        assert q["role"] in ["ai_engineer", "both"]
        assert q["type"] == "technical"

    # Filter for Backend project questions
    be_proj = bank.get_questions(role="python_backend", interview_type="project")
    assert len(be_proj) > 0
    for q in be_proj:
        assert q["role"] in ["python_backend", "both"]
        assert q["type"] == "project"

def test_question_bank_topic_fallback():
    bank = QuestionBank()
    
    # Try to filter by a topic that definitely doesn't exist for backend technical questions
    non_existent_topic = "Quantum Teleportation"
    questions = bank.get_questions(role="python_backend", interview_type="technical", topic=non_existent_topic)
    
    # It should fall back and return some questions
    assert len(questions) > 0
    for q in questions:
        assert q["role"] in ["python_backend", "both"]
        assert q["type"] == "technical"

def test_sample_questions_batch():
    bank = QuestionBank()
    count = 3
    batch = bank.sample_questions_batch(role="ai_engineer", interview_type="technical", count=count)
    assert len(batch) == count
    # IDs must be unique in a single batch
    ids = [q["id"] for q in batch]
    assert len(ids) == len(set(ids))
