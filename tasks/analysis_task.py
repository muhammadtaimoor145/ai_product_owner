from crewai import Task

from config.agents_config import get_po_agent


def create_analysis_task() -> Task:
    """Create task for Product Owner agent to analyze inputs."""
    po_agent = get_po_agent()
    return Task(
        description=(
            "Analyze the provided Slack messages and meeting notes.\n\n"
            "Slack messages:\n{slack_messages}\n\n"
            "Meeting notes:\n{meeting_notes}\n\n"
            "Extract the key business requirements, goals, constraints, and "
            "open questions. Summarize them clearly in product language, "
            "ready to be shared with a Tech Lead."
        ),
        expected_output=(
            "A concise product requirements summary with:\n"
            "- Overall goal\n"
            "- Key user problems\n"
            "- Functional requirements\n"
            "- Non-functional requirements\n"
            "- Risks or ambiguities\n"
        ),
        agent=po_agent,
    )


