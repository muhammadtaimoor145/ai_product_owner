from dataclasses import dataclass

from crewai import Agent

from config.llm_config import get_llm


@dataclass
class AgentConfig:
    """Configuration data for a CrewAI agent."""

    role: str
    goal: str
    backstory: str
    verbose: bool = True
    allow_delegation: bool = False
    memory: bool = True


def create_agent(config: AgentConfig) -> Agent:
    """Create a CrewAI Agent from a configuration object."""
    return Agent(
        role=config.role,
        goal=config.goal,
        backstory=config.backstory,
        verbose=config.verbose,
        allow_delegation=config.allow_delegation,
        memory=config.memory,
        llm=get_llm(),
    )


def get_po_agent() -> Agent:
    """Return the Product Owner agent."""
    po_config = AgentConfig(
        role="Product Owner",
        goal=(
            "Understand business requirements from Slack messages and meeting notes "
            "and explain them in clear product language."
        ),
        backstory=(
            "You are a seasoned Product Owner with deep domain knowledge. "
            "You excel at reading fragmented communication (Slack threads, "
            "meeting notes) and synthesizing them into clear product requirements."
        ),
    )
    return create_agent(po_config)


def get_tech_lead_agent() -> Agent:
    """Return the Tech Lead agent."""
    lead_config = AgentConfig(
        role="Tech Lead",
        goal=(
            "Translate the Product Owner's requirements into technical tasks, "
            "estimates, and suggested assignees."
        ),
        backstory=(
            "You are an experienced Tech Lead who collaborates closely with "
            "Product Owners. You break down product requirements into technical "
            "work, identify risks, and estimate complexity."
        ),
    )
    return create_agent(lead_config)


def get_story_agent() -> Agent:
    """Return the User Story and Assignment agent."""
    story_config = AgentConfig(
        role="User Story Writer",
        goal=(
            "Generate structured user stories and assign them to simulated "
            "developers based on the PO and Tech Lead discussion."
        ),
        backstory=(
            "You are a detail-oriented agile practitioner who writes clear user "
            "stories with acceptance criteria, priorities, and assignments."
        ),
    )
    return create_agent(story_config)


def get_evaluator_agent() -> Agent:
    """Return the Evaluator agent acting as an LLM judge."""
    evaluator_config = AgentConfig(
        role="Evaluator Agent",
        goal=(
            "Objectively evaluate the quality of extracted requirements, "
            "user stories, assignments, and agent communication, and return "
            "a structured JSON score report."
        ),
        backstory=(
            "You are an impartial LLM judge. You review the original inputs, "
            "the conversation between the agents, and the final user stories. "
            "You score the workflow across multiple dimensions and provide "
            "clear reasoning for each score."
        ),
    )
    return create_agent(evaluator_config)


