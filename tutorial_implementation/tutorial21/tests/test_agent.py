"""
Test agent configuration for vision_catalog_agent
"""

from vision_catalog_agent import root_agent
from vision_catalog_agent.agent import (
    vision_analyzer,
    catalog_generator,
    analyze_product_image,
    analyze_uploaded_image,
    compare_product_images,
    generate_catalog_entry,
    generate_product_mockup,
    list_sample_images
)


class TestAgentConfiguration:
    """Test agent configuration and structure."""
    
    def test_root_agent_exists(self):
        """Test root_agent is defined."""
        assert root_agent is not None
    
    def test_root_agent_name(self):
        """Test root_agent has correct name."""
        assert root_agent.name == 'vision_catalog_coordinator'
    
    def test_root_agent_model(self):
        """Test root_agent uses correct model."""
        assert root_agent.model in [
            'gemini-2.0-flash-exp',
            'gemini-2.0-flash',
            'gemini-1.5-pro',
            'gemini-1.5-flash'
        ]
    
    def test_root_agent_has_tools(self):
        """Test root_agent has tools configured."""
        assert root_agent.tools is not None
        assert len(root_agent.tools) >= 5  # list_sample_images, generate_product_mockup, analyze_uploaded_image, analyze_product_image, compare_product_images
    
    def test_root_agent_has_instruction(self):
        """Test root_agent has instruction."""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0
    
    def test_root_agent_has_description(self):
        """Test root_agent has description."""
        assert root_agent.description is not None
        assert len(root_agent.description) > 0


class TestVisionAnalyzerAgent:
    """Test vision analyzer agent configuration."""
    
    def test_vision_analyzer_exists(self):
        """Test vision_analyzer is defined."""
        assert vision_analyzer is not None
    
    def test_vision_analyzer_name(self):
        """Test vision_analyzer has correct name."""
        assert vision_analyzer.name == 'vision_analyzer'
    
    def test_vision_analyzer_model(self):
        """Test vision_analyzer uses vision-capable model."""
        assert 'gemini' in vision_analyzer.model.lower()
    
    def test_vision_analyzer_instruction(self):
        """Test vision_analyzer has vision-specific instruction."""
        instruction = vision_analyzer.instruction.lower()
        assert any(keyword in instruction for keyword in [
            'vision', 'image', 'visual', 'analyze'
        ])
    
    def test_vision_analyzer_temperature(self):
        """Test vision_analyzer has appropriate temperature."""
        if vision_analyzer.generate_content_config:
            assert vision_analyzer.generate_content_config.temperature <= 0.5


class TestCatalogGeneratorAgent:
    """Test catalog generator agent configuration."""
    
    def test_catalog_generator_exists(self):
        """Test catalog_generator is defined."""
        assert catalog_generator is not None
    
    def test_catalog_generator_name(self):
        """Test catalog_generator has correct name."""
        assert catalog_generator.name == 'catalog_generator'
    
    def test_catalog_generator_has_tools(self):
        """Test catalog_generator has tools."""
        assert catalog_generator.tools is not None
        assert len(catalog_generator.tools) > 0
    
    def test_catalog_generator_instruction(self):
        """Test catalog_generator has catalog-specific instruction."""
        instruction = catalog_generator.instruction.lower()
        assert any(keyword in instruction for keyword in [
            'catalog', 'description', 'product'
        ])


class TestTools:
    """Test tool functions."""
    
    def test_analyze_product_image_callable(self):
        """Test analyze_product_image is callable."""
        assert callable(analyze_product_image)
    
    def test_analyze_uploaded_image_callable(self):
        """Test analyze_uploaded_image is callable."""
        assert callable(analyze_uploaded_image)
    
    def test_compare_product_images_callable(self):
        """Test compare_product_images is callable."""
        assert callable(compare_product_images)
    
    def test_generate_product_mockup_callable(self):
        """Test generate_product_mockup is callable."""
        assert callable(generate_product_mockup)
    
    def test_list_sample_images_callable(self):
        """Test list_sample_images is callable."""
        assert callable(list_sample_images)
    
    def test_generate_catalog_entry_callable(self):
        """Test generate_catalog_entry is callable."""
        assert callable(generate_catalog_entry)
    
    def test_tool_signatures(self):
        """Test tool function signatures."""
        import inspect
        
        # analyze_product_image should have product_id, image_path, tool_context
        sig = inspect.signature(analyze_product_image)
        assert 'product_id' in sig.parameters
        assert 'image_path' in sig.parameters
        assert 'tool_context' in sig.parameters
        
        # analyze_uploaded_image should have product_name, tool_context
        sig = inspect.signature(analyze_uploaded_image)
        assert 'product_name' in sig.parameters
        assert 'tool_context' in sig.parameters
        
        # compare_product_images should have image_paths, tool_context
        sig = inspect.signature(compare_product_images)
        assert 'image_paths' in sig.parameters
        assert 'tool_context' in sig.parameters
        
        # generate_catalog_entry should have product_name, analysis, tool_context
        sig = inspect.signature(generate_catalog_entry)
        assert 'product_name' in sig.parameters
        assert 'analysis' in sig.parameters
        assert 'tool_context' in sig.parameters
        
        # generate_product_mockup should have product_description, product_name, tool_context
        sig = inspect.signature(generate_product_mockup)
        assert 'product_description' in sig.parameters
        assert 'product_name' in sig.parameters
        assert 'tool_context' in sig.parameters


class TestAgentToolIntegration:
    """Test agent-tool integration."""
    
    def test_root_agent_tool_names(self):
        """Test root_agent has expected tool names."""
        tool_names = []
        for tool in root_agent.tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            elif hasattr(tool, '_function') and hasattr(tool._function, '__name__'):
                tool_names.append(tool._function.__name__)
        
        expected_tools = {'list_sample_images', 'generate_product_mockup', 'analyze_uploaded_image', 'analyze_product_image', 'compare_product_images'}
        actual_tools = set(tool_names)
        
        assert expected_tools.issubset(actual_tools), \
            f"Missing tools: {expected_tools - actual_tools}"
    
    def test_catalog_generator_has_artifact_tool(self):
        """Test catalog_generator has artifact generation tool."""
        tool_names = []
        for tool in catalog_generator.tools:
            if hasattr(tool, 'name'):
                tool_names.append(tool.name)
            elif hasattr(tool, '_function') and hasattr(tool._function, '__name__'):
                tool_names.append(tool._function.__name__)
        
        assert 'generate_catalog_entry' in tool_names


class TestConfiguration:
    """Test agent configuration settings."""
    
    def test_generate_content_configs(self):
        """Test agents have appropriate generation configs."""
        agents = [root_agent, vision_analyzer, catalog_generator]
        
        for agent in agents:
            if agent.generate_content_config:
                config = agent.generate_content_config
                
                # Temperature should be reasonable
                if hasattr(config, 'temperature'):
                    assert 0.0 <= config.temperature <= 1.0
                
                # Max tokens should be set
                if hasattr(config, 'max_output_tokens'):
                    assert config.max_output_tokens > 0
