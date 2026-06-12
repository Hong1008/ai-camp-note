import re
import json
import logging
from typing import Type, TypeVar, Optional, Dict, Any, List
from openai import OpenAI, RateLimitError, APIStatusError, APIError, APITimeoutError
from pydantic import BaseModel, ValidationError

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from week10.mini_project import config

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    """
    LLM Client wrapper for interacting with the OpenAI-compatible Gemini endpoint.
    Includes custom parsing for thinking blocks, JSON sanitization, and robust retry logic.
    """
    def __init__(self, model_name: Optional[str] = None) -> None:
        self.client = OpenAI(
            api_key=config.GOOGLE_AI_API_KEY,
            base_url=config.BASE_URL,
            timeout=config.DEFAULT_TIMEOUT
        )
        self.model_name = model_name or config.MODEL_NAME
        self.is_google_api = "googleapis.com" in config.BASE_URL
        self.last_thinking = ""
        logger.info(f"Initialized LLMClient (Is Google API: {self.is_google_api}) pointing to {config.BASE_URL} for model {self.model_name} with timeout={config.DEFAULT_TIMEOUT}s")


    def _prepare_call_params(
        self, 
        temperature: Optional[float] = None, 
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Prepares the temperature, top_p, max_tokens and extra_body arguments dynamically.
        Specifically, it strips top_k if calling Google's OpenAI endpoint to prevent 400 Bad Request.
        It also conditionally configures thinking budget parameters depending on the active model.
        """
        params: Dict[str, Any] = {
            "temperature": temperature if temperature is not None else config.DEFAULT_TEMPERATURE,
            "top_p": top_p if top_p is not None else config.DEFAULT_TOP_P,
            "max_tokens": max_tokens if max_tokens is not None else config.DEFAULT_MAX_TOKENS
        }
        
        extra_body: Dict[str, Any] = {}
        
        # If calling Google's API (OpenAI compatibility endpoint)
        if self.is_google_api:
            extra_body["reasoning_effort"] = "high"
        else:
            # Local Ollama/vLLM models
            extra_body["top_k"] = config.DEFAULT_TOP_K
            
        if extra_body:
            params["extra_body"] = extra_body
            
        return params



    def clean_raw_output(self, content: str) -> str:
        """
        Cleans the model's raw string output by:
        1. Stripping thinking blocks (<thought>...</thought> or <|channel>thought...<channel|>).
        2. Extracting only the JSON portion if text is mixed.
        3. Stripping markdown wrapper code blocks.
        """
        if not content:
            return ""

        # Remove <thought>...</thought>
        cleaned = re.sub(r'<thought>.*?</thought>', '', content, flags=re.DOTALL)
        # Remove <|channel>thought ... <channel|>
        cleaned = re.sub(r'<\|channel>thought.*?<channel\|>', '', cleaned, flags=re.DOTALL)
        cleaned = cleaned.strip()

        # Try to locate the JSON block inside the cleaned text
        json_match = re.search(r'(\{.*\}).*', cleaned, flags=re.DOTALL)
        if json_match:
            cleaned = json_match.group(1).strip()

        # Remove markdown JSON wraps: ```json ... ``` or ``` ... ```
        cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        cleaned = cleaned.strip()

        return cleaned

    def extract_thinking(self, content: str) -> str:
        """
        Extracts the thinking process string from the model output if present.
        """
        if not content:
            return ""
        
        # Check standard <thought> tag
        match = re.search(r'<thought>(.*?)</thought>', content, flags=re.DOTALL)
        if match:
            return match.group(1).strip()
            
        # Check gemma model card <|channel>thought tag
        match_channel = re.search(r'<\|channel>thought(.*?)(?:<channel\|>|$)', content, flags=re.DOTALL)
        if match_channel:
            return match_channel.group(1).strip()
            
        return ""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APIStatusError, APITimeoutError)),
        reraise=True
    )
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        temperature: Optional[float] = None, 
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generates standard text completion using standard parameters with exponential backoff on rate limits and timeouts.
        """
        params = self._prepare_call_params(temperature, top_p, max_tokens)
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                reasoning_effort="high",
                messages=messages,
                **params
            )
            message = response.choices[0].message
            if getattr(message, "refusal", None):
                logger.error(f"Model refused the request: {message.refusal}")
                raise APIError(f"Request refused by model: {message.refusal}", request=None, message=message.refusal)
            return message.content or ""

        except APIStatusError as e:
            if e.status_code == 429:
                logger.warning("Rate limit hit (429). Retrying...")
                raise RateLimitError(message=e.message, response=e.response, body=e.body)
            raise e


    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type((json.JSONDecodeError, ValidationError, APITimeoutError)),
        reraise=True
    )
    def generate_json_with_retry(
        self, 
        messages: List[Dict[str, str]], 
        response_model: Type[T],
        temperature: Optional[float] = None, 
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> T:
        """
        Helper method to perform LLM generation and JSON validation with repair retries.
        """
        params = self._prepare_call_params(temperature, top_p, max_tokens)
        # Inject json_object constraint
        params["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            **params
        )
        message = response.choices[0].message
        if getattr(message, "refusal", None):
            logger.error(f"Model refused the request (JSON): {message.refusal}")
            raise APIError(f"Request refused by model: {message.refusal}", request=None, message=message.refusal)
        raw_content = message.content or ""
        self.last_thinking = self.extract_thinking(raw_content)

        cleaned = self.clean_raw_output(raw_content)



        try:
            parsed_dict = json.loads(cleaned)
            validated = response_model.model_validate(parsed_dict)
            return validated
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"JSON Parsing or Validation failed on attempt. Cleaned text: {repr(cleaned)}. Error: {e}")
            raise e

    def generate_json(
        self, 
        messages: List[Dict[str, str]], 
        response_model: Type[T],
        fallback_factory: Any,
        temperature: Optional[float] = None, 
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> T:
        """
        Calls chat completion requesting a JSON object. Cleans thinking blocks, validates with Pydantic,
        uses tenacity to retry on parse failure, and falls back to a default object if it fails completely.
        """
        try:
            return self.generate_json_with_retry(
                messages=messages,
                response_model=response_model,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
        except Exception as e:
            logger.error(f"Generate JSON failed completely after retries. Falling back to default. Error: {e}")
            return fallback_factory()

