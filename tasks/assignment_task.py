from crewai import Task

from config.agents_config import get_story_agent


def create_assignment_task() -> Task:
    """Create task for User Story agent to generate stories and assignments."""
    story_agent = get_story_agent()
    return Task(
        description=(
            "You have just received both the Product Owner's requirements summary "
            "and the Tech Lead's technical breakdown from the previous steps in "
            "this conversation.\n\n"
            "Generate a list of user stories in the specified format. "
            "Each story must follow this structure:\n"
            "- Title\n"
            "- As a [user], I want [action] so that [benefit]\n"
            "- Acceptance Criteria (minimum 3 points)\n"
            "- Priority: P0 / P1 / P2\n"
            "- Assigned Developer (simulated)\n"
            "- Estimated Effort: S / M / L\n\n"
            "Return the stories as a JSON array where each item has the fields:\n"
            '"title", "user_story", "acceptance_criteria", '
            '"priority", "assigned_developer", "estimated_effort".'
        ),
        expected_output=(
            "A valid JSON array of user stories with the required fields and "
            "at least three acceptance criteria items per story."
        ),
        agent=story_agent,
    )


