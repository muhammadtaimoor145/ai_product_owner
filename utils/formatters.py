import json
import logging
from typing import Any, Dict, List, Optional

import pandas as pd


logger = logging.getLogger(__name__)


def parse_stories_to_dataframe(raw_output: str) -> Optional[pd.DataFrame]:
    """Parse raw JSON stories output into a pandas DataFrame.

    The raw_output is expected to be a JSON array where each item has:
    - title
    - user_story
    - acceptance_criteria (list of strings)
    - priority
    - assigned_developer
    - estimated_effort
    """
    try:
        stories: List[Dict[str, Any]] = json.loads(raw_output)
    except json.JSONDecodeError:
        logger.error("Failed to decode stories JSON from agent output.")
        return None

    if not isinstance(stories, list):
        logger.error("Stories JSON is not a list.")
        return None

    normalized: List[Dict[str, Any]] = []
    for story in stories:
        acceptance_raw = story.get("acceptance_criteria", [])
        if isinstance(acceptance_raw, list):
            acceptance_text = "\n".join(f"- {item}" for item in acceptance_raw)
        else:
            acceptance_text = str(acceptance_raw)

        normalized.append(
            {
                "Title": story.get("title", ""),
                "User Story": story.get("user_story", ""),
                "Acceptance Criteria": acceptance_text,
                "Priority": story.get("priority", ""),
                "Assigned Developer": story.get("assigned_developer", ""),
                "Estimated Effort": story.get("estimated_effort", ""),
            }
        )

    if not normalized:
        return None

    return pd.DataFrame(normalized)


