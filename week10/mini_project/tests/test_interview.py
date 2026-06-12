import pytest
from week10.mini_project.core.interview import InterviewManager
from week10.mini_project.core.schemas import EvaluationResult

def test_interview_manager_init():
    manager = InterviewManager(
        role="ai_engineer",
        persona_key="friendly",
        interview_type="technical",
        max_questions=3
    )
    assert manager.role == "ai_engineer"
    assert manager.persona_key == "friendly"
    assert manager.interview_type == "technical"
    assert manager.max_questions == 3
    assert manager.max_followup == 1
    assert manager.persona["label"] == "친근형"

def test_interview_turn_gating_gate_failed():
    manager = InterviewManager(
        role="python_backend",
        persona_key="neutral",
        interview_type="technical",
        max_questions=2
    )
    
    # Set up question manually
    manager.current_question = {
        "id": "be_tech_001",
        "question": "Python list, tuple의 차이를 말해주세요.",
        "eval_points": ["Point 1", "Point 2"],
        "min_answer_tokens": 40
    }
    manager.asked_ids.append("be_tech_001")
    manager.current_turn_history = [{"role": "assistant", "content": manager.current_question["question"]}]
    
    # Very short answer that should fail the gate
    answer = "몰라요"
    msg, details = manager.process_answer(answer)
    
    assert details["type"] == "gate_failed"
    assert "구체적으로" in msg or "자세히" in msg or "다시" in msg
    assert manager.followup_count == 0 # Follow-up count should NOT increase

@pytest.mark.integration
def test_interview_full_loop_evaluation_and_feedback():
    manager = InterviewManager(
        role="ai_engineer",
        persona_key="neutral",
        interview_type="technical",
        max_questions=1
    )
    
    # Pull next question
    q_txt = manager.prepare_next_question()
    assert q_txt is not None
    assert manager.current_question is not None
    
    # Process long enough answer
    answer = "지도학습은 정답 레이블이 주어지는 데이터로 훈련하여 회귀나 분류 문제를 해결하는 기법이고, 대표적인 예로는 선형 회귀나 로지스틱 회귀가 있습니다. 반면 비지도학습은 레이블이 주어지지 않고 데이터의 내재적 패턴을 학습하며, 대표적으로 K-평균 군집화나 PCA 차원축소가 활용됩니다."
    msg, details = manager.process_answer(answer)
    
    # Since answer is good and long, details should be either 'follow_up' or 'feedback'
    assert details["type"] in ["follow_up", "feedback"]
    assert "evaluation" in details["data"]
    eval_data = details["data"]["evaluation"]
    assert "eval_point_results" in eval_data
    assert len(eval_data["eval_point_results"]) == len(manager.current_question["eval_points"])

def test_get_summary_statistics():
    manager = InterviewManager(
        role="ai_engineer",
        persona_key="neutral",
        interview_type="technical"
    )
    
    # Empty transcript
    stats = manager.get_summary_statistics()
    assert stats["avg_total_score"] == 0.0
    
    # Add dummy transcript turns
    manager.transcript = [
        {
            "evaluation": {
                "eval_point_results": [True, True, False],
                "logic_score": 4,
                "detail_score": 3,
                "delivery_score": 5
            }
        },
        {
            "evaluation": {
                "eval_point_results": [True, True, True, False],
                "logic_score": 3,
                "detail_score": 4,
                "delivery_score": 4
            }
        }
    ]
    
    stats = manager.get_summary_statistics()
    assert stats["num_questions"] == 2
    assert stats["avg_logic_score"] == 3.5  # (4 + 3)/2
    assert stats["avg_detail_score"] == 3.5  # (3 + 4)/2
    assert stats["avg_delivery_score"] == 4.5  # (5 + 4)/2
    assert stats["avg_total_score"] == 3.83  # (3.5 + 3.5 + 4.5)/3 = 11.5/3 = 3.83
    # fulfillment: satisfied = 2 (first) + 3 (second) = 5. total = 3 + 4 = 7. 5/7 = 71.4%
    assert stats["overall_criteria_fulfillment_rate"] == 71.4
