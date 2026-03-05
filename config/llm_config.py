import os
from typing import Any, Dict

from crewai import LLM
from dotenv import load_dotenv


load_dotenv()


def get_llm() -> LLM:
    """Create and return the shared LLM configuration for all agents."""
    model_name: str = os.getenv("MODEL_NAME", "gpt-4.1-nano")
    api_key: str | None = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    llm_config: Dict[str, Any] = {
        "model": model_name,
        "temperature": 0.2,
    }
    # Avoid passing `model` twice; the config dict already includes it.
    return LLM(**llm_config)


