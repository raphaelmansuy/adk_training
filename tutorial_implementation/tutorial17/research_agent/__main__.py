"""
Research Agent - A2A Server

A specialized agent for research, information gathering, and fact-checking.
Runs as an A2A server on localhost:9001
"""

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from .agent_executor import ResearchAgentExecutor


def main():
    """Start the Research Agent A2A server."""

    # Define the research skill
    research_skill = AgentSkill(
        id='research',
        name='Research and Analysis',
        description='Conduct comprehensive research on topics, gather facts, and provide citations',
        tags=['research', 'analysis', 'facts', 'information'],
        examples=[
            'Research quantum computing trends',
            'Find information about AI adoption',
            'Analyze market trends for technology X'
        ],
    )

    # Create the agent card
    agent_card = AgentCard(
        name='Research Specialist Agent',
        description='Specialized agent for conducting research, fact-checking, and information gathering',
        url='http://localhost:9001/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[research_skill],
        supports_authenticated_extended_card=False,
    )

    # Create the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=ResearchAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create and start the A2A server
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("🚀 Starting Research Agent A2A Server on http://localhost:9001")
    print("📚 Agent specializes in research and information gathering")
    print("🔗 Agent card available at: http://localhost:9001/.well-known/agent.json")

    uvicorn.run(server.build(), host='0.0.0.0', port=9001)


if __name__ == '__main__':
    main()