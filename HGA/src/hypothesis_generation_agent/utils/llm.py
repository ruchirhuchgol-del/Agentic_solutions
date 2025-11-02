

import logging
import json
import re
import tiktoken
from typing import Dict, Any, Optional, Union

from crewai import LLM
from ..config import get_config_loader

logger = logging.getLogger(__name__)

def create_llm(model_name: Optional[str] = None, **kwargs) -> LLM:
    """
    Creates and returns a configured CrewAI LLM instance.

    This function acts as a factory for LLMs, pulling default configurations
    from the central config loader and allowing for overrides.

    Args:
        model_name (Optional[str]): The name of the model configuration to use
            (e.g., "default", "creative", "precise"). If None, the default is used.
        **kwargs: Additional parameters to override the LLM configuration
            (e.g., temperature, model).

    Returns:
        LLM: A configured CrewAI LLM instance.
    """
    config_loader = get_config_loader()
    llm_config_dict = config_loader.get_llm_config(model_name)
    
    # Merge with any provided kwargs
    final_config = {**llm_config_dict, **kwargs}
    
    logger.info(f"Creating LLM with model: {final_config.get('model')}")
    return LLM(**final_config)

def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """
    Counts the number of tokens in a given text string for a specific model.

    Args:
        text (str): The text to tokenize.
        model (str): The model name to use for tokenization.

    Returns:
        int: The number of tokens.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning(f"Model '{model}' not found in tiktoken. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))

def parse_json_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Parses a JSON object from a potentially messy LLM text response.

    This function attempts to extract and parse JSON, handling common issues
    like markdown code block wrappers and trailing commas.

    Args:
        response_text (str): The raw text response from an LLM.

    Returns:
        Optional[Dict[str, Any]]: The parsed JSON object as a dictionary,
        or None if parsing fails.
    """
    if not isinstance(response_text, str):
        logger.error("Input to parse_json_response must be a string.")
        return None

    # Attempt to find JSON within markdown code blocks
    match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL | re.IGNORECASE)
    if match:
        json_str = match.group(1)
    else:
        # If no code block, assume the whole string is JSON
        json_str = response_text

    # Clean up common JSON errors
    json_str = json_str.strip()
    # Remove trailing commas before closing brackets/braces
    json_str = re.sub(r",(\s*[}\]])", r"\1", json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from response: {e}")
        logger.debug(f"Problematic JSON string: {json_str}")
        return None

# Example usage for testing
if __name__ == "__main__":
    # Test LLM creation
    llm_instance = create_llm(model_name="precise")
    print(f"Created LLM: {llm_instance.model}")

    # Test token counting
    sample_text = "This is a sample text to count tokens."
    token_count = count_tokens(sample_text)
    print(f"Token count for '{sample_text}': {token_count}")

    # Test JSON parsing
    messy_json = """
    Here is the data you requested:
    ```json
    {
        "hypothesis": "H₀: μ₁ = μ₂",
        "test": "t-test",
    }
    ```
    """
    parsed_data = parse_json_response(messy_json)
    print(f"Parsed JSON: {parsed_data}")