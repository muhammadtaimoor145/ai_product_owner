import json
import logging
from typing import Any, Dict, Optional

from crewai import Crew, Process

from tasks.analysis_task import create_analysis_task
from tasks.communication_task import create_communication_task
from tasks.assignment_task import create_assignment_task
from tasks.evaluation_task import create_evaluation_task
from utils.formatters import parse_stories_to_dataframe


logger = logging.getLogger(__name__)


def _extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Best-effort extraction of a JSON object from LLM output."""
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
    except ValueError:
        return None

    snippet = text[start:end]
    try:
        return json.loads(snippet)
    except json.JSONDecodeError:
        return None


def _run_main_crew(slack_messages: str, meeting_notes: str) -> Dict[str, Any]:
    """Run the main PO → Tech Lead → Story agent workflow."""
    analysis_task = create_analysis_task()
    communication_task = create_communication_task()
    assignment_task = create_assignment_task()

    crew = Crew(
        agents=[
            analysis_task.agent,
            communication_task.agent,
            assignment_task.agent,
        ],
        tasks=[analysis_task, communication_task, assignment_task],
        process=Process.sequential,
    )

    inputs: Dict[str, Any] = {
        "slack_messages": slack_messages,
        "meeting_notes": meeting_notes,
    }

    result = crew.kickoff(inputs=inputs)

    stories_dataframe = None
    try:
        stories_dataframe = parse_stories_to_dataframe(str(result))  # type: ignore[arg-type]
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to parse stories into a DataFrame: %s", exc)

    return {
        "raw_result": str(result),
        "stories_table": stories_dataframe,
    }


def _run_evaluation(
    original_input: str,
    agent_communication: str,
    user_stories_json: str,
) -> Optional[Dict[str, Any]]:
    """Run the Evaluator agent on the final stories and inputs."""
    evaluation_task = create_evaluation_task(
        original_input=original_input,
        agent_communication=agent_communication,
        user_stories_json=user_stories_json,
    )

    evaluation_crew = Crew(
        agents=[evaluation_task.agent],
        tasks=[evaluation_task],
        process=Process.sequential,
    )

    result = evaluation_crew.kickoff(
        inputs={
            "original_input": original_input,
            "agent_communication": agent_communication,
            "user_stories_json": user_stories_json,
        }
    )

    raw_text = str(result)
    parsed = _extract_json_object(raw_text)
    if parsed is None:
        logger.error("Failed to decode evaluation JSON from evaluator output.")
    return parsed


def run_crew(slack_messages: str, meeting_notes: str) -> Dict[str, Any]:
    """Run the full workflow (main crew + evaluation) and return results for the UI."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    main_result = _run_main_crew(slack_messages=slack_messages, meeting_notes=meeting_notes)

    original_input = (
        f"Slack messages:\n{slack_messages}\n\n"
        f"Meeting notes:\n{meeting_notes}"
    )

    # For now, we treat the main crew's raw result as the communication transcript.
    agent_communication = main_result.get("raw_result", "")
    user_stories_json = main_result.get("raw_result", "")

    evaluation = _run_evaluation(
        original_input=original_input,
        agent_communication=str(agent_communication),
        user_stories_json=str(user_stories_json),
    )

    return {
        "raw_result": main_result.get("raw_result"),
        "stories_table": main_result.get("stories_table"),
        "evaluation": evaluation,
    }


