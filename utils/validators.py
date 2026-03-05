from typing import Tuple


def validate_inputs(slack_messages: str, meeting_notes: str) -> Tuple[bool, str]:
    """Validate that at least one of the input fields has content."""
    if not slack_messages.strip() and not meeting_notes.strip():
        return False, "Please provide Slack messages, meeting notes, or both."
    return True, ""


