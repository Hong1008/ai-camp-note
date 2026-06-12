import json
import random
import logging
from typing import List, Dict, Any, Optional

from week10.mini_project import config

logger = logging.getLogger(__name__)

class QuestionBank:
    """
    Handles loading, filtering, and sampling questions from the JSON database.
    Includes a fallback mechanism to prevent empty selections.
    """
    def __init__(self) -> None:
        self.questions: List[Dict[str, Any]] = []
        self.load_questions()

    def load_questions(self) -> None:
        """
        Loads questions from the configured JSON file path.
        """
        try:
            with open(config.QUESTION_BANK_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.questions = data.get("questions", [])
            logger.info(f"Loaded {len(self.questions)} questions from {config.QUESTION_BANK_PATH}")
        except Exception as e:
            logger.error(f"Failed to load questions from {config.QUESTION_BANK_PATH}: {e}")
            self.questions = []

    def get_questions(
        self,
        role: str,
        interview_type: str,
        topic: Optional[str] = None,
        asked_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Filters questions based on role, type, topic, and excludes already asked questions.
        If topic filter yields no results, falls back to role & type.
        """
        asked = asked_ids or []
        
        # Helper to check if role matches (handles 'both')
        def role_matches(q_role: str, target_role: str) -> bool:
            return q_role == target_role or q_role == "both"

        # Step 1: Filter by role and type, excluding already asked
        base_filtered = [
            q for q in self.questions
            if role_matches(q.get("role", ""), role)
            and q.get("type", "") == interview_type
            and q.get("id") not in asked
        ]

        if not base_filtered:
            # If everything of this role/type was asked, reset and allow asked ones as fallback
            logger.warning(f"All questions for role={role}, type={interview_type} have been asked. Resetting exclusion.")
            base_filtered = [
                q for q in self.questions
                if role_matches(q.get("role", ""), role)
                and q.get("type", "") == interview_type
            ]

        # Step 2: Apply topic filter if requested
        if topic:
            topic_filtered = [
                q for q in base_filtered
                if q.get("topic") == topic
            ]
            if topic_filtered:
                return topic_filtered
            else:
                logger.warning(f"No questions found for topic='{topic}' under role={role}, type={interview_type}. Falling back to general role/type questions.")
        
        return base_filtered

    def sample_question(
        self,
        role: str,
        interview_type: str,
        topic: Optional[str] = None,
        asked_ids: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Samples a single question randomly based on filters.
        """
        candidates = self.get_questions(role, interview_type, topic, asked_ids)
        if not candidates:
            return None
        return random.choice(candidates)

    def sample_questions_batch(
        self,
        role: str,
        interview_type: str,
        count: int,
        asked_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Samples a batch of N questions. It distributes questions across topics to maximize diversity.
        """
        candidates = self.get_questions(role, interview_type, topic=None, asked_ids=asked_ids)
        if not candidates:
            return []
        
        # Shuffle candidates to randomize selection
        random.shuffle(candidates)
        
        # Try to select questions with unique topics to increase diversity
        selected: List[Dict[str, Any]] = []
        selected_topics = set()
        
        # First pass: try to get unique topics
        for q in candidates:
            q_topic = q.get("topic")
            if q_topic not in selected_topics:
                selected.append(q)
                selected_topics.add(q_topic)
                if len(selected) == count:
                    break
                    
        # Second pass: if we need more questions, fill in from remaining candidates
        if len(selected) < count:
            remaining = [q for q in candidates if q not in selected]
            needed = count - len(selected)
            selected.extend(remaining[:needed])
            
        return selected[:count]
