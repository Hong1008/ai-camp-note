from typing import List
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    """
    Evaluation result for a candidate answer.
    Uses index mapping (List[bool]) for eval_points to avoid string matching mismatches.
    """
    eval_point_results: List[bool] = Field(
        description="질문 은행에 등재된 eval_points 인덱스 순서대로 각 채점 기준을 만족했는지 여부 (예: 첫 번째 기준 만족 시 True, 두 번째 미만족 시 False)"
    )
    logic_score: int = Field(
        description="답변의 논리적 전개 수준 점수 (1~5 정수)"
    )
    detail_score: int = Field(
        description="답변의 기술적/경험적 구체성 수준 점수 (1~5 정수)"
    )
    delivery_score: int = Field(
        description="답변의 의사소통 및 전달력 수준 점수 (1~5 정수)"
    )

class FollowUpQuestion(BaseModel):
    """
    A generated follow-up tail question.
    """
    question: str = Field(description="지원자에게 던질 꼬리질문 (페르소나 톤 반영)")

class FeedbackAndModelAnswer(BaseModel):
    """
    Feedback and expansion of the model answer key.
    """
    model_answer: str = Field(description="model_answer_key를 신입 눈높이 문장으로 살을 붙여 확장한 모범 답안")
    feedback: str = Field(description="지원자 답변과 모범 답안을 대비하여 강점과 학습 방향을 짚어주는 페르소나 스타일 피드백")

class SessionReportSummary(BaseModel):
    """
    Final review summary of the entire interview.
    """
    summary: str = Field(description="전체 면접 과정에 대한 한눈에 보는 종합 총평 (한국어)")
    strengths: List[str] = Field(description="면접 답변에서 돋보인 핵심 강점 목록 (최대 3개)")
    weaknesses: List[str] = Field(description="면접 답변에서 보완이 필수적인 약점 목록 (최대 3개)")
    recommendations: List[str] = Field(description="신입 엔지니어 관점에서 공부하면 좋을 실무 학습 추천 사항 목록")
