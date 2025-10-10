"""
Content Agent Executor - A2A Server Implementation

This agent specializes in content creation, writing, and summarization.
"""

import asyncio
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.utils import new_agent_text_message


class ContentAgent:
    """Content Agent that creates written content and summaries."""

    async def invoke(self, query: str) -> str:
        """Process content creation queries and return written content."""
        # Simulate content creation process
        await asyncio.sleep(0.5)  # Simulate processing time

        if "summary" in query.lower() or "executive" in query.lower():
            return """# Executive Summary

## Overview

This comprehensive analysis examines the current state and future prospects of the technology landscape. Our research indicates significant opportunities for growth and innovation in this rapidly evolving field.

## Key Findings

- **Market Opportunity**: Substantial growth potential identified with a projected CAGR of 22%
- **Technology Trends**: Emerging solutions showing promise in enterprise adoption
- **Competitive Landscape**: Several key players actively innovating and capturing market share

## Strategic Implications

Organizations should consider strategic investments in this area, focusing on:
- Technology adoption and integration
- Talent development and training
- Partnership and ecosystem building

## Conclusion

The analysis suggests a positive outlook with clear strategic directions for success. Companies that invest early in these technologies are likely to gain significant competitive advantages.

## Recommendations

1. **Immediate Actions**: Begin pilot programs within 3-6 months
2. **Medium-term Goals**: Achieve full production deployment within 12-18 months
3. **Long-term Vision**: Establish leadership position in the evolving market

*This summary is based on comprehensive research and industry analysis.*"""

        elif "article" in query.lower() or "blog" in query.lower():
            return """# The Future of Technology: Trends and Innovations

## Introduction

In an era of rapid technological advancement, understanding emerging trends is crucial for organizations seeking to maintain competitive advantage. This article explores the key technology trends shaping our future and their potential impact on businesses and society.

## Current Technology Landscape

### Artificial Intelligence and Machine Learning

The proliferation of AI and ML technologies continues to accelerate, with applications spanning from automated customer service to predictive analytics. Organizations are increasingly recognizing AI not just as a tool, but as a strategic imperative.

### Cloud Computing Evolution

Cloud technologies have matured from basic infrastructure services to sophisticated platforms offering AI, analytics, and edge computing capabilities. The shift towards multi-cloud and hybrid strategies reflects the need for flexibility and resilience.

### Edge Computing and IoT

The growth of Internet of Things (IoT) devices and the need for real-time processing have driven the adoption of edge computing. This distributed computing paradigm brings processing closer to data sources, reducing latency and bandwidth requirements.

## Emerging Trends

### Quantum Computing

While still in its early stages, quantum computing promises to solve complex problems that are currently intractable for classical computers. Industries such as pharmaceuticals, materials science, and financial modeling stand to benefit significantly.

### Sustainable Technology

Environmental consciousness is driving innovation in green technologies, from energy-efficient computing to carbon-neutral data centers. Organizations are increasingly evaluating technology solutions based on their environmental impact.

### Human-AI Collaboration

The future lies not in replacing human workers, but in augmenting their capabilities. Technologies that enhance human productivity while maintaining ethical standards will be key differentiators.

## Strategic Considerations

### Investment Priorities

Organizations should focus on technologies that align with their strategic objectives while building flexible platforms that can adapt to future changes.

### Skills and Talent

The technology landscape demands new skills. Organizations must invest in training and development to prepare their workforce for the future.

### Ethical and Responsible Innovation

As technologies become more powerful, ensuring ethical development and deployment becomes paramount. Organizations should establish clear guidelines and governance frameworks.

## Conclusion

The technology landscape is evolving at an unprecedented pace. Organizations that embrace change, invest in the right technologies, and develop the necessary skills will be best positioned to thrive in this dynamic environment.

Success will depend not just on adopting new technologies, but on integrating them thoughtfully into organizational culture and processes."""

        else:
            return """# Content Summary

## Executive Overview

This comprehensive analysis examines the current state and future prospects of the topic under investigation. Our research indicates significant opportunities for growth and innovation in this space.

## Key Findings

- **Market Opportunity**: Substantial growth potential identified
- **Technology Trends**: Emerging solutions showing promise
- **Competitive Landscape**: Several key players actively innovating

## Strategic Implications

Organizations should consider strategic investments in this area, focusing on technology adoption and market positioning.

## Conclusion

The analysis suggests a positive outlook with clear strategic directions for success.

*Content generated based on comprehensive research and analysis.*"""


class ContentAgentExecutor(AgentExecutor):
    """A2A Agent Executor for the Content Agent."""

    def __init__(self):
        self.agent = ContentAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute content creation tasks."""
        try:
            # Extract query from the request
            query = ""
            if context.message and context.message.parts:
                for part in context.message.parts:
                    # Handle nested root structure in A2A SDK
                    part_data = part
                    if hasattr(part, 'root'):
                        part_data = part.root
                        
                    if hasattr(part_data, 'text'):
                        query += part_data.text

            if not query:
                query = "general content creation inquiry"

            # Process the content creation query
            result = await self.agent.invoke(query)

            # Send the result as a text message
            message = new_agent_text_message(result)
            await event_queue.enqueue_event(message)

        except Exception as e:
            # Send error message
            error_message = new_agent_text_message(f"Content creation failed: {str(e)}")
            await event_queue.enqueue_event(error_message)

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel the current content creation task."""
        # Send cancellation acknowledgment
        message = new_agent_text_message("Content creation task cancelled")
        await event_queue.enqueue_event(message)