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
        'contact',
      ],
    },
    {
      type: 'category',
      label: 'Foundation Tutorials',
      collapsed: false,
      items: [
        'setup_authentication',
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
        'gepa_optimization_advanced',
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
    {
      type: 'category',
      label: 'End-to-End Implementations',
      collapsed: true,
      description: 'Complete, production-ready applications demonstrating ADK patterns',
      items: [
        'commerce_agent_e2e',
        'file_search_policy_navigator',
      ],
    },
    {
      type: 'category',
      label: 'Today I Learn (TIL)',
      collapsed: true,
      description: 'Quick daily learning pieces on specific ADK features',
      items: [
        {
          type: 'doc',
          id: 'til/til_index',
          label: '🎯 TIL Index',
        },
        {
          type: 'doc',
          id: 'til/til_custom_session_services_20251023',
          label: 'TIL: Custom Session Services (Oct 23)',
        },
        {
          type: 'doc',
          id: 'til/til_rubric_based_tool_use_quality_20251021',
          label: 'TIL: Tool Use Quality (Oct 21)',
        },
        {
          type: 'doc',
          id: 'til/til_pause_resume_20251020',
          label: 'TIL: Pause & Resume (Oct 20)',
        },
        {
          type: 'doc',
          id: 'til/til_context_compaction_20250119',
          label: 'TIL: Context Compaction (Oct 19)',
        },
        {
          type: 'doc',
          id: 'til/til_template',
          label: '📋 TIL Guidelines & Template',
        },
      ],
    },
    {
      type: 'category',
      label: 'SEO Audit & Implementation',
      collapsed: true,
      description: 'Comprehensive SEO audit with 6-month implementation roadmap',
      items: [
        {
          type: 'doc',
          id: 'seo_audit/seo_audit_index',
          label: '🎯 SEO Audit Index',
        },
        {
          type: 'doc',
          id: 'seo_audit/seo_executive_summary',
          label: 'Executive Summary',
        },
        {
          type: 'doc',
          id: 'seo_audit/seo_detailed_findings',
          label: 'Detailed Findings',
        },
        {
          type: 'doc',
          id: 'seo_audit/seo_implementation_guide',
          label: 'Implementation Guide',
        },
        {
          type: 'doc',
          id: 'seo_audit/seo_phase_based_roadmap',
          label: 'Phase-Based Roadmap',
        },
        {
          type: 'doc',
          id: 'seo_audit/seo_monitoring_dashboard',
          label: 'Monitoring Dashboard',
        },
        {
          type: 'doc',
          id: 'seo_audit/seo_progress_tracking',
          label: 'Progress Tracking',
        },
      ],
    },
  ],
};

export default sidebars;
