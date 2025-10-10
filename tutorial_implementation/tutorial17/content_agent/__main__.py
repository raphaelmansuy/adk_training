"""
Content Agent - A2A Server

A specialized agent for content creation, writing, and summarization.
Runs as an A2A server on localhost:9003
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
from .agent_executor import ContentAgentExecutor


def main():
    """Start the Content Agent A2A server."""

    # Define the content creation skill
    content_skill = AgentSkill(
        id='content_creation',
        name='Content Creation and Writing',
        description='Create written content, articles, summaries, and documentation',
        tags=['content', 'writing', 'summary', 'articles'],
        examples=[
            'Write an executive summary',
            'Create a blog article about technology trends',
            'Generate a content summary for research findings'
        ],
    )

    # Create the agent card
    agent_card = AgentCard(
        name='Content Creation Agent',
        description='Specialized agent for creating written content, articles, summaries, and documentation',
        url='http://localhost:9003/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[content_skill],
        supports_authenticated_extended_card=False,
    )

    # Create the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=ContentAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create and start the A2A server
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("🚀 Starting Content Agent A2A Server on http://localhost:9003")
    print("✍️ Agent specializes in content creation and writing")
    print("🔗 Agent card available at: http://localhost:9003/.well-known/agent.json")

    uvicorn.run(server.build(), host='0.0.0.0', port=9003)


if __name__ == '__main__':
    main()