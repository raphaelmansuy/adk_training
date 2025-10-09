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
      type: 'doc',
      id: 'mermaid-test',
      label: 'Mermaid Test',
    },
    {
      type: 'category',
      label: 'Foundation Tutorials',
      collapsed: false,
      items: [
        'tutorial/01_hello_world_agent',
        'tutorial/02_function_tools',
        'tutorial/03_openapi_tools',
      ],
    },
  ],
};

export default sidebars;
