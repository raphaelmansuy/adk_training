"""
Tests for Tutorial 06: Multi-Agent Systems - Content Publishing System
"""

from __future__ import annotations

import pytest
from content_publisher.agent import (
    # Individual agents
    news_fetcher, news_summarizer, social_monitor, sentiment_analyzer,
    expert_finder, quote_extractor, article_writer, article_editor, article_formatter,
    # Sequential pipelines
    news_pipeline, social_pipeline, expert_pipeline,
    # Parallel research
    parallel_research,
    # Complete system
    content_publishing_system, root_agent
)


class TestIndividualAgents:
    """Test individual agent configurations"""

    def test_news_agents_config(self):
        """Test news pipeline agent configurations"""
        assert news_fetcher.name == "news_fetcher"
        assert news_fetcher.model == "gemini-2.0-flash"
        assert news_fetcher.description == "Fetches current news articles using Google Search"
        assert "news" in news_fetcher.instruction.lower()
        assert "google_search" in news_fetcher.instruction.lower()
        assert news_fetcher.output_key == "raw_news"

        assert news_summarizer.name == "news_summarizer"
        assert news_summarizer.model == "gemini-2.0-flash"
        assert news_summarizer.description == "Summarizes key news points"
        assert "summarize" in news_summarizer.instruction.lower()
        assert news_summarizer.output_key == "news_summary"

    def test_social_agents_config(self):
        """Test social pipeline agent configurations"""
        assert social_monitor.name == "social_monitor"
        assert social_monitor.model == "gemini-2.0-flash"
        assert social_monitor.description == "Monitors social media trends using Google Search"
        assert "social" in social_monitor.instruction.lower()
        assert "google_search" in social_monitor.instruction.lower()
        assert social_monitor.output_key == "raw_social"

        assert sentiment_analyzer.name == "sentiment_analyzer"
        assert sentiment_analyzer.model == "gemini-2.0-flash"
        assert sentiment_analyzer.description == "Analyzes social sentiment"
        assert "sentiment" in sentiment_analyzer.instruction.lower()
        assert sentiment_analyzer.output_key == "social_insights"

    def test_expert_agents_config(self):
        """Test expert pipeline agent configurations"""
        assert expert_finder.name == "expert_finder"
        assert expert_finder.model == "gemini-2.0-flash"
        assert expert_finder.description == "Finds expert opinions using Google Search"
        assert "expert" in expert_finder.instruction.lower()
        assert "google_search" in expert_finder.instruction.lower()
        assert expert_finder.output_key == "raw_experts"

        assert quote_extractor.name == "quote_extractor"
        assert quote_extractor.model == "gemini-2.0-flash"
        assert quote_extractor.description == "Extracts quotable insights"
        assert "quote" in quote_extractor.instruction.lower()
        assert quote_extractor.output_key == "expert_quotes"

    def test_content_creation_agents_config(self):
        """Test content creation agent configurations"""
        assert article_writer.name == "article_writer"
        assert article_writer.model == "gemini-2.0-flash"
        assert article_writer.description == "Writes article draft from all research"
        assert "write" in article_writer.instruction.lower()
        assert article_writer.output_key == "draft_article"

        assert article_editor.name == "article_editor"
        assert article_editor.model == "gemini-2.0-flash"
        assert article_editor.description == "Edits article for clarity and impact"
        assert "edit" in article_editor.instruction.lower()
        assert article_editor.output_key == "edited_article"

        assert article_formatter.name == "article_formatter"
        assert article_formatter.model == "gemini-2.0-flash"
        assert article_formatter.description == "Formats article for publication"
        assert "format" in article_formatter.instruction.lower()
        assert article_formatter.output_key == "published_article"

    def test_agents_have_unique_output_keys(self):
        """Test that all agents have unique output keys"""
        output_keys = [
            news_fetcher.output_key, news_summarizer.output_key,
            social_monitor.output_key, sentiment_analyzer.output_key,
            expert_finder.output_key, quote_extractor.output_key,
            article_writer.output_key, article_editor.output_key, article_formatter.output_key
        ]
        assert len(set(output_keys)) == len(output_keys)


class TestSequentialPipelines:
    """Test sequential pipeline configurations"""

    def test_news_pipeline_structure(self):
        """Test news pipeline is sequential with correct sub-agents"""
        assert news_pipeline.name == "NewsPipeline"
        assert news_pipeline.description == "Fetches and summarizes news"
        assert len(news_pipeline.sub_agents) == 2
        assert news_pipeline.sub_agents[0] == news_fetcher
        assert news_pipeline.sub_agents[1] == news_summarizer

    def test_social_pipeline_structure(self):
        """Test social pipeline is sequential with correct sub-agents"""
        assert social_pipeline.name == "SocialPipeline"
        assert social_pipeline.description == "Monitors and analyzes social media"
        assert len(social_pipeline.sub_agents) == 2
        assert social_pipeline.sub_agents[0] == social_monitor
        assert social_pipeline.sub_agents[1] == sentiment_analyzer

    def test_expert_pipeline_structure(self):
        """Test expert pipeline is sequential with correct sub-agents"""
        assert expert_pipeline.name == "ExpertPipeline"
        assert expert_pipeline.description == "Finds and extracts expert opinions"
        assert len(expert_pipeline.sub_agents) == 2
        assert expert_pipeline.sub_agents[0] == expert_finder
        assert expert_pipeline.sub_agents[1] == quote_extractor


class TestParallelResearch:
    """Test parallel research configuration"""

    def test_parallel_research_is_parallel_agent(self):
        """Test parallel_research is a ParallelAgent"""
        from google.adk.agents import ParallelAgent
        assert isinstance(parallel_research, ParallelAgent)

    def test_parallel_research_name_and_description(self):
        """Test parallel research name and description"""
        assert parallel_research.name == "ParallelResearch"
        assert parallel_research.description == "Runs all research pipelines concurrently"

    def test_parallel_research_has_three_pipelines(self):
        """Test parallel research has all three sequential pipelines"""
        assert len(parallel_research.sub_agents) == 3
        assert news_pipeline in parallel_research.sub_agents
        assert social_pipeline in parallel_research.sub_agents
        assert expert_pipeline in parallel_research.sub_agents


class TestContentPublishingSystem:
    """Test complete content publishing system"""

    def test_system_is_sequential_agent(self):
        """Test content publishing system is a SequentialAgent"""
        from google.adk.agents import SequentialAgent
        assert isinstance(content_publishing_system, SequentialAgent)

    def test_system_name_and_description(self):
        """Test system name and description"""
        assert content_publishing_system.name == "ContentPublishingSystem"
        assert content_publishing_system.description == "Complete content publishing system with parallel research and sequential creation"

    def test_system_has_correct_phases(self):
        """Test system has parallel research phase + 3 sequential creation phases"""
        assert len(content_publishing_system.sub_agents) == 4
        assert content_publishing_system.sub_agents[0] == parallel_research
        assert content_publishing_system.sub_agents[1] == article_writer
        assert content_publishing_system.sub_agents[2] == article_editor
        assert content_publishing_system.sub_agents[3] == article_formatter


class TestRootAgent:
    """Test root agent configuration"""

    def test_root_agent_is_content_publishing_system(self):
        """Test root_agent is the content publishing system"""
        assert root_agent == content_publishing_system

    def test_root_agent_is_sequential_agent(self):
        """Test root agent is a SequentialAgent"""
        from google.adk.agents import SequentialAgent
        assert isinstance(root_agent, SequentialAgent)


class TestStateManagement:
    """Test state management and data flow"""

    def test_parallel_agents_have_output_keys_for_state_injection(self):
        """Test that parallel pipeline agents save to state for sequential access"""
        # News pipeline outputs
        assert news_summarizer.output_key == "news_summary"
        # Social pipeline outputs
        assert sentiment_analyzer.output_key == "social_insights"
        # Expert pipeline outputs
        assert quote_extractor.output_key == "expert_quotes"

    def test_writer_reads_all_research_outputs(self):
        """Test writer instruction includes all research output keys"""
        instruction = article_writer.instruction
        assert "{news_summary}" in instruction
        assert "{social_insights}" in instruction
        assert "{expert_quotes}" in instruction

    def test_editor_reads_writer_output(self):
        """Test editor reads from writer's output key"""
        instruction = article_editor.instruction
        assert "{draft_article}" in instruction

    def test_formatter_reads_editor_output(self):
        """Test formatter reads from editor's output key"""
        instruction = article_formatter.instruction
        assert "{edited_article}" in instruction

    def test_no_circular_dependencies(self):
        """Test no agent reads from keys it or its successors produce"""
        # Writer should not read from draft_article (its own output)
        assert "{draft_article}" not in article_writer.instruction
        # Editor should not read from edited_article (its own output)
        assert "{edited_article}" not in article_editor.instruction
        # Formatter should not read from published_article (its own output)
        assert "{published_article}" not in article_formatter.instruction


class TestAgentInstructions:
    """Test agent instruction quality and completeness"""

    def test_news_fetcher_instruction_format(self):
        """Test news fetcher has clear, specific instructions"""
        instruction = news_fetcher.instruction
        assert "news researcher" in instruction.lower()
        assert "google_search" in instruction.lower()
        assert "3-4" in instruction
        assert "bulleted list" in instruction
        assert "recent" in instruction

    def test_news_summarizer_instruction_format(self):
        """Test news summarizer reads from fetcher and has clear format"""
        instruction = news_summarizer.instruction
        assert "{raw_news}" in instruction
        assert "key takeaways" in instruction.lower()
        assert "1." in instruction
        assert "2." in instruction
        assert "3." in instruction

    def test_social_monitor_instruction_format(self):
        """Test social monitor has clear social media focus"""
        instruction = social_monitor.instruction
        assert "social media analyst" in instruction.lower()
        assert "google_search" in instruction.lower()
        assert "trending" in instruction.lower()
        assert "hashtags" in instruction.lower()
        assert "sentiment" in instruction.lower()

    def test_sentiment_analyzer_instruction_format(self):
        """Test sentiment analyzer reads from monitor and has clear format"""
        instruction = sentiment_analyzer.instruction
        assert "{raw_social}" in instruction
        assert "social insights" in instruction.lower()
        assert "trending:" in instruction.lower()
        assert "sentiment:" in instruction.lower()

    def test_expert_finder_instruction_format(self):
        """Test expert finder focuses on credible sources"""
        instruction = expert_finder.instruction
        assert "expert opinion researcher" in instruction.lower()
        assert "google_search" in instruction.lower()
        assert "industry experts" in instruction.lower()
        assert "academics" in instruction.lower()
        assert "thought leaders" in instruction.lower()

    def test_quote_extractor_instruction_format(self):
        """Test quote extractor reads from finder and formats quotes"""
        instruction = quote_extractor.instruction
        assert "{raw_experts}" in instruction
        assert "expert insights" in instruction.lower()
        assert "quote" in instruction.lower()

    def test_writer_instruction_comprehensive(self):
        """Test writer instruction requires all research inputs"""
        instruction = article_writer.instruction
        assert "professional writer" in instruction.lower()
        assert "engaging article" in instruction.lower()
        assert "compelling hook" in instruction.lower()
        assert "expert quotes" in instruction.lower()
        assert "strong conclusion" in instruction.lower()

    def test_editor_instruction_focus(self):
        """Test editor focuses on improvement areas"""
        instruction = article_editor.instruction
        assert "editor" in instruction.lower()
        assert "clarity" in instruction.lower()
        assert "flow" in instruction.lower()
        assert "impact" in instruction.lower()

    def test_formatter_instruction_structure(self):
        """Test formatter adds publication elements"""
        instruction = article_formatter.instruction
        assert "format" in instruction.lower()
        assert "publication" in instruction.lower()
        assert "title" in instruction.lower()
        assert "byline" in instruction.lower()
        assert "markdown" in instruction.lower()

    def test_instructions_focus_on_output(self):
        """Test instructions emphasize clear, structured output"""
        instructions = [
            news_fetcher.instruction, news_summarizer.instruction,
            social_monitor.instruction, sentiment_analyzer.instruction,
            expert_finder.instruction, quote_extractor.instruction,
            article_writer.instruction, article_editor.instruction, article_formatter.instruction
        ]

        for instruction in instructions:
            # Each instruction should mention output format or structure
            output_indicators = ["output", "format", "bulleted", "list", "summary", "insights"]
            assert any(indicator in instruction.lower() for indicator in output_indicators), \
                f"Instruction lacks output guidance: {instruction[:100]}..."


class TestImports:
    """Test import and module structure"""

    def test_google_adk_agents_import(self):
        """Test google.adk.agents imports successfully"""
        try:
            from google.adk.agents import Agent, ParallelAgent, SequentialAgent
        except ImportError as e:
            pytest.fail(f"Failed to import google.adk.agents: {e}")

    def test_content_publisher_agent_import(self):
        """Test content_publisher.agent imports successfully"""
        try:
            import content_publisher.agent
        except ImportError as e:
            pytest.fail(f"Failed to import content_publisher.agent: {e}")

    def test_root_agent_exists(self):
        """Test root_agent is defined and accessible"""
        try:
            from content_publisher.agent import root_agent
            assert root_agent is not None
        except (ImportError, AttributeError) as e:
            pytest.fail(f"root_agent not accessible: {e}")

    def test_future_annotations_import(self):
        """Test __future__ annotations import works"""
        try:
            exec("from __future__ import annotations")
        except ImportError as e:
            pytest.fail(f"Failed to import __future__.annotations: {e}")


class TestProjectStructure:
    """Test project file and directory structure"""

    def test_content_publisher_directory_exists(self):
        """Test content_publisher directory exists"""
        import os
        assert os.path.isdir("content_publisher")

    def test_init_py_exists(self):
        """Test __init__.py exists"""
        import os
        assert os.path.isfile("content_publisher/__init__.py")

    def test_agent_py_exists(self):
        """Test agent.py exists"""
        import os
        assert os.path.isfile("content_publisher/agent.py")

    def test_env_example_exists(self):
        """Test .env.example exists"""
        import os
        assert os.path.isfile("content_publisher/.env.example")

    def test_init_py_content(self):
        """Test __init__.py has correct import"""
        with open("content_publisher/__init__.py", "r") as f:
            content = f.read().strip()
            assert "from . import agent" in content

    def test_agent_py_is_python_file(self):
        """Test agent.py is a valid Python file"""
        with open("content_publisher/agent.py", "r") as f:
            content = f.read()
            assert "from __future__ import annotations" in content
            assert "root_agent = content_publishing_system" in content

    def test_env_example_content(self):
        """Test .env.example has required variables"""
        with open("content_publisher/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_GENAI_USE_VERTEXAI=FALSE" in content
            assert "GOOGLE_API_KEY=" in content


class TestTestStructure:
    """Test test directory and file structure"""

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        import os
        assert os.path.isdir("tests")

    def test_tests_init_py_exists(self):
        """Test tests/__init__.py exists"""
        import os
        assert os.path.isfile("tests/__init__.py")

    def test_test_files_exist(self):
        """Test test files exist"""
        import os
        assert os.path.isfile("tests/test_agent.py")
        assert os.path.isfile("tests/test_imports.py")
        assert os.path.isfile("tests/test_structure.py")


class TestAgentIntegration:
    """Test agent integration and system coherence"""

    def test_pipeline_can_be_created_without_error(self):
        """Test complete pipeline can be instantiated without errors"""
        try:
            from content_publisher.agent import root_agent
            assert root_agent is not None
            assert root_agent.name == "ContentPublishingSystem"
        except Exception as e:
            pytest.fail(f"Failed to create pipeline: {e}")

    def test_pipeline_has_valid_configuration_for_api(self):
        """Test pipeline has valid configuration for ADK API"""
        from content_publisher.agent import root_agent

        # Should have name and description
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'description')
        assert root_agent.name
        assert root_agent.description

        # Should have sub_agents
        assert hasattr(root_agent, 'sub_agents')
        assert len(root_agent.sub_agents) > 0

    def test_state_flow_is_configured(self):
        """Test state flow between agents is properly configured"""
        from content_publisher.agent import (
            parallel_research, article_writer, article_editor, article_formatter
        )

        # Parallel research should have agents with output keys
        for pipeline in parallel_research.sub_agents:
            for agent in pipeline.sub_agents:
                assert hasattr(agent, 'output_key')
                assert agent.output_key

        # Sequential agents should read from previous outputs
        assert "{news_summary}" in article_writer.instruction
        assert "{social_insights}" in article_writer.instruction
        assert "{expert_quotes}" in article_writer.instruction
        assert "{draft_article}" in article_editor.instruction
        assert "{edited_article}" in article_formatter.instruction