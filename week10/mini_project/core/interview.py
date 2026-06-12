import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple

from week10.mini_project import config
from week10.mini_project.core.llm_client import LLMClient
from week10.mini_project.core.question_bank import QuestionBank
from week10.mini_project.core.text_utils import normalize, is_answer_long_enough
from week10.mini_project.core.schemas import (
    EvaluationResult, 
    FollowUpQuestion, 
    FeedbackAndModelAnswer, 
    SessionReportSummary
)
from week10.mini_project.core import prompts

logger = logging.getLogger(__name__)

class InterviewManager:
    """
    Orchestrates the lifecycle of an interview session.
    Controls the flow: Setup -> Gating -> Evaluation -> Branching (Follow-up / Feedback) -> Report.
    """
    def __init__(self, role: str, persona_key: str, interview_type: str, max_questions: int = 3, model_name: Optional[str] = None) -> None:
        self.role = role
        self.persona_key = persona_key
        self.interview_type = interview_type
        self.max_questions = max_questions
        self.model_name = model_name or config.MODEL_NAME
        
        # Load persona details
        self.persona = self._load_persona(persona_key)
        self.max_followup = self.persona.get("max_followup", 1)
        
        # Instantiate dependencies
        self.llm = LLMClient(model_name=self.model_name)
        self.q_bank = QuestionBank()
        
        # Initialize internal state trackers
        self.current_question: Optional[Dict[str, Any]] = None
        self.followup_count: int = 0
        self.asked_ids: List[str] = []
        self.transcript: List[Dict[str, Any]] = [] # Records completed questions (Q, A, Eval, Feedback, ModelAnswer)
        self.current_turn_history: List[Dict[str, str]] = [] # Dialogue history for the CURRENT question (includes tail questions)
        self.current_turn_evaluations: List[Dict[str, Any]] = [] # Tracks evaluations and thinking blocks in current turn

        
    def _load_persona(self, persona_key: str) -> Dict[str, Any]:
        """Loads persona specs from configuration."""
        try:
            with open(config.PERSONA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            personas = data.get("personas", {})
            return personas.get(persona_key, personas.get("neutral", {}))
        except Exception as e:
            logger.error(f"Failed to load persona metadata: {e}")
            return {"label": "중립형", "tone": "담백한 말투", "style_directives": [], "max_followup": 1, "encouragement": "mid"}

    def prepare_next_question(self) -> Optional[str]:
        """
        Samples a new question from the bank.
        Resets turn-specific counters and dialogue history.
        Returns the initial question text.
        """
        self.current_question = self.q_bank.sample_question(
            role=self.role,
            interview_type=self.interview_type,
            asked_ids=self.asked_ids
        )
        if not self.current_question:
            logger.warning("No more questions available in the bank.")
            return None
            
        self.followup_count = 0
        self.asked_ids.append(self.current_question["id"])
        
        # Format initial question with persona's greeting if it's the very first question
        greeting = ""
        if len(self.asked_ids) == 1:
            greeting = self.persona.get("greeting", "") + " "
            
        question_text = greeting + self.current_question["question"]
        
        # Reset current turn dialogue history
        self.current_turn_history = [
            {"role": "assistant", "content": question_text}
        ]
        
        return question_text

    def process_answer(self, user_answer: str) -> Tuple[str, Dict[str, Any]]:
        """
        Processes a candidate's answer.
        Returns:
            Tuple[response_message, details_dict]
            - response_message: The next question (follow-up) or feedback & model answer.
            - details_dict: Dictionary containing internal states ("type": "follow_up" | "feedback" | "gate_failed", "data": {...})
        """
        if not self.current_question:
            raise ValueError("No active question to answer.")

        normalized_ans = normalize(user_answer)
        min_tokens = self.current_question.get("min_answer_tokens", 40)
        
        # Append candidate's response to the dialogue history (thought blocks will not be here)
        self.current_turn_history.append({"role": "user", "content": normalized_ans})

        # 1. Gating check
        if not is_answer_long_enough(normalized_ans, min_tokens):
            logger.info("Answer failed length gate.")
            # Do NOT increment followup_count or LLM evaluation. Just prompt for more details.
            gate_msg = "답변이 조금 짧은 것 같습니다. 본인의 생각이나 기술적 경험을 더 구체적으로 보충해서 답변해주실 수 있을까요?"
            
            # Persona adjustments to gate message
            if self.persona_key == "pressure":
                gate_msg = "답변이 너무 빈약합니다. 구체적인 내용과 근거를 담아 다시 답변해 주세요."
            elif self.persona_key == "friendly":
                gate_msg = "좋은 방향인데, 조금만 더 자세히 들려주실 수 있을까요? 예를 들어 구체적인 원리나 사례가 있다면 함께 말씀해주세요!"
                
            # Keep dialogue track clean by removing this short attempt or adjusting history
            self.current_turn_history.pop() # Remove the short answer from official history
            
            return gate_msg, {"type": "gate_failed", "data": {"min_tokens": min_tokens}}

        # 2. Perform Evaluation (LLM Call, thinking ON, index mapped)
        eval_result = self._evaluate_answer(normalized_ans)
        thinking = self.llm.last_thinking
        
        self.current_turn_evaluations.append({
            "answer": normalized_ans,
            "evaluation": eval_result.model_dump(),
            "thinking": thinking
        })
        
        # 3. Determine branching logic
        unresolved_idx = self._get_unresolved_eval_point_index(eval_result.eval_point_results)
        
        if unresolved_idx is not None and self.followup_count < self.max_followup:
            # Branch A: Follow-up Question
            self.followup_count += 1
            follow_up_q = self._generate_follow_up(unresolved_idx, normalized_ans)
            
            # Record follow-up question to dialogue history
            self.current_turn_history.append({"role": "assistant", "content": follow_up_q})
            
            return follow_up_q, {
                "type": "follow_up", 
                "data": {
                    "evaluation": eval_result.model_dump(),
                    "followup_count": self.followup_count,
                    "max_followup": self.max_followup
                }
            }
        else:
            # Branch B: Feedback and Model Answer
            feedback_data = self._generate_feedback_and_model_answer()
            
            # Package this turn into transcript
            self.transcript.append({
                "question_id": self.current_question["id"],
                "topic": self.current_question.get("topic", ""),
                "difficulty": self.current_question.get("difficulty", "medium"),
                "question": self.current_question["question"],
                "candidate_conversation": list(self.current_turn_history),
                "evaluations": list(self.current_turn_evaluations),
                "evaluation": eval_result.model_dump(),
                "model_answer": feedback_data.model_answer,
                "feedback": feedback_data.feedback,
                "thinking": thinking
            })
            
            # Clean turn history for next question
            self.current_turn_history = []
            self.current_turn_evaluations = []
            
            return feedback_data.feedback, {
                "type": "feedback",
                "data": {
                    "evaluation": eval_result.model_dump(),
                    "model_answer": feedback_data.model_answer,
                    "feedback": feedback_data.feedback
                }
            }


    def _evaluate_answer(self, candidate_answer: str) -> EvaluationResult:
        """Calls LLM with strict evaluation rubric and index mapping."""
        eval_points = self.current_question["eval_points"]
        eval_points_text = "\n".join([f"- [{i}] {point}" for i, point in enumerate(eval_points)])
        
        system_prompt = prompts.EVALUATION_SYSTEM_PROMPT.format(
            question_text=self.current_question["question"],
            eval_points_text=eval_points_text
        )
        
        user_prompt = prompts.EVALUATION_USER_TEMPLATE.format(
            candidate_answer=candidate_answer,
            num_eval_points=len(eval_points)
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Fallback factory for EvaluationResult
        def evaluation_fallback():
            return EvaluationResult(
                eval_point_results=[False] * len(eval_points),
                logic_score=3,
                detail_score=3,
                delivery_score=3
            )
            
        result = self.llm.generate_json(
            messages=messages,
            response_model=EvaluationResult,
            fallback_factory=evaluation_fallback,
            temperature=0.0 # Strict objectivity
        )
        
        # Post-processing safeguard: ensure list length matches expected points
        if len(result.eval_point_results) != len(eval_points):
            logger.warning(f"Model returned list length {len(result.eval_point_results)} but expected {len(eval_points)}. Truncating or padding.")
            results = result.eval_point_results[:len(eval_points)]
            while len(results) < len(eval_points):
                results.append(False)
            result.eval_point_results = results
            
        return result

    def _get_unresolved_eval_point_index(self, results: List[bool]) -> Optional[int]:
        """Finds the first unresolved evaluation point index."""
        for i, satisfied in enumerate(results):
            if not satisfied:
                return i
        return None

    def _generate_follow_up(self, unresolved_idx: int, last_answer: str) -> str:
        """Generates a persona-aligned tail question addressing a specific missing point."""
        eval_points = self.current_question["eval_points"]
        follow_up_hints = self.current_question.get("follow_up_hints", [])
        
        unresolved_point = eval_points[unresolved_idx]
        # Map to hint if available, otherwise construct fallback
        follow_up_hint = ""
        if unresolved_idx < len(follow_up_hints):
            follow_up_hint = follow_up_hints[unresolved_idx]
        else:
            follow_up_hint = f"'{unresolved_point}'에 대해 조금 더 구체적으로 고찰하도록 이끄세요."
            
        system_prompt = prompts.FOLLOW_UP_SYSTEM_PROMPT.format(
            persona_tone=self.persona.get("tone", ""),
            persona_directives="\n".join([f"- {d}" for d in self.persona.get("style_directives", [])]),
            persona_encouragement=self.persona.get("encouragement", "mid"),
            original_question=self.current_question["question"],
            candidate_answer=last_answer,
            unresolved_point=unresolved_point,
            follow_up_hint=follow_up_hint
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompts.FOLLOW_UP_USER_TEMPLATE}
        ]
        
        fallback_msg = "그렇다면 방금 말씀하신 원리가 구체적으로 어떻게 구현되는지 조금 더 설명해주시겠어요?"
        
        result = self.llm.generate_json(
            messages=messages,
            response_model=FollowUpQuestion,
            fallback_factory=lambda: FollowUpQuestion(question=fallback_msg)
        )
        return result.question

    def _generate_feedback_and_model_answer(self) -> FeedbackAndModelAnswer:
        """Generates final question feedback wrapping standard model keys in persona styles."""
        # Convert turn dialog into readable transcript
        dialog = []
        for turn in self.current_turn_history:
            speaker = "면접관" if turn["role"] == "assistant" else "지원자"
            dialog.append(f"{speaker}: {turn['content']}")
        dialog_text = "\n".join(dialog)
        
        model_answer_keys = self.current_question["model_answer_key"]
        keys_text = "\n".join([f"- {key}" for key in model_answer_keys])
        
        system_prompt = prompts.FEEDBACK_SYSTEM_PROMPT.format(
            persona_tone=self.persona.get("tone", ""),
            feedback_style=self.persona.get("feedback_style", "사실에 근거해 전달"),
            persona_encouragement=self.persona.get("encouragement", "mid"),
            original_question=self.current_question["question"],
            model_answer_key=keys_text,
            conversation_transcript=dialog_text
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompts.FEEDBACK_USER_TEMPLATE}
        ]
        
        fallback_ans = " ".join(model_answer_keys)
        fallback_feedback = "성실히 답변해주셔서 감사합니다. 전체적으로 잘 요약해 주셨습니다."
        
        result = self.llm.generate_json(
            messages=messages,
            response_model=FeedbackAndModelAnswer,
            fallback_factory=lambda: FeedbackAndModelAnswer(model_answer=fallback_ans, feedback=fallback_feedback)
        )
        return result

    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Computes numerical scores and evaluation point success rates using PURE python code.
        """
        if not self.transcript:
            return {
                "avg_logic_score": 0.0,
                "avg_detail_score": 0.0,
                "avg_delivery_score": 0.0,
                "avg_total_score": 0.0,
                "overall_criteria_fulfillment_rate": 0.0,
                "num_questions": 0
            }
            
        total_logic = 0
        total_detail = 0
        total_delivery = 0
        
        total_eval_points = 0
        satisfied_eval_points = 0
        
        for turn in self.transcript:
            eval_data = turn["evaluation"]
            total_logic += eval_data["logic_score"]
            total_detail += eval_data["detail_score"]
            total_delivery += eval_data["delivery_score"]
            
            results = eval_data["eval_point_results"]
            total_eval_points += len(results)
            satisfied_eval_points += sum(1 for r in results if r)
            
        num_q = len(self.transcript)
        
        avg_l = round(total_logic / num_q, 2)
        avg_det = round(total_detail / num_q, 2)
        avg_del = round(total_delivery / num_q, 2)
        avg_tot = round((avg_l + avg_det + avg_del) / 3, 2)
        
        fulfillment_rate = round((satisfied_eval_points / total_eval_points) * 100, 1) if total_eval_points > 0 else 0.0
        
        return {
            "avg_logic_score": avg_l,
            "avg_detail_score": avg_det,
            "avg_delivery_score": avg_del,
            "avg_total_score": avg_tot,
            "overall_criteria_fulfillment_rate": fulfillment_rate,
            "num_questions": num_q
        }

    def generate_final_report(self) -> SessionReportSummary:
        """
        Calls LLM to generate descriptive strengths, weaknesses, and roadmap recommendations.
        """
        # Convert all completed transcript dialogue logs into context text
        session_logs = []
        for i, turn in enumerate(self.transcript):
            session_logs.append(f"=== 질문 {i+1} ===")
            session_logs.append(f"질문 내용: {turn['question']}")
            
            dialog = []
            for item in turn["candidate_conversation"]:
                speaker = "면접관" if item["role"] == "assistant" else "지원자"
                dialog.append(f"  {speaker}: {item['content']}")
            session_logs.append("대화록:")
            session_logs.append("\n".join(dialog))
            
            eval_data = turn["evaluation"]
            scores_txt = f"평가 점수 - 논리성: {eval_data['logic_score']}, 구체성: {eval_data['detail_score']}, 전달력: {eval_data['delivery_score']}"
            session_logs.append(scores_txt)
            session_logs.append(f"피드백: {turn['feedback']}")
            session_logs.append("\n")
            
        session_transcript_text = "\n".join(session_logs)
        
        system_prompt = prompts.FINAL_REPORT_SYSTEM_PROMPT.format(
            role="AI 엔지니어" if self.role == "ai_engineer" else "Python 백엔드 개발자",
            interview_type="기술 면접" if self.interview_type == "technical" else "프로젝트 경험 면접",
            session_transcript=session_transcript_text
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompts.FINAL_REPORT_USER_TEMPLATE}
        ]
        
        fallback_report = SessionReportSummary(
            summary="전체 면접 세션을 성공적으로 이수하셨습니다. 기술적 개념과 전개 면에서 기본기를 보여주셨습니다.",
            strengths=["기본적인 문항 이해력과 답변 전개 능력"],
            weaknesses=["세부 지식에 대한 논리적 구체성 보완 필요"],
            recommendations=["지원 직무와 관련된 핵심 모범 답안 내용을 추가로 실무 학습해 볼 것을 권장합니다."]
        )
        
        result = self.llm.generate_json(
            messages=messages,
            response_model=SessionReportSummary,
            fallback_factory=lambda: fallback_report,
            temperature=0.7 # Allow descriptive synthesis
        )
        return result
