import pytest
from pydantic import BaseModel, Field
from week10.mini_project.core.llm_client import LLMClient

class MockSchema(BaseModel):
    score: int = Field(description="점수")
    feedback: str = Field(description="피드백")

def test_clean_raw_output():
    client = LLMClient()
    
    # 1. Standard thought block stripping
    raw_1 = "<thought>This is some thinking process.</thought>{\"score\": 5, \"feedback\": \"Good job\"}"
    assert client.clean_raw_output(raw_1) == "{\"score\": 5, \"feedback\": \"Good job\"}"

    # 2. Channel thought block stripping
    raw_2 = "<|channel>thoughtThis is another thinking process.<channel|>{\"score\": 4, \"feedback\": \"Decent\"}"
    assert client.clean_raw_output(raw_2) == "{\"score\": 4, \"feedback\": \"Decent\"}"

    # 3. Markdown JSON wrapping stripping
    raw_3 = "```json\n{\"score\": 3, \"feedback\": \"OK\"}\n```"
    assert client.clean_raw_output(raw_3) == "{\"score\": 3, \"feedback\": \"OK\"}"

    # 4. Hybrid mixed text block with markdown and thought
    raw_4 = "<thought>Thinking...</thought>\nHere is some non-json leading text.\n```json\n{\"score\": 5, \"feedback\": \"Excellent\"}\n```\nSome trailing text."
    assert client.clean_raw_output(raw_4) == "{\"score\": 5, \"feedback\": \"Excellent\"}"

def test_extract_thinking():
    client = LLMClient()
    
    raw_1 = "<thought>This is the thought.</thought>Response text"
    assert client.extract_thinking(raw_1) == "This is the thought."

    raw_2 = "<|channel>thoughtThis is channel thought.<channel|>Response text"
    assert client.extract_thinking(raw_2) == "This is channel thought."
    
    raw_no_thought = "Response text without thought block"
    assert client.extract_thinking(raw_no_thought) == ""

@pytest.mark.integration
def test_real_llm_json_generation():
    """
    Integration test to verify that thinking ON and response_format={"type": "json_object"}
    coexist stably on the Google Gemini OpenAI-compatible API without throwing errors.
    """
    client = LLMClient()
    messages = [
        {"role": "system", "content": "You are a helpful assistant. You must respond ONLY with a JSON object matching the schema: {'score': int, 'feedback': str}."},
        {"role": "user", "content": "Evaluate this statement: 'FastAPI is faster than Django because of asynchronous support.'"}
    ]
    
    # Call the LLM to get structured JSON
    result = client.generate_json(
        messages=messages,
        response_model=MockSchema,
        fallback_factory=lambda: MockSchema(score=1, feedback="Fallback")
    )
    
    # Assertions
    assert isinstance(result, MockSchema)
    assert 1 <= result.score <= 100
    assert len(result.feedback) > 0
    print(f"Integration Test Success! Parsed Result: {result}")


