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
  title: 'Google ADK Training Hub',
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

  // Broken link handling: 'warn' shows warnings during build, 'throw' fails the build
  // Changed from 'ignore' to 'warn' to catch broken internal doc links early
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  onBrokenAnchors: 'warn',

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
    // ========================================
    // Mobile & Viewport Configuration (PWA)
    // ========================================
    {
      tagName: 'meta',
      attributes: {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1.0, viewport-fit=cover, user-scalable=yes, maximum-scale=5',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        name: 'mobile-web-app-capable',
        content: 'yes',
      },
    },
    // ========================================
    // Security Headers for PWA
    // ========================================
    {
      tagName: 'meta',
      attributes: {
        'http-equiv': 'X-UA-Compatible',
        content: 'IE=edge',
      },
    },
    {
      tagName: 'meta',
      attributes: {
        'http-equiv': 'Content-Security-Policy',
        content: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://www.google-analytics.com https://www.googletagmanager.com https://giscus.app; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https: wss:; frame-src https://giscus.app; frame-ancestors 'self'; base-uri 'self'; form-action 'self';",
      },
    },
    // ========================================
    // Performance Optimizations for Core Web Vitals
    // ========================================
    {
      tagName: 'link',
      attributes: {
        rel: 'preconnect',
        href: 'https://fonts.googleapis.com',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: 'anonymous',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'dns-prefetch',
        href: 'https://www.google-analytics.com',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'dns-prefetch',
        href: 'https://www.googletagmanager.com',
      },
    },
    // Preload critical resources
    {
      tagName: 'link',
      attributes: {
        rel: 'preload',
        href: '/adk_training/img/ADK-512-color.svg',
        as: 'image',
        type: 'image/svg+xml',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'prefetch',
        href: '/adk_training/offline.html',
        as: 'document',
      },
    },
    // Organization schema
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Organization',
        name: 'Google ADK Training Hub',
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
        name: 'Google ADK Training Hub',
        url: 'https://raphaelmansuy.github.io/adk_training/',
        description: 'Master Google Agent Development Kit from first principles to production deployment.',
        potentialAction: {
          '@type': 'SearchAction',
          target: 'https://raphaelmansuy.github.io/adk_training/search?q={search_term_string}',
          'query-input': 'required name=search_term_string',
        },
      }),
    },

    // Course schema
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Course',
        name: 'Google ADK Training Hub - Build Production AI Agents',
        description: 'Complete hands-on training for Google Agent Development Kit with 34 free tutorials, production deployment patterns, multi-agent systems, and full-stack integration examples.',
        provider: {
          '@type': 'Organization',
          name: 'Google ADK Training Hub',
          url: 'https://raphaelmansuy.github.io/adk_training/',
        },
        courseMode: 'online',
        educationalLevel: 'beginner to advanced',
        teaches: [
          'Google Agent Development Kit (ADK)',
          'Multi-Agent Systems Architecture',
          'Agent Orchestration Patterns',
          'Production Agent Deployment',
          'Google Gemini Integration',
          'A2A Protocol Implementation',
          'MCP Tools Integration',
          'Agent Testing and Evaluation',
          'Cloud Run Deployment',
          'Vertex AI Agent Engine',
          'Google Cloud Pub/Sub Integration',
          'Event-Driven Agent Architectures',
        ],
        hasCourseInstance: {
          '@type': 'CourseInstance',
          courseMode: 'online',
          courseWorkload: 'PT34H',
          instructor: {
            '@type': 'Person',
            name: 'Raphael Mansuy',
          },
        },
        offers: {
          '@type': 'Offer',
          price: '0',
          priceCurrency: 'USD',
          availability: 'https://schema.org/InStock',
          category: 'Free',
        },
      }),
    },

    // FAQ Schema for rich snippets
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        mainEntity: [
          {
            '@type': 'Question',
            name: 'What is Google ADK (Agent Development Kit)?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'Google Agent Development Kit (ADK) is a comprehensive framework for building production-ready AI agents using Google Gemini models. It provides tools for agent orchestration, multi-agent systems, state management, and deployment patterns.',
            },
          },
          {
            '@type': 'Question',
            name: 'Is Google ADK training free?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'Yes! All 34 tutorials, mental models, code examples, and production deployment guides are completely free. You can access everything without any registration or payment.',
            },
          },
          {
            '@type': 'Question',
            name: 'What will I learn from Google ADK Training Hub?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'You will learn to build production AI agents from scratch, including multi-agent systems, agent orchestration patterns, Google Gemini integration, deployment on Cloud Run and Vertex AI, UI integration (React, Next.js, Streamlit), MCP tools, A2A protocol, and comprehensive testing strategies.',
            },
          },
          {
            '@type': 'Question',
            name: 'Do I need prior AI experience to start?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'No prior AI experience required! The training starts from first principles with a "Hello World" agent and progressively covers advanced topics. Basic Python or JavaScript knowledge is helpful but not mandatory.',
            },
          },
          {
            '@type': 'Question',
            name: 'How long does it take to complete the training?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'The complete training comprises 34 tutorials totaling approximately 34 hours of hands-on learning. You can go at your own pace - complete it in a week of intensive study or spread it over several weeks.',
            },
          },
          {
            '@type': 'Question',
            name: 'Can I deploy agents to production after this training?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'Absolutely! The training includes comprehensive production deployment guides for Google Cloud Run, Vertex AI Agent Engine, and GKE. You will learn testing, monitoring, and best practices for production-grade AI agents.',
            },
          },
        ],
      }),
    },

    // Breadcrumb Schema for better navigation
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: 'https://raphaelmansuy.github.io/adk_training/',
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Tutorials',
            item: 'https://raphaelmansuy.github.io/adk_training/docs/',
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: 'Mental Models',
            item: 'https://raphaelmansuy.github.io/adk_training/docs/overview',
          },
        ],
      }),
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          path: path.resolve(__dirname, './docs'), // Absolute path to docs directory (contains til/ subdirectory)
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/raphaelmansuy/adk_training/edit/main/docs/docs/',
          // SEO: Add canonical URLs to prevent duplicate content issues
          // This ensures each page has a canonical tag pointing to the preferred URL
          routeBasePath: 'docs',
          // Show last update time and author for better SEO signals
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
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
          // authorsMapPath is relative to blog content directory (blog/)
          // Default is 'authors.yml' - file should be at blog/authors.yml
          authorsMapPath: 'authors.yml',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'ignore',
          onUntruncatedBlogPosts: 'warn',
          // SEO: Show last update time for better freshness signals
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
          // SEO: Generate proper blog post schema for rich snippets
          // Docusaurus automatically adds BlogPosting schema to blog posts
          blogTitle: 'Google ADK Training Blog',
          blogDescription: 'Latest updates, tutorials, and insights about Google Agent Development Kit',
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
        /**
         * 🔴 CRITICAL: Replace 'GA_MEASUREMENT_ID' with your actual Google Analytics 4 Measurement ID
         * 
         * How to get your GA4 Measurement ID:
         * 1. Go to https://analytics.google.com
         * 2. Create a new GA4 property (if you don't have one)
         * 3. Property name: "Google ADK Training Hub"
         * 4. Data stream platform: Web
         * 5. Website URL: https://raphaelmansuy.github.io
         * 6. Stream name: adk_training
         * 7. Copy the Measurement ID (format: G-XXXXXXXXXX)
         * 8. Replace 'GA_MEASUREMENT_ID' below with your actual ID
         * 
         * Example: trackingID: 'G-ABC123DEF4',
         * 
         * See implementation guide: /docs/seo_audit/seo_implementation_guide
         */
        trackingID: 'GA_MEASUREMENT_ID', // ⚠️ PLACEHOLDER - NOT TRACKING until you add your actual ID
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
      require.resolve('./plugins/docusaurus-plugin-og-image-dimensions.js'),
      {
        // Plugin to handle custom og:image dimensions for blog posts
      },
    ],
    // TODO: Re-enable PWA plugin after creating custom PwaReloadPopup theme component
    // [
    //   '@docusaurus/plugin-pwa',
    //   { ... PWA configuration ... }
    // ],
    // TODO: Add Giscus plugin when available
    // TODO: Add social sharing plugin
  ],

  themeConfig: {
    // Enhanced metadata for better SEO
    metadata: [
      // Basic SEO meta tags with competitor-informed long-tail keywords
      { name: 'keywords', content: 'Google ADK tutorial, Agent Development Kit Python, build AI agents, multi-agent systems, agent orchestration, Google Gemini agents, ADK training, production AI agents, deploy agents cloud run, agent architecture patterns, A2A protocol, MCP tools, sequential workflows, parallel agents, agent deployment, Vertex AI agents, agent testing, agent evaluation, React agent integration, Next.js AI agents, Streamlit agents, agent state management, tool integration, OpenAPI agents, function calling agents, agent workflows, ADK examples, ADK code samples, learn Google ADK, ADK documentation' },
      { name: 'author', content: 'Raphael Mansuy' },
      { name: 'robots', content: 'index, follow' },
      { name: 'language', content: 'English' },
      { name: 'revisit-after', content: '3 days' },

      // Open Graph meta tags for better social sharing
      { property: 'og:type', content: 'website' },
      { property: 'og:site_name', content: 'Google ADK Training Hub' },
      { property: 'og:locale', content: 'en_US' },
      { property: 'og:title', content: 'Google ADK Training Hub - Master AI Agent Development' },
      { property: 'og:description', content: 'Complete hands-on training for Google Agent Development Kit with 34 free tutorials, production deployment patterns, multi-agent systems, and full-stack integration examples.' },
      { property: 'og:image', content: 'https://raphaelmansuy.github.io/adk_training/img/docusaurus-social-card.jpg' },
      { property: 'og:image:width', content: '1200' },
      { property: 'og:image:height', content: '630' },
      { property: 'og:image:alt', content: 'Google ADK Training Hub - Learn to build production AI agents with Google\'s Agent Development Kit' },
      { property: 'og:url', content: 'https://raphaelmansuy.github.io/adk_training/' },

      // Twitter Card meta tags for optimal Twitter sharing
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:site', content: '@raphaelmansuy' },
      { name: 'twitter:creator', content: '@raphaelmansuy' },
      { name: 'twitter:title', content: 'Google ADK Training Hub - Master AI Agent Development' },
      { name: 'twitter:description', content: 'Complete hands-on training for Google Agent Development Kit with 34 free tutorials, production deployment patterns, multi-agent systems, and full-stack integration examples.' },
      { name: 'twitter:image', content: 'https://raphaelmansuy.github.io/adk_training/img/docusaurus-social-card.jpg' },
      { name: 'twitter:image:alt', content: 'Google ADK Training Hub - Learn to build production AI agents with Google\'s Agent Development Kit' },

      // LinkedIn meta tags
      { property: 'og:type', content: 'website' },
      { property: 'og:site_name', content: 'Google ADK Training Hub' },

      /**
       * 🔴 CRITICAL: Google Search Console Verification
       * 
       * Replace 'tuQTXHERxeAB5YzYV7ZHPEFqwMYBCEBVmsYy_m-nJEU' with your actual verification code
       * 
       * How to get your verification code:
       * 1. Go to https://search.google.com/search-console
       * 2. Click "Add property"
       * 3. Select "URL prefix"
       * 4. Enter: https://raphaelmansuy.github.io/adk_training/
       * 5. Choose "HTML tag" verification method
       * 6. Copy the content value from: <meta name="google-site-verification" content="XXXXX"/>
       * 7. Replace the content value below with your actual code
       * 8. Deploy your site, then click "Verify" in Search Console
       * 
       * After verification, you can:
       * - Submit your sitemap: sitemap.xml
       * - Monitor indexing status
       * - View search performance data
       * 
       * See implementation guide: /docs/seo_audit/seo_implementation_guide
       */
      { name: 'google-site-verification', content: 'tuQTXHERxeAB5YzYV7ZHPEFqwMYBCEBVmsYy_m-nJEU' }, // ⚠️ PLACEHOLDER - Site not verified until you add your actual code
    ],

    // Replace with your project's social card
    image: 'https://raphaelmansuy.github.io/adk_training/img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Google ADK Training Hub',
      logo: {
        alt: 'Google ADK Training Hub Logo',
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
        {
          type: 'dropdown',
          label: '📚 Today I Learn',
          position: 'left',
          items: [
            {
              label: 'TIL Index',
              to: '/docs/til/til_index',
              description: 'Browse all TIL articles',
            },
            {
              label: 'Context Compaction (Oct 19)',
              to: '/docs/til/til_context_compaction_20250119',
              description: 'Reduce token usage in long conversations',
            },
            {
              label: 'TIL Guidelines',
              to: '/docs/til/til_template',
              description: 'How to create TIL articles',
            },
          ],
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
