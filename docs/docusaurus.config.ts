import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import * as path from 'path';

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

  // Structured data for rich snippets
  headTags: [
    // Organization schema
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Organization',
        name: 'ADK Training Hub',
        url: 'https://raphaelmansuy.github.io/adk_training/',
        logo: 'https://raphaelmansuy.github.io/adk_training/img/ADK-512-color.svg',
        description: 'Comprehensive training for Google Agent Development Kit with 34 tutorials, mental models, and production-ready examples.',
        founder: {
          '@type': 'Person',
          name: 'Raphael Mansuy',
        },
        sameAs: [
          'https://github.com/raphaelmansuy',
          'https://github.com/raphaelmansuy/adk_training',
        ],
      }),
    },

    // Website schema
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        name: 'ADK Training Hub',
        url: 'https://raphaelmansuy.github.io/adk_training/',
        description: 'Master Google Agent Development Kit from first principles to production deployment.',
        potentialAction: {
          '@type': 'SearchAction',
          target: 'https://raphaelmansuy.github.io/adk_training/search?q={search_term_string}',
          'query-input': 'required name=search_term_string',
        },
      }),
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          path: path.resolve(__dirname, './tutorial'), // Absolute path to tutorial directory
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/raphaelmansuy/adk_training/edit/main/docs/tutorial/',
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
        sitemap: {
          lastmod: 'datetime',
          changefreq: null, // Let individual pages control this
          priority: null, // Use dynamic priority based on page type
          ignorePatterns: ['/tags/**', '/search/**'],
          createSitemapItems: async (params) => {
            const { defaultCreateSitemapItems, ...rest } = params;
            const items = await defaultCreateSitemapItems(rest);

            return items.map((item) => {
              // Set different priorities based on page type
              if (item.url.includes('/docs/overview')) {
                return { ...item, priority: 1.0, changefreq: 'monthly' };
              }
              if (item.url.includes('/docs/')) {
                return { ...item, priority: 0.8, changefreq: 'weekly' };
              }
              if (item.url.includes('/blog')) {
                return { ...item, priority: 0.6, changefreq: 'weekly' };
              }
              if (item.url === 'https://raphaelmansuy.github.io/adk_training/') {
                return { ...item, priority: 1.0, changefreq: 'daily' };
              }
              return { ...item, priority: 0.5, changefreq: 'monthly' };
            });
          },
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    '@docusaurus/theme-mermaid',
  ],

  plugins: [
    [
      '@docusaurus/plugin-google-gtag',
      {
        trackingID: 'GA_MEASUREMENT_ID', // Replace with your actual GA4 measurement ID
        anonymizeIP: true,
      },
    ],
  ],

  themeConfig: {
    // Enhanced metadata for better SEO
    metadata: [
      // Basic SEO meta tags
      { name: 'keywords', content: 'Google ADK, Agent Development Kit, AI agents, machine learning, Google Gemini, tutorial, programming, Python, JavaScript' },
      { name: 'author', content: 'Raphael Mansuy' },
      { name: 'robots', content: 'index, follow' },
      { name: 'language', content: 'English' },
      { name: 'revisit-after', content: '7 days' },

      // Open Graph meta tags
      { property: 'og:type', content: 'website' },
      { property: 'og:site_name', content: 'ADK Training Hub' },
      { property: 'og:locale', content: 'en_US' },

      // Twitter Card meta tags
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:site', content: '@raphaelmansuy' },
      { name: 'twitter:creator', content: '@raphaelmansuy' },

      // Google Search Console verification
      { name: 'google-site-verification', content: 'YOUR_VERIFICATION_CODE' }, // Replace with your actual verification code
    ],

    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'ADK Training Hub',
      logo: {
        alt: 'ADK Training Hub Logo',
        src: 'img/ADK-512-color.svg',
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
              to: '/docs/hello_world_agent',
            },
            {
              label: 'Mental Models',
              to: '/docs/overview',
            },
            {
              label: 'Code Examples',
              to: '/docs/hello_world_agent',
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
        {
          title: 'Contact',
          items: [
            {
              label: 'Contact the Author',
              to: '/docs/contact',
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
