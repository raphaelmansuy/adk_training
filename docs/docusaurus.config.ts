import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import * as path from 'path';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * 🌟 Community & Social Features Added:
 *
 * 1. Enhanced Footer Links:
 *    - Twitter/X
 *    - Newsletter Signup
 *    - Calendly for scheduling calls
 *
 * 2. Navbar Social Links:
 *    - Twitter icon in navbar
 *
 * 3. Comments System:
 *    - Giscus integration ready (requires manual setup)
 *    - TODO: Create custom Giscus component in src/components/Comments.tsx
 *    - TODO: Add @giscus/react to package.json
 *
 * 4. Social Sharing:
 *    - Ready for custom social sharing component
 *    - TODO: Create src/components/SocialShare.tsx
 *
 * 5. Enhanced Metadata:
 *    - LinkedIn Open Graph tags
 *    - Additional social profiles in structured data
 *
 * Manual Setup Instructions:
 * 1. Install Giscus: npm install @giscus/react
 * 2. Create src/components/Comments.tsx with Giscus component
 * 3. Create src/components/SocialShare.tsx for sharing buttons
 * 4. Get your Giscus repo ID and category ID from: https://giscus.app/
 * 5. Update social media URLs with your actual profiles
 * 6. Set up newsletter service and update URL
 */

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
          'https://twitter.com/raphaelmansuy',
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
    [
      '@easyops-cn/docusaurus-search-local',
      {
        // https://github.com/easyops-cn/docusaurus-search-local
        hashed: true,
        indexDocs: true,
        indexBlog: true,
        indexPages: false,
        docsRouteBasePath: '/docs',
        blogRouteBasePath: '/blog',
        language: ['en'],
      },
    ],
    [
      '@docusaurus/plugin-pwa',
      {
        debug: true,
        offlineModeActivationStrategies: [
          'appInstalled',
          'standalone',
          'queryString',
        ],
        pwaHead: [
          {
            tagName: 'link',
            rel: 'icon',
            href: '/img/favicon.ico',
          },
          {
            tagName: 'link',
            rel: 'manifest',
            href: '/manifest.json',
          },
          {
            tagName: 'meta',
            name: 'theme-color',
            content: '#25c2a0',
          },
          {
            tagName: 'meta',
            name: 'apple-mobile-web-app-capable',
            content: 'yes',
          },
          {
            tagName: 'meta',
            name: 'apple-mobile-web-app-status-bar-style',
            content: '#000',
          },
          {
            tagName: 'link',
            rel: 'apple-touch-icon',
            href: '/img/ADK-192.png',
          },
          {
            tagName: 'link',
            rel: 'mask-icon',
            href: '/img/favicon.ico',
            color: '#25c2a0',
          },
          {
            tagName: 'meta',
            name: 'msapplication-TileImage',
            content: '/img/ADK-144.png',
          },
          {
            tagName: 'meta',
            name: 'msapplication-TileColor',
            content: '#000',
          },
        ],
      },
    ],
    // TODO: Add Giscus plugin when available
    // TODO: Add social sharing plugin
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

      // LinkedIn meta tags
      { property: 'og:type', content: 'website' },
      { property: 'og:site_name', content: 'ADK Training Hub' },

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
        {
          href: 'https://twitter.com/raphaelmansuy',
          label: 'Twitter',
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
            {
              label: 'Twitter/X',
              href: 'https://twitter.com/raphaelmansuy',
            },
            {
              label: 'Newsletter',
              href: 'https://newsletter.adk-training.com',
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
            {
              label: 'Newsletter Signup',
              href: 'https://newsletter.adk-training.com',
            },
            {
              label: 'Schedule a Call',
              href: 'https://calendly.com/raphaelmansuy',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} ADK Training Project. Built with Docusaurus.`,
    },
    // prism: {
    //   theme: prismThemes.github,
    //   darkTheme: prismThemes.dracula,
    // },
    mermaid: {
      theme: { light: 'base', dark: 'base' },
      options: {
        theme: 'base',
        themeVariables: {
          fontFamily: 'JetBrains Mono, Fira Code, SF Mono, Monaco, Cascadia Code, Roboto Mono, Consolas, Courier New, monospace',
          fontSize: '14px',
          darkMode: false,
          background: 'transparent',
          primaryColor: '#3182ce',
          primaryTextColor: '#2d3748',
          primaryBorderColor: '#4a5568',
          lineColor: '#3182ce',
          secondaryColor: '#e2e8f0',
          tertiaryColor: '#f7fafc',
          textColor: '#2d3748',
          mainBkg: '#f8f9fa',
          secondBkg: '#e2e8f0',
          border1: '#4a5568',
          border2: '#718096',
        },
        flowchart: {
          useMaxWidth: true,
          htmlLabels: true,
          curve: 'basis',
          nodeSpacing: 50,
          rankSpacing: 50,
        },
        sequence: {
          useMaxWidth: true,
          htmlLabels: true,
          messageFontSize: 14,
          noteFontSize: 12,
          actorFontSize: 14,
        },
        gantt: {
          useMaxWidth: true,
          htmlLabels: true,
          fontSize: 14,
        },
      },
    },
    // TODO: Add community features config when plugins are available
    // giscus: { ... },
    // share: { ... },
  } satisfies Preset.ThemeConfig,
};

export default config;
