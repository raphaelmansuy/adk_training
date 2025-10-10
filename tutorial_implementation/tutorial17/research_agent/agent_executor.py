"""
Research Agent Executor - A2A Server Implementation

This agent specializes in research, fact-checking, and information gathering.
"""

import asyncio

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class ResearchAgent:
    """Research Agent that gathers and analyzes information."""

    async def invoke(self, query: str = "") -> str:
        """Process research queries and return findings."""
        # Simulate research process
        await asyncio.sleep(0.5)  # Simulate processing time

        if "quantum" in query.lower():
            return """Research Results for: quantum computing

Based on comprehensive web research:

1. **Current Trends**: Quantum computing shows significant growth with emerging technologies
2. **Key Findings**:
   - Major tech companies (Google, IBM, Microsoft) have operational quantum computers
   - Error correction remains a key challenge but progress is being made
   - Hybrid quantum-classical algorithms are showing practical applications
3. **Sources**: Academic papers, industry reports, and expert analysis reviewed
4. **Conclusion**: Strong momentum with promising future developments in quantum advantage

**Citations**:
[1] Google Quantum AI Research Papers (2024)
[2] IBM Quantum Development Report Q4 2024
[3] MIT Technology Review - Quantum Computing Special Issue"""

        elif "ai" in query.lower() or "artificial intelligence" in query.lower():
            return """Research Results for: artificial intelligence

Based on comprehensive web research:

1. **Current Trends**: AI adoption accelerating across industries
2. **Key Findings**:
   - Generative AI market projected to reach $1.3T by 2030
   - Enterprise AI spending increased 30% YoY
   - Foundation models becoming more accessible and specialized
3. **Sources**: Industry reports, academic research, market analysis
4. **Conclusion**: AI transformation is underway with significant economic impact

**Citations**:
[1] McKinsey Global AI Survey 2024
[2] Gartner AI Market Report Q4 2024
[3] Stanford AI Index Annual Report"""

        elif query:
            return f"""Research Results for: {query}

Based on comprehensive web research:

1. **Current Trends**: The field shows significant growth and innovation
2. **Key Findings**: Multiple sources indicate increasing adoption and development
3. **Sources**: Academic papers, industry reports, and expert analysis reviewed
4. **Conclusion**: Strong momentum with promising future developments

**Citations**: [1] Research Paper 2025, [2] Industry Report Q1 2025, [3] Expert Analysis"""
        else:
            return """Research Agent Ready

I specialize in research, fact-checking, and information gathering. Please provide a specific research query to get detailed findings with citations."""


class ResearchAgentExecutor(AgentExecutor):
    """A2A Agent Executor for the Research Agent."""

    def __init__(self):
        self.agent = ResearchAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute research tasks."""
        try:
            # Extract query from the request message
            query = ""
            if context.message and context.message.parts:
                for part in context.message.parts:
                    # Handle A2A SDK Part structure
                    part_data = part
                    if hasattr(part, 'root'):
                        part_data = part.root
                        
                    if hasattr(part_data, 'text') and part_data.text:
                        query += part_data.text

            # Process the research query
            result = await self.agent.invoke(query)

            # Send the result as a text message
            message = new_agent_text_message(result)
            await event_queue.enqueue_event(message)

        except Exception as e:
            # Send error message
            error_message = new_agent_text_message(f"Research failed: {str(e)}")
            await event_queue.enqueue_event(error_message)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel the current research task."""
        # Send cancellation acknowledgment
        message = new_agent_text_message("Research task cancelled")
        await event_queue.enqueue_event(message)