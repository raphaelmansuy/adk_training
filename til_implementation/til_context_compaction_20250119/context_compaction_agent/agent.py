"""Agent demonstrating Context Compaction in ADK 1.16.

This agent showcases how to use EventsCompactionConfig to automatically
summarize old conversation history and reduce token usage in long
conversations.
"""

from google.adk.agents import Agent

def summarize_text(text: str) -> dict:
  """Utility tool to summarize text chunks."""
  if len(text) > 200:
    return {
        "status": "success",
        "report": f"Summarized {len(text)} chars",
        "summary": text[:100] + "...",
    }
  return {
      "status": "success",
      "report": "Text is short enough",
      "summary": text,
  }

def calculate_complexity(question: str) -> dict:
  """Analyze question complexity to determine response depth."""
  word_count = len(question.split())
  if word_count > 20:
    complexity = "high"
  elif word_count > 10:
    complexity = "medium"
  else:
    complexity = "low"

  return {
      "status": "success",
      "report": f"Question complexity: {complexity}",
      "complexity_level": complexity,
      "word_count": word_count,
  }

# Create agent with built-in tools
root_agent = Agent(
    name="context_compaction_agent",
    model="gemini-2.0-flash",
    description="Agent demonstrating context compaction for long conversations",
    instruction=(
        "You are a knowledgeable assistant specializing in ADK and agent "
        "development.\n\n"
        "Your role:\n"
        "1. Answer questions about Google ADK and AI agents\n"
        "2. Provide code examples when relevant\n"
        "3. Explain best practices for agent development\n"
        "4. Use the provided tools to analyze questions and summarize content\n\n"
        "This agent is designed to handle long, multi-turn conversations. "
        "Behind the scenes, context compaction automatically summarizes older "
        "messages to keep the conversation efficient.\n\n"
        "You don't need to manage this - just respond naturally to the user, "
        "and the system handles token optimization automatically."
    ),
    tools=[summarize_text, calculate_complexity],
)

# Export for ADK discovery
__all__ = ["root_agent"]
