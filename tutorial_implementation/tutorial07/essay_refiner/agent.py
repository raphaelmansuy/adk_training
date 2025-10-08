from __future__ import annotations

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext

# ===== Exit Tool for Loop Termination =====
def exit_loop(tool_context: ToolContext):
    """
    Signal that the essay refinement is complete.
    Called by the refiner when critic approves the essay.
    """
    print(f"  [Exit Loop] Called by {tool_context.agent_name} - Essay approved!")
    tool_context.actions.end_of_agent = True  # Signal to stop looping
    # Return a minimal valid content part so the backend always produces a valid LlmResponse
    return {"text": "Loop exited successfully. The agent has determined the task is complete."}

# =====================================================
# PHASE 1: Initial Writer (Runs ONCE before loop)
# =====================================================
initial_writer = Agent(
    name="InitialWriter",
    model="gemini-2.0-flash",
    description="Writes the first draft of an essay",
    instruction=(
        "You are a creative writer. Write a first draft essay on the topic "
        "requested by the user.\n"
        "\n"
        "Write 3-4 paragraphs:\n"
        "- Opening paragraph with thesis\n"
        "- 1-2 body paragraphs with supporting points\n"
        "- Concluding paragraph\n"
        "\n"
        "Don't worry about perfection - this is just the first draft.\n"
        "\n"
        "Output ONLY the essay text, no meta-commentary."
    ),
    output_key="current_essay"  # Saves to state
)

# =====================================================
# PHASE 2: Refinement Loop (Runs REPEATEDLY)
# =====================================================

# ===== Loop Agent 1: Critic =====
critic = Agent(
    name="Critic",
    model="gemini-2.0-flash",
    description="Evaluates essay quality and provides feedback",
    instruction=(
        "You are an experienced essay critic and teacher. Review the essay below "
        "and evaluate its quality.\n"
        "\n"
        "**Essay to Review:**\n"
        "{current_essay}\n"
        "\n"
        "**Evaluation Criteria:**\n"
        "- Clear thesis and organization\n"
        "- Strong supporting arguments\n"
        "- Good grammar and style\n"
        "- Engaging and coherent writing\n"
        "\n"
        "**Your Task:**\n"
        "IF the essay meets ALL criteria well (doesn't need to be perfect, just solid):\n"
        "  Output EXACTLY this phrase: 'APPROVED - Essay is complete.'\n"
        "\n"
        "ELSE if essay needs improvement:\n"
        "  Provide 2-3 specific, actionable improvements. Be constructive and clear.\n"
        "  Example: 'The thesis is vague - make it more specific about X.'\n"
        "\n"
        "Output ONLY the approval phrase OR the specific feedback."
    ),
    output_key="critique"  # Saves feedback to state
)

# ===== Loop Agent 2: Refiner =====
refiner = Agent(
    name="Refiner",
    model="gemini-2.0-flash",
    tools=[exit_loop],  # Provide exit tool!
    description="Improves essay based on critique or signals completion",
    instruction=(
        "You are an essay editor. Read the critique below and take appropriate action.\n"
        "\n"
        "**Current Essay:**\n"
        "{current_essay}\n"
        "\n"
        "**Critique:**\n"
        "{critique}\n"
        "\n"
        "**Your Task:**\n"
        "IF the critique says 'APPROVED - Essay is complete.':\n"
        "  Call the 'exit_loop' function immediately. Do NOT output any text.\n"
        "  This means your response should ONLY be the function call, nothing else.\n"
        "\n"
        "ELSE (the critique contains improvement suggestions):\n"
        "  Apply the suggested improvements to create a better version of the essay.\n"
        "  Output ONLY the improved essay text, no explanations or meta-commentary.\n"
        "  Do NOT call any functions when improving the essay.\n"
        "\n"
        "IMPORTANT: You must EITHER call exit_loop OR output improved essay text.\n"
        "Never do both in the same response."
    ),
    output_key="current_essay"  # Overwrites essay with improved version!
)

# ===== Create Refinement Loop =====
refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[
        critic,   # Step 1: Evaluate
        refiner   # Step 2: Improve OR exit
    ],
    max_iterations=5  # Safety limit - stops after 5 loops max
)

# =====================================================
# COMPLETE SYSTEM: Initial Draft + Refinement Loop
# =====================================================
essay_refinement_system = SequentialAgent(
    name="EssayRefinementSystem",
    sub_agents=[
        initial_writer,    # Phase 1: Write first draft (once)
        refinement_loop    # Phase 2: Refine iteratively (loop)
    ],
    description="Complete essay writing and refinement system"
)

# MUST be named root_agent for ADK
root_agent = essay_refinement_system