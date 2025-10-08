"""
Tutorial 06: Multi-Agent Systems - Content Publishing System

This tutorial demonstrates sophisticated multi-agent orchestration by combining
Sequential and Parallel agents in nested workflows. The content publishing system
runs parallel research pipelines (news, social, expert) then creates content
through sequential refinement (write, edit, format).
"""

from __future__ import annotations

from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

# ============================================================================
# PARALLEL BRANCH 1: News Research Pipeline
# ============================================================================

news_fetcher = Agent(
    name="news_fetcher",
    model="gemini-2.0-flash",
    description="Fetches current news articles using Google Search",
    instruction=(
        "You are a news researcher. Based on the user's topic, search for "
        "current news articles and recent developments.\n"
        "\n"
        "Use the google_search tool to find 3-4 current news articles.\n"
        "Focus on recent, credible news sources from the past 6 months.\n"
        "\n"
        "Output a bulleted list with:\n"
        "• Source + Headline + Brief summary\n"
        "• Include publication dates when available\n"
        "\n"
        "Search query should be: '[topic] news recent developments site:reputable-news-sites'"
    ),
    tools=[google_search],
    output_key="raw_news"
)

news_summarizer = Agent(
    name="news_summarizer",
    model="gemini-2.0-flash",
    description="Summarizes key news points",
    instruction=(
        "Summarize the news articles into 2-3 key takeaways.\n"
        "\n"
        "**Raw News:**\n"
        "{raw_news}\n"
        "\n"
        "Output format:\n"
        "KEY TAKEAWAYS:\n"
        "1. First key point\n"
        "2. Second key point\n"
        "3. Third key point"
    ),
    output_key="news_summary"
)

# Sequential pipeline for news research
news_pipeline = SequentialAgent(
    name="NewsPipeline",
    sub_agents=[news_fetcher, news_summarizer],
    description="Fetches and summarizes news"
)

# ============================================================================
# PARALLEL BRANCH 2: Social Media Research Pipeline
# ============================================================================

social_monitor = Agent(
    name="social_monitor",
    model="gemini-2.0-flash",
    description="Monitors social media trends using Google Search",
    instruction=(
        "You are a social media analyst. Based on the user's topic, search for "
        "trending discussions, popular hashtags, and public sentiment.\n"
        "\n"
        "Use the google_search tool to find:\n"
        "• Trending hashtags and topics on social platforms\n"
        "• Recent social media discussions and viral content\n"
        "• Public opinion and sentiment analysis\n"
        "\n"
        "Search for: '[topic] social media trends reddit twitter discussion'\n"
        "\n"
        "Output:\n"
        "• 3-4 trending hashtags or topics\n"
        "• Popular discussion themes\n"
        "• General sentiment (positive/negative/mixed) with evidence"
    ),
    tools=[google_search],
    output_key="raw_social"
)

sentiment_analyzer = Agent(
    name="sentiment_analyzer",
    model="gemini-2.0-flash",
    description="Analyzes social sentiment",
    instruction=(
        "Analyze the social media data and extract key insights.\n"
        "\n"
        "**Social Media Data:**\n"
        "{raw_social}\n"
        "\n"
        "Output format:\n"
        "SOCIAL INSIGHTS:\n"
        "• Trending: [hashtags/topics]\n"
        "• Sentiment: [overall mood]\n"
        "• Key Themes: [main discussion points]"
    ),
    output_key="social_insights"
)

# Sequential pipeline for social research
social_pipeline = SequentialAgent(
    name="SocialPipeline",
    sub_agents=[social_monitor, sentiment_analyzer],
    description="Monitors and analyzes social media"
)

# ============================================================================
# PARALLEL BRANCH 3: Expert Opinion Pipeline
# ============================================================================

expert_finder = Agent(
    name="expert_finder",
    model="gemini-2.0-flash",
    description="Finds expert opinions using Google Search",
    instruction=(
        "You are an expert opinion researcher. Based on the user's topic, search for "
        "what industry experts, academics, or thought leaders are saying.\n"
        "\n"
        "Use the google_search tool to find:\n"
        "• Industry experts and their credentials\n"
        "• Academic researchers and their affiliations\n"
        "• Thought leaders and their recent statements\n"
        "\n"
        "Search for: '[topic] expert opinion academic research thought leader'\n"
        "\n"
        "Output:\n"
        "• 2-3 expert names and their credentials\n"
        "• Their key statements or positions\n"
        "• Source (where they said it) with links when available"
    ),
    tools=[google_search],
    output_key="raw_experts"
)

quote_extractor = Agent(
    name="quote_extractor",
    model="gemini-2.0-flash",
    description="Extracts quotable insights",
    instruction=(
        "Extract the most impactful quotes and insights from expert opinions.\n"
        "\n"
        "**Expert Opinions:**\n"
        "{raw_experts}\n"
        "\n"
        "Output format:\n"
        "EXPERT INSIGHTS:\n"
        "• Quote 1: \"...\" - [Expert Name], [Credentials]\n"
        "• Quote 2: \"...\" - [Expert Name], [Credentials]"
    ),
    output_key="expert_quotes"
)

# Sequential pipeline for expert research
expert_pipeline = SequentialAgent(
    name="ExpertPipeline",
    sub_agents=[expert_finder, quote_extractor],
    description="Finds and extracts expert opinions"
)

# ============================================================================
# PHASE 1: PARALLEL RESEARCH (3 pipelines run together!)
# ============================================================================

parallel_research = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[
        news_pipeline,    # Sequential: fetch → summarize
        social_pipeline,  # Sequential: monitor → analyze
        expert_pipeline   # Sequential: find → extract
    ],
    description="Runs all research pipelines concurrently"
)

# ============================================================================
# PHASE 2: CONTENT CREATION (Sequential synthesis)
# ============================================================================

article_writer = Agent(
    name="article_writer",
    model="gemini-2.0-flash",
    description="Writes article draft from all research",
    instruction=(
        "You are a professional writer. Write an engaging article using ALL "
        "the research below.\n"
        "\n"
        "**News Summary:**\n"
        "{news_summary}\n"
        "\n"
        "**Social Insights:**\n"
        "{social_insights}\n"
        "\n"
        "**Expert Quotes:**\n"
        "{expert_quotes}\n"
        "\n"
        "Write a 4-5 paragraph article that:\n"
        "- Opens with a compelling hook\n"
        "- Incorporates news, social trends, and expert opinions naturally\n"
        "- Uses expert quotes effectively\n"
        "- Has a strong conclusion\n"
        "\n"
        "Output ONLY the article text."
    ),
    output_key="draft_article"
)

article_editor = Agent(
    name="article_editor",
    model="gemini-2.0-flash",
    description="Edits article for clarity and impact",
    instruction=(
        "You are an editor. Review and improve the article below.\n"
        "\n"
        "**Draft Article:**\n"
        "{draft_article}\n"
        "\n"
        "Edit for:\n"
        "- Clarity and flow\n"
        "- Impact and engagement\n"
        "- Grammar and style\n"
        "\n"
        "Output the improved article."
    ),
    output_key="edited_article"
)

article_formatter = Agent(
    name="article_formatter",
    model="gemini-2.0-flash",
    description="Formats article for publication",
    instruction=(
        "Format the article for publication with proper markdown.\n"
        "\n"
        "**Article:**\n"
        "{edited_article}\n"
        "\n"
        "Add:\n"
        "- Compelling title (# heading)\n"
        "- Byline (By: AI Content Team)\n"
        "- Section headings where appropriate (## subheadings)\n"
        "- Proper formatting (bold, italic, quotes)\n"
        "- Publication date placeholder\n"
        "\n"
        "Output the final formatted article."
    ),
    output_key="published_article"
)

# ============================================================================
# COMPLETE MULTI-AGENT SYSTEM
# ============================================================================

content_publishing_system = SequentialAgent(
    name="ContentPublishingSystem",
    sub_agents=[
        parallel_research,  # Phase 1: Research (3 parallel pipelines!)
        article_writer,     # Phase 2: Draft
        article_editor,     # Phase 3: Edit
        article_formatter   # Phase 4: Format
    ],
    description="Complete content publishing system with parallel research and sequential creation"
)

# MUST be named root_agent for ADK discovery
root_agent = content_publishing_system