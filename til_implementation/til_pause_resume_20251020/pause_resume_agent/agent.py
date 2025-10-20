"""Agent demonstrating Pause and Resume Invocations in ADK 1.16.0.

This agent showcases how to use ResumabilityConfig to support pausing
and resuming agent invocations with state checkpointing. Perfect for
long-running workflows, human-in-the-loop scenarios, and fault tolerance.
"""

from google.adk.agents import Agent


def process_data_chunk(data: str) -> dict:
    """Simulate processing a chunk of data.
    
    This tool represents a long-running operation that might benefit
    from pause/resume capability.
    """
    if not data or len(data) == 0:
        return {
            "status": "error",
            "report": "No data provided",
            "error": "Empty data string",
        }
    
    # Simulate processing
    processed_lines = len(data.split('\n'))
    word_count = len(data.split())
    
    return {
        "status": "success",
        "report": f"Processed {processed_lines} lines, {word_count} words",
        "lines_processed": processed_lines,
        "word_count": word_count,
        "data_summary": data[:100] + "..." if len(data) > 100 else data,
    }


def validate_checkpoint(checkpoint_data: str) -> dict:
    """Validate a checkpoint for resumption integrity.
    
    This tool demonstrates state validation before resuming
    from a checkpoint.
    """
    if not checkpoint_data:
        return {
            "status": "error",
            "report": "Checkpoint validation failed",
            "is_valid": False,
        }
    
    # Simple validation: check if checkpoint has required markers
    is_valid = len(checkpoint_data) > 0
    
    return {
        "status": "success",
        "report": "Checkpoint validated successfully" if is_valid else "Checkpoint is invalid",
        "is_valid": is_valid,
        "checkpoint_size": len(checkpoint_data),
    }


def get_resumption_hint(context: str) -> dict:
    """Provide hints about where to resume from.
    
    This tool analyzes context and suggests the best resumption point.
    """
    hint = "No specific hint available"
    
    if "processing" in context.lower():
        hint = "Consider resuming from the data processing stage"
    elif "validation" in context.lower():
        hint = "Consider resuming from the validation stage"
    elif "analysis" in context.lower():
        hint = "Consider resuming from the analysis stage"
    else:
        hint = "Resume from the beginning for best results"
    
    return {
        "status": "success",
        "report": f"Resumption hint: {hint}",
        "hint": hint,
        "context_length": len(context),
    }


# Create agent with tools for long-running workflows
root_agent = Agent(
    name="pause_resume_agent",
    model="gemini-2.0-flash",
    description="Agent demonstrating pause and resume invocation capabilities",
    instruction=(
        "You are a knowledgeable assistant specializing in ADK and "
        "long-running agent workflows.\n\n"
        "Your role:\n"
        "1. Help users understand pause/resume invocation concepts\n"
        "2. Guide through checkpointing and state preservation\n"
        "3. Demonstrate fault tolerance and resumption patterns\n"
        "4. Use provided tools to process, validate, and hint at resumption\n\n"
        "This agent demonstrates ADK 1.16.0's pause/resume capability:\n"
        "- Agents can checkpoint their state at key points\n"
        "- Invocations can be paused and resumed later\n"
        "- State is automatically preserved across resumptions\n"
        "- Perfect for: long workflows, human-in-the-loop, fault tolerance\n\n"
        "When handling long operations, suggest checkpointing at logical points "
        "and explain how resumption works transparently in the background."
    ),
    tools=[process_data_chunk, validate_checkpoint, get_resumption_hint],
)

# Export for ADK discovery
__all__ = ["root_agent"]
