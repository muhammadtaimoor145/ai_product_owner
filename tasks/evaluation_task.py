from crewai import Task

from config.agents_config import get_evaluator_agent


def create_evaluation_task(
    original_input: str,
    agent_communication: str,
    user_stories_json: str,
) -> Task:
    """Create task for Evaluator agent to score the workflow output."""
    evaluator = get_evaluator_agent()
    return Task(
        description=(
            "You are an Evaluator Agent acting as an LLM judge.\n\n"
            "You receive:\n"
            "1) The original input (Slack messages and meeting notes)\n"
            "2) The communication between the Product Owner, Tech Lead, and Story agents\n"
            "3) The final user stories and assignments as JSON\n\n"
            "Your job is to score the overall workflow on four metrics, each from 0 to 100:\n"
            "- Extraction Accuracy: Did the agents find all key requirements from the input?\n"
            "- User Story Quality: Are stories well-structured with acceptance criteria and priority?\n"
            "- Assignment Accuracy: Are tasks assigned to appropriate developers based on context?\n"
            "- Communication Quality: Was the PO and Tech Lead conversation clear and logical?\n\n"
            "Use the following inputs:\n"
            "Original input:\n{original_input}\n\n"
            "Agent communication transcript:\n{agent_communication}\n\n"
            "Final user stories JSON:\n{user_stories_json}\n\n"
            "Calculate the weighted score using this formula:\n"
            "weighted_score = (\n"
            "    extraction_accuracy * 0.30 +\n"
            "    user_story_quality * 0.30 +\n"
            "    assignment_accuracy * 0.25 +\n"
            "    communication_quality * 0.15\n"
            ")\n"
            "final_score = weighted_score * 100\n\n"
            "Return ONLY strict JSON with this exact structure and no extra text:"
        ),
        expected_output=(
            '{\n'
            '  "extraction_accuracy": { "score": 0, "reasoning": "" },\n'
            '  "user_story_quality": { "score": 0, "reasoning": "" },\n'
            '  "assignment_accuracy": { "score": 0, "reasoning": "" },\n'
            '  "communication_quality": { "score": 0, "reasoning": "" },\n'
            '  "weighted_total": 0,\n'
            '  "final_score_out_of_10000": 0\n'
            '}'
        ),
        agent=evaluator,
    )


