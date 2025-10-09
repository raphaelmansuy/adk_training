import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'overview',
      label: 'Mental Models Overview',
    },
    {
      type: 'category',
      label: 'Mental Models',
      collapsed: false,
      items: [
        'overview',
        'agent-architecture',
        'tools-capabilities',
        'workflows-orchestration',
        'llm-integration',
        'production-deployment',
        'advanced-patterns',
        'decision-frameworks',
        'learning-paths',
        'reference-guide',
      ],
    },
    {
      type: 'category',
      label: 'Foundation Tutorials',
      collapsed: false,
      items: [
        'hello_world_agent',
        'function_tools',
        'openapi_tools',
        'sequential_workflows',
        'parallel_processing',
      ],
    },
    {
      type: 'category',
      label: 'Advanced Tutorials',
      collapsed: true,
      items: [
        'multi_agent_systems',
        'loop_agents',
        'state_memory',
        'callbacks_guardrails',
        'evaluation_testing',
        'built_in_tools_grounding',
        'planners_thinking',
        'code_execution',
        'streaming_sse',
        'live_api_audio',
        'mcp_integration',
        'agent_to_agent',
        'events_observability',
        'artifacts_files',
        'yaml_configuration',
        'multimodal_image',
        'model_selection',
        'production_deployment',
        'advanced_observability',
        'best_practices',
        'google_agentspace',
        'third_party_tools',
        'using_other_llms',
      ],
    },
    {
      type: 'category',
      label: 'UI Integration Tutorials',
      collapsed: true,
      items: [
        'ui_integration_intro',
        'nextjs_adk_integration',
        'react_vite_adk_integration',
        'streamlit_adk_integration',
        'slack_adk_integration',
        'pubsub_adk_integration',
      ],
    },
  ],
};

export default sidebars;
