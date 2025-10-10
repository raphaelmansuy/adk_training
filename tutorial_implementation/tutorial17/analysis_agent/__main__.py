"""
Analysis Agent - A2A Server

A specialized agent for data analysis, statistical insights, and quantitative analysis.
Runs as an A2A server on localhost:9002
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
from .agent_executor import AnalysisAgentExecutor


def main():
    """Start the Analysis Agent A2A server."""

    # Define the analysis skill
    analysis_skill = AgentSkill(
        id='analysis',
        name='Data Analysis and Insights',
        description='Analyze data, generate statistical insights, and provide quantitative analysis',
        tags=['analysis', 'data', 'statistics', 'insights'],
        examples=[
            'Analyze market growth trends',
            'Provide performance metrics analysis',
            'Generate statistical insights for dataset X'
        ],
    )

    # Create the agent card
    agent_card = AgentCard(
        name='Data Analysis Agent',
        description='Specialized agent for data analysis, statistical insights, and quantitative research',
        url='http://localhost:9002/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[analysis_skill],
        supports_authenticated_extended_card=False,
    )

    # Create the request handler
    request_handler = DefaultRequestHandler(
        agent_executor=AnalysisAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # Create and start the A2A server
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("🚀 Starting Analysis Agent A2A Server on http://localhost:9002")
    print("📊 Agent specializes in data analysis and statistical insights")
    print("🔗 Agent card available at: http://localhost:9002/.well-known/agent.json")

    uvicorn.run(server.build(), host='0.0.0.0', port=9002)


if __name__ == '__main__':
    main()