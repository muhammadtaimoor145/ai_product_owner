## AI Product Owner Multi-Agent System

## Problem Statement

### What Problem Does This Agent Solve?

Product Owners, Product Managers, and Project Managers spend a 
significant portion of their time on low-value coordination tasks — 
extracting requirements from client meetings, converting discussion 
notes into user stories, running grooming sessions with developers, 
and manually assigning tasks across the team.

This constant context-switching pulls them away from high-value 
strategic work like roadmap planning, stakeholder alignment, and 
product decision making.

Meanwhile developers sit idle waiting for properly structured user 
stories before they can begin work. This creates a bottleneck that 
slows down the entire development cycle.

### Why Did I Choose This Problem?

This problem sits at the intersection of two expensive inefficiencies:

**1. Wasted PM time**
Research shows PMs spend up to 60% of their time in meetings and 
on administrative tasks rather than actual product thinking. Writing 
and grooming user stories is one of the most time-consuming of those 
tasks.

**2. Developer idle time**
Developers cannot start work without clear requirements. Every hour 
a developer waits for a user story is direct revenue loss for the 
company. This is a completely avoidable bottleneck.

### Why Is This My #1 Priority?

This problem is my top priority for three reasons:

First, it is universal. Every software team regardless of size, 
industry or methodology faces this exact bottleneck. The solution 
has a massive addressable market.

Second, it is solvable with AI today. Meeting transcripts and Slack 
conversations contain all the information needed to generate user 
stories. The data exists — it just needs an intelligent agent to 
process it.

Third, it is personal. As someone who has worked closely with 
development teams, I have directly experienced how much time is 
lost between a client conversation and a developer actually starting 
work. This agent eliminates that gap entirely.

### What Does The Agent Specifically Do?

This agent takes two inputs that already exist in every team's 
workflow — Slack messages and meeting notes — and automatically:

- Extracts all product requirements and decisions
- Generates properly structured user stories with acceptance criteria
- Assigns stories to the right developers based on context
- Requests human approval before finalizing assignments

No new tools, no new processes. The agent fits into how teams 
already work and removes the manual overhead entirely.

we can integrate this with tools like meet or slack using webhooks , But currently this functionality is not there

### Agent Workflow

This system uses four specialized AI agents, each with a distinct 
role. They work in sequence, passing information to each other like 
a real product team would.

---

#### Agent 1: Product Owner Agent
Reads the Slack messages and meeting notes provided as input.
Understands the business requirements and client needs.
Explains the requirements in clear product language to the Tech Lead.

#### Agent 2: Tech Lead Agent
Receives the requirements from the Product Owner Agent.
Breaks them down into technical tasks.
Identifies which developer is best suited for each task based on 
the context provided in the input.

#### Agent 3: User Story Agent
Takes the output from the PO and Tech Lead conversation.
Generates properly structured user stories for each requirement.
Assigns each story to a developer.
Before finalizing, it asks the user for approval on the assignments.
User can modify any assignment before confirming.

#### Agent 4: Evaluator Agent
After all agents finish, this agent acts as an independent judge.
It reviews the entire output and scores the system performance 
across four criteria.

---

### Performance Metric

The Evaluator Agent scores the system out of 10,000 using four 
metrics:

| Metric | What It Measures | Weight |
|---|---|---|
| Extraction Accuracy | Did the agent find all requirements from the input? | 30% |
| User Story Quality | Are stories properly formatted with acceptance criteria and priority? | 30% |
| Assignment Accuracy | Were tasks assigned to the right developers based on context? | 25% |
| Communication Quality | Was the conversation between PO and Tech Lead clear and logical? | 15% |

### Score Calculation
```
final_score = (
    extraction_accuracy  × 0.30 +
    user_story_quality   × 0.30 +
    assignment_accuracy  × 0.25 +
    communication_quality × 0.15
) × 100
```

Each metric is scored out of 100 by the Evaluator Agent with a 
written reason explaining the score.

Example output:
```json
{
  "extraction_accuracy":   { "score": 85, "reasoning": "Found 5 out of 6 requirements. Missed email verification requirement from Slack." },
  "user_story_quality":    { "score": 90, "reasoning": "All stories follow correct format with acceptance criteria and priority assigned." },
  "assignment_accuracy":   { "score": 80, "reasoning": "4 out of 5 assignments matched developer context from meeting notes." },
  "communication_quality": { "score": 88, "reasoning": "PO explained requirements clearly. Tech Lead provided detailed technical breakdown." },
  "weighted_total":        86.25,
  "final_score_out_of_10000": 8625
}
```

### Manual Score Override

If the user disagrees with any score given by the Evaluator Agent,
they can manually adjust each metric score directly in the UI.
The system will automatically recalculate the weighted total and 
final score based on the updated values.

This ensures the evaluation reflects both AI judgment and human 
expertise.

### Benchmarking Against Plain Claude

To measure how much value our multi-agent system adds, we ran the 
same input through both our agent system and plain Claude with no 
customization.

**Test Setup**
- Same Slack messages and meeting notes used as input for both
- Same evaluation criteria applied to both outputs
- Evaluator Agent scored both results using identical metrics
- Test was repeated multiple times to check consistency

**Key Finding**

Plain Claude produced a higher raw score on some individual runs 
but the score changed significantly across multiple simulations 
with the same input. This inconsistency indicates that plain Claude 
is not reliable for this specific use case — its output format, 
level of detail, and developer assignments varied every time.

Our agent system produced consistent, structured output across all 
test runs because the agents follow strict role definitions, output 
formats, and evaluation criteria defined in the system.

**Conclusion**

A reliable system is more valuable than an occasionally high 
scoring one. Our multi-agent setup trades some raw flexibility for 
consistency, structure, and predictability — which is exactly what 
a product team needs when generating user stories from meeting input.

### Future Advancements

The current system accepts manual input as a starting point. 
The following enhancements are planned to make the system 
production-ready and deeply integrated into real team workflows.

---

#### 1. Webhook Integrations
Connect the agent directly to tools teams already use — Google Meet, 
Slack, Jira, Linear, and Notion. Instead of pasting input manually, 
the agent will trigger automatically when a meeting ends or a new 
Slack thread is created. User stories will be pushed directly into 
the project management tool of choice without any human copy-pasting.

#### 2. Learning Engine
Every time a user manually overrides a score or leaves a comment 
on the evaluation, that feedback will be saved to a backend database. 
Over time the agent learns from these corrections, improves its 
scoring accuracy, and better understands team-specific preferences. 
This turns the system from a static tool into one that gets smarter 
with every use.

#### 3. Runtime Prompt Customization
Users will be able to adjust agent roles, responsibilities, and 
instructions directly from the UI without touching any code. 
For example a team can redefine what the Product Owner Agent 
prioritizes or change how the Tech Lead Agent estimates effort. 
This makes the system adaptable to any team structure or workflow 
without requiring developer involvement.



### Tech Stack
- **Python** 3.11+
- **CrewAI** for multi-agent orchestration
- **OpenAI GPT-4.1-nano** (configurable via environment variable)
- **Streamlit** for the frontend UI
- **python-dotenv** for environment variables

### Project Structure
- `app.py` – Streamlit entry point and UI
- `config/llm_config.py` – LLM and model configuration
- `config/agents_config.py` – Agent roles, goals, backstories
- `agents/` – (optional future per-agent modules)
- `tasks/` – Analysis, communication, and assignment tasks
- `crew/crew_runner.py` – CrewAI crew setup and execution
- `utils/formatters.py` – Output formatting helpers
- `utils/validators.py` – Input validation helpers

### Setup
1. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables** (e.g. in a `.env` file next to `app.py`):
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-4.1-nano
   ```

### Running the App
Run the Streamlit app from the project root:
```bash
streamlit run app.py
```

Paste relevant Slack messages and meeting notes into the sidebar, click **"Analyze and Generate User Stories"**, and review the generated stories table.

