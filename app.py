import streamlit as st

from crew.crew_runner import run_crew
from utils.validators import validate_inputs


def main() -> None:
    """Streamlit entry point for the AI Product Owner multi-agent system UI."""
    st.set_page_config(page_title="AI Product Owner Automation", layout="wide")

    if "run_id" not in st.session_state:
        st.session_state.run_id = 0
    if "stories_table" not in st.session_state:
        st.session_state.stories_table = None
    if "evaluation" not in st.session_state:
        st.session_state.evaluation = None

    st.title("AI Product Owner Automation")
    st.write(
        "Provide Slack messages, meeting notes, and developer names. "
        "The agents will analyze the input, generate user stories with "
        "assignments, and an evaluator agent will score the results."
    )

    # Section 1: Input Panel
    st.markdown("### Input Panel")
    col_input, _ = st.columns([3, 2])
    with col_input:
        slack_messages = st.text_area(
            "Slack Messages",
            height=200,
            placeholder="Paste relevant Slack conversation here...",
        )
        meeting_notes = st.text_area(
            "Meeting Notes",
            height=200,
            placeholder="Paste meeting notes or transcript here...",
        )
        developer_names = st.text_input(
            "Developer names (comma separated, e.g. Ali, Raza, Ahmed)",
            value="",
        )

        start_button = st.button("Start Agent")

    valid, error_message = validate_inputs(slack_messages, meeting_notes)
    if start_button:
        if not valid:
            st.error(error_message)
        else:
            st.session_state.run_id += 1

    # Only run when we have a trigger and some input
    if st.session_state.run_id and valid:
        # Section 2: Agent Communication
        st.markdown("### Agent Communication")
        with st.spinner("Agents are analyzing inputs and preparing user stories..."):
            result = run_crew(
                slack_messages=slack_messages,
                meeting_notes=meeting_notes,
            )

        st.session_state.stories_table = result.get("stories_table")
        st.session_state.evaluation = result.get("evaluation")

        with st.chat_message("assistant"):
            st.markdown("**Product Owner Agent** has analyzed the Slack messages and meeting notes.")
        with st.chat_message("assistant"):
            st.markdown("**Tech Lead Agent** has produced a technical breakdown and suggested ownership.")
        with st.chat_message("assistant"):
            st.markdown("**User Story Agent** has generated structured user stories with assignments.")
        with st.chat_message("assistant"):
            st.markdown("**Evaluator Agent** has scored the output on the defined metrics.")

        # Section 3: Assignment Permission
        st.markdown("### Assignment Permission")
        stories_table = st.session_state.stories_table
        if stories_table is not None:
            st.write("Review the proposed assignments before finalizing.")
            choice = st.radio(
                "Approve assignments?",
                options=["Yes", "Modify"],
                horizontal=True,
            )

            if choice == "Modify":
                edited_table = st.data_editor(
                    stories_table,
                    num_rows="dynamic",
                    key="edited_stories_table",
                )
                stories_table = edited_table
                st.session_state.stories_table = edited_table
            else:
                st.dataframe(stories_table)
        else:
            st.info("No user stories generated.")

        # Section 4: Final User Stories
        st.markdown("### Final User Stories")
        if stories_table is not None:
            st.dataframe(stories_table)

        # Section 5: Performance Evaluation
        st.markdown("### Performance Evaluation")
        evaluation = st.session_state.evaluation
        if evaluation:
            metrics_rows = []
            for key in [
                "extraction_accuracy",
                "user_story_quality",
                "assignment_accuracy",
                "communication_quality",
            ]:
                metric = evaluation.get(key, {})
                metrics_rows.append(
                    {
                        "Metric": key.replace("_", " ").title(),
                        "Score": metric.get("score", 0),
                        "Reasoning": metric.get("reasoning", ""),
                    }
                )

            st.table(metrics_rows)

            final_score = evaluation.get("final_score_out_of_10000", 0)
            st.subheader(f"Final Score: {final_score} / 10,000")

            st.markdown("#### Manual Override")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                extraction_override = st.number_input(
                    "Extraction Accuracy",
                    min_value=0,
                    max_value=100,
                    value=int(evaluation["extraction_accuracy"]["score"]),
                )
            with col2:
                story_quality_override = st.number_input(
                    "User Story Quality",
                    min_value=0,
                    max_value=100,
                    value=int(evaluation["user_story_quality"]["score"]),
                )
            with col3:
                assignment_override = st.number_input(
                    "Assignment Accuracy",
                    min_value=0,
                    max_value=100,
                    value=int(evaluation["assignment_accuracy"]["score"]),
                )
            with col4:
                communication_override = st.number_input(
                    "Communication Quality",
                    min_value=0,
                    max_value=100,
                    value=int(evaluation["communication_quality"]["score"]),
                )

            if st.button("Recalculate Score"):
                weighted_score = (
                    extraction_override * 0.30
                    + story_quality_override * 0.30
                    + assignment_override * 0.25
                    + communication_override * 0.15
                )
                manual_final = int(weighted_score * 100)
                st.markdown(
                    f"**LLM Score:** {final_score} / 10,000  \n"
                    f"**Manual Score:** {manual_final} / 10,000"
                )
        else:
            st.info("Evaluation is not available for this run.")


if __name__ == "__main__":
    main()


