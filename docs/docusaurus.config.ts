import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'ADK Training Hub',
  tagline: 'Master Google Agent Development Kit from First Principles',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://raphaelmansuy.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/adk_training/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'raphaelmansuy', // Usually your GitHub org/user name.
  projectName: 'adk_training', // Usually your repo name.

  onBrokenLinks: 'ignore',

  markdown: {
    mermaid: true,
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: '../tutorial', // Point to the root tutorial directory
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/raphaelmansuy/adk_training/edit/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/raphaelmansuy/adk_training/edit/main/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    '@docusaurus/theme-mermaid',
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'ADK Training Hub',
      logo: {
        alt: 'ADK Training Hub Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Tutorials',
        },
        {
          to: '/docs/overview',
          label: 'Mental Models',
          position: 'left',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/raphaelmansuy/adk_training',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {
              label: 'Tutorials',
              to: '/docs/tutorial/01_hello_world_agent',
            },
            {
              label: 'Mental Models',
              to: '/docs/overview',
            },
            {
              label: 'Code Examples',
              to: '/docs/tutorial/01_hello_world_agent',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/raphaelmansuy/adk_training',
            },
            {
              label: 'Issues',
              href: 'https://github.com/raphaelmansuy/adk_training/issues',
            },
            {
              label: 'Discussions',
              href: 'https://github.com/raphaelmansuy/adk_training/discussions',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Google ADK Docs',
              href: 'https://google.github.io/adk-docs/',
            },
            {
              label: 'Google AI Studio',
              href: 'https://makersuite.google.com/app/apikey',
            },
            {
              label: 'ADK Python',
              href: 'https://github.com/google/adk-python',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} ADK Training Project. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    mermaid: {
      theme: { light: 'default', dark: 'dark' },
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
