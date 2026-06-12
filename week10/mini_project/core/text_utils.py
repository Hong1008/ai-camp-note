import re

def normalize(text: str) -> str:
    """
    Normalizes the input text by stripping whitespace, merging multiple spaces,
    and removing any potential markdown garbage tags.
    """
    if not text:
        return ""
    # Merge multiple spaces and newlines
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()

def estimate_tokens(text: str) -> int:
    """
    Estimates the number of tokens in the text using a fast heuristics method.
    This avoids loading heavy models like transformers into memory.
    - CJK characters: 1 character ~ 1.5 tokens
    - English words: 1 word ~ 1.3 tokens
    - Others: 1 character ~ 1 token
    """
    if not text:
        return 0
        
    cjk_char_count = 0
    english_word_chars = []
    other_chars_count = 0
    
    # Iterate characters to count CJK vs English
    for char in text:
        # Check CJK range (Hangul, Hanja, etc.)
        if '\u4e00' <= char <= '\u9fff' or '\uac00' <= char <= '\ud7a3' or '\u1100' <= char <= '\u11ff' or '\u3130' <= char <= '\u318f':
            cjk_char_count += 1
        elif char.isalnum() or char == "'":
            english_word_chars.append(char)
        else:
            if char.isspace() and english_word_chars:
                english_word_chars.append(' ')
            else:
                other_chars_count += 1
                
    # Parse English words
    english_text = "".join(english_word_chars)
    english_words = [w for w in english_text.split() if w]
    english_word_count = len(english_words)
    
    estimated = int(
        (cjk_char_count * 1.5) +
        (english_word_count * 1.3) +
        (other_chars_count * 1.0)
    )
    # Always return at least 1 token if input is not empty
    return max(1, estimated)

def is_answer_long_enough(text: str, min_tokens: int) -> bool:
    """
    Returns True if the estimated tokens of the normalized text satisfies the minimum token requirement.
    """
    normalized_text = normalize(text)
    token_count = estimate_tokens(normalized_text)
    return token_count >= min_tokens
