from crewai import Task

from config.agents_config import get_tech_lead_agent


def create_communication_task() -> Task:
    """Create task for Tech Lead to respond to Product Owner analysis."""
    tech_lead = get_tech_lead_agent()
    return Task(
        description=(
            "You have just received the Product Owner's requirements summary from "
            "the previous step in this conversation.\n\n"
            "As the Tech Lead, break this down into technical implications. "
            "Identify components, services, or systems impacted, outline the "
            "high-level technical approach, and estimate complexity. "
            "Suggest which types of developers (e.g., frontend, backend, "
            "data engineer) should own each area."
        ),
        expected_output=(
            "A structured technical breakdown including:\n"
            "- List of technical areas or components\n"
            "- For each, a short description and complexity (S/M/L)\n"
            "- Suggested developer profile to own it\n"
            "- Key risks or dependencies\n"
        ),
        agent=tech_lead,
    )


