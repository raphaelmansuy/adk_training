import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Head from '@docusaurus/Head';
import { 
  ProgressIndicator, 
  GitHubStats, 
  LearningPathQuiz, 
  AnimatedCounter 
} from '../components/InteractiveElements';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroLogo}>
            <img src="/adk_training/img/ADK-512-color.svg" alt="Google ADK Training Logo" className={styles.logo} />
          </div>
          <Heading as="h1" className={clsx("hero__title", styles.heroTitle)}>
            Build Production-Ready AI Agents in Days, Not Months
          </Heading>
          <p className={clsx("hero__subtitle", styles.heroSubtitle)}>
            The only comprehensive Google ADK training with 34 hands-on tutorials, 
            working code examples, and production deployment patterns. 
            Learn skills that directly impact your projects and career.
          </p>
          <div className={styles.buttons}>
            <Link
              className={styles.primaryButton}
              to="/docs/hello_world_agent">
              🚀 Start Building Free
            </Link>
            <Link
              className={styles.secondaryButton}
              to="/docs/overview">
              � Read the Guide
            </Link>
          </div>
          <p className={styles.heroStats}>
            ✓ 100% Free & Open Source  •  ✓ No Login Required  •  ✓ Copy-Paste Ready Code
          </p>
        </div>
      </div>
    </header>
  );
}

function QuickWins() {
  return (
    <section className={styles.quickWins}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          What You'll Build (and When)
        </Heading>
        <p className={styles.sectionSubtitle}>
          Stop learning in the abstract. Start building real agents you can show your team today.
        </p>
        <div className={styles.timelineGrid}>
          <div className={styles.timelineCard}>
            <div className={styles.timelineBadge}>⚡ First 30 Minutes</div>
            <h3 className={styles.timelineTitle}>Your First Working Agent</h3>
            <p className={styles.timelineDescription}>
              Deploy a conversational agent with Google Search integration. Copy, paste, run. 
              That simple. No complex setup or infrastructure required.
            </p>
            <Link className={styles.timelineLink} to="/docs/hello_world_agent">
              Start tutorial →
            </Link>
          </div>
          
          <div className={styles.timelineCard}>
            <div className={styles.timelineBadge}>🎯 Day 1</div>
            <h3 className={styles.timelineTitle}>Multi-Agent System</h3>
            <p className={styles.timelineDescription}>
              Build coordinated agent workflows with parallel processing. The kind of architecture 
              senior engineers get paid to design.
            </p>
            <Link className={styles.timelineLink} to="/docs/sequential_workflows">
              View roadmap →
            </Link>
          </div>
          
          <div className={styles.timelineCard}>
            <div className={styles.timelineBadge}>🚀 Week 1</div>
            <h3 className={styles.timelineTitle}>Production Deployment</h3>
            <p className={styles.timelineDescription}>
              Ship to Cloud Run with monitoring, testing, and enterprise integrations. 
              Portfolio-worthy code you can deploy tomorrow.
            </p>
            <Link className={styles.timelineLink} to="/docs/evaluation_testing">
              See deployment patterns →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function LearningPaths() {
  return (
    <section className={styles.learningPaths}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Choose Your Career Path
        </Heading>
        <p className={styles.sectionSubtitle}>
          Pick the track that matches where you want to take your AI development skills
        </p>
        <div className={styles.learningPathsGrid}>
          <div className={styles.pathCard}>
            <span className={styles.pathIcon}>🟢</span>
            <h3 className={styles.pathTitle}>Get Hired Track</h3>
            <p className={styles.pathDescription}>
              Master ADK fundamentals that hiring managers look for. Build portfolio projects 
              that prove you can ship production agents.
            </p>
            <ul className={styles.pathFeatures}>
              <li>Working code examples you can demo</li>
              <li>Tool integration patterns</li>
              <li>State management & workflows</li>
              <li>Interview-ready knowledge</li>
            </ul>
            <Link className={clsx("button button--primary", styles.pathButton)} to="/docs/hello_world_agent">
              Start Building →
            </Link>
          </div>
          
          <div className={styles.pathCard}>
            <span className={styles.pathIcon}>🟡</span>
            <h3 className={styles.pathTitle}>Level Up Track</h3>
            <p className={styles.pathDescription}>
              Advance from junior to senior by mastering complex multi-agent architectures 
              and sophisticated orchestration patterns.
            </p>
            <ul className={styles.pathFeatures}>
              <li>Multi-agent coordination</li>
              <li>Parallel & async workflows</li>
              <li>Agent-to-Agent (A2A) protocol</li>
              <li>MCP tool integration</li>
            </ul>
            <Link className={clsx("button button--primary", styles.pathButton)} to="/docs/sequential_workflows">
              Advance Skills →
            </Link>
          </div>
          
          <div className={styles.pathCard}>
            <span className={styles.pathIcon}>🔴</span>
            <h3 className={styles.pathTitle}>Ship to Prod Track</h3>
            <p className={styles.pathDescription}>
              Deploy enterprise-grade agents with confidence. Learn testing, monitoring, 
              and deployment strategies used by production teams.
            </p>
            <ul className={styles.pathFeatures}>
              <li>Cloud Run & Vertex AI deployment</li>
              <li>Testing & evaluation frameworks</li>
              <li>Observability & debugging</li>
              <li>React/Next.js integration</li>
            </ul>
            <Link className={clsx("button button--primary", styles.pathButton)} to="/docs/evaluation_testing">
              Deploy Now →
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

function StatsSection() {
  return (
    <section className={styles.stats}>
      <div className="container">
        <div className={styles.statsGrid}>
          <div className={styles.statItem}>
            <AnimatedCounter end={34} label="Tutorials Planned" />
          </div>
          <div className={styles.statItem}>
            <AnimatedCounter end={12} label="Currently Available" />
          </div>
          <div className={styles.statItem}>
            <AnimatedCounter end={50} label="Test Cases" />
          </div>
          <div className={styles.statItem}>
            <AnimatedCounter end={100} label="Open Source %" />
          </div>
        </div>
      </div>
    </section>
  );
}

function FeaturesSection() {
  return (
    <section className={styles.featuresSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Why Developers Choose This Training
        </Heading>
        <p className={styles.sectionSubtitle}>
          We respect your time. Every tutorial is designed to teach you something you'll actually use.
        </p>
        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>💻</div>
            <h3 className={styles.featureTitle}>Copy-Paste Ready Code</h3>
            <p className={styles.featureDescription}>
              Every example runs. No pseudo-code, no "figure it out yourself" gaps. 
              Working implementations with tests you can adapt immediately.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🧠</div>
            <h3 className={styles.featureTitle}>Mental Models, Not Just Syntax</h3>
            <p className={styles.featureDescription}>
              Understand the "why" behind agent architecture decisions. 
              Learn frameworks that help you solve new problems, not just memorize patterns.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🎯</div>
            <h3 className={styles.featureTitle}>Aligned with Google's Official ADK</h3>
            <p className={styles.featureDescription}>
              Based on official documentation and patterns from Google's ADK team. 
              Learn the framework as it's meant to be used, with 13.7k+ stars on GitHub.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🚀</div>
            <h3 className={styles.featureTitle}>Production Patterns Included</h3>
            <p className={styles.featureDescription}>
              Deploy to Cloud Run, Vertex AI, or your own infrastructure. 
              Testing, monitoring, and CI/CD patterns that work in real companies.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📈</div>
            <h3 className={styles.featureTitle}>Progressive Complexity</h3>
            <p className={styles.featureDescription}>
              Start with a working agent in 30 minutes. Build to multi-agent systems. 
              Each tutorial builds on previous knowledge without overwhelming you.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🌐</div>
            <h3 className={styles.featureTitle}>Full-Stack Integration Examples</h3>
            <p className={styles.featureDescription}>
              Connect agents to React, Next.js, Streamlit UIs. Learn A2A protocol and MCP. 
              Build complete applications, not just isolated backends.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

function CommunitySection() {
  return (
    <section className={styles.communitySection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Join Our Growing Community
        </Heading>
        <p className={styles.sectionSubtitle}>
          Connect with fellow developers and contribute to the future of AI agent development
        </p>
        <GitHubStats />
        <div className={styles.progressContainer}>
          <ProgressIndicator completed={12} total={34} label="Tutorial Implementation Progress" />
          <ProgressIndicator completed={50} total={100} label="Test Coverage Target" />
        </div>
      </div>
    </section>
  );
}

// Commented out for now since this is a new website - will add real testimonials later
/*
function TestimonialsSection() {
  return (
    <section className={styles.testimonialsSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          What Developers Are Saying
        </Heading>
        <div className={styles.testimonialsGrid}>
          <div className={styles.testimonial}>
            <div className={styles.testimonialContent}>
              "The mental models approach really helped me understand ADK from first principles. 
              The progression from basic concepts to production deployment is excellent."
            </div>
            <div className={styles.testimonialAuthor}>
              <div className={styles.authorAvatar}>🧑‍💻</div>
              <div>
                <div className={styles.authorName}>Alex Chen</div>
                <div className={styles.authorTitle}>AI Engineer @ TechCorp</div>
              </div>
            </div>
          </div>
          
          <div className={styles.testimonial}>
            <div className={styles.testimonialContent}>
              "Comprehensive coverage of Google ADK with hands-on examples. 
              The testing patterns and deployment guides saved me weeks of research."
            </div>
            <div className={styles.testimonialAuthor}>
              <div className={styles.authorAvatar}>👩‍💻</div>
              <div>
                <div className={styles.authorName}>Sarah Johnson</div>
                <div className={styles.authorTitle}>Senior Developer @ StartupAI</div>
              </div>
            </div>
          </div>
          
          <div className={styles.testimonial}>
            <div className={styles.testimonialContent}>
              "Perfect for both beginners and experienced developers. 
              The sequential learning approach makes complex topics accessible."
            </div>
            <div className={styles.testimonialAuthor}>
              <div className={styles.authorAvatar}>🧑‍🔬</div>
              <div>
                <div className={styles.authorName}>Dr. Michael Rodriguez</div>
                <div className={styles.authorTitle}>AI Researcher @ Google</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
*/

function GetStartedSection() {
  return (
    <section className={styles.getStartedSection}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Not Sure Where to Start?
        </Heading>
        <p className={styles.sectionSubtitle}>
          Take our quick quiz to find the perfect learning path for your experience level
        </p>
        <LearningPathQuiz />
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Google ADK Training: Build Production AI Agents Fast (34 Free Tutorials)"
      description="Learn Google Agent Development Kit (ADK) with 34 hands-on tutorials. Build multi-agent systems, deploy to production, integrate with React/Next.js. Free, open-source, copy-paste ready code for Python developers.">
      <Head>
        {/* Article Schema */}
        <script type="application/ld+json">
          {JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Article',
            headline: 'Google ADK Training: Build Production AI Agents Fast (34 Free Tutorials)',
            description: 'Learn Google Agent Development Kit (ADK) with 34 hands-on tutorials. Build multi-agent systems, deploy to production, integrate with React/Next.js. Free, open-source, copy-paste ready code.',
            image: 'https://raphaelmansuy.github.io/adk_training/img/docusaurus-social-card.jpg',
            datePublished: '2025-01-01',
            dateModified: '2025-10-14',
            author: {
              '@type': 'Person',
              name: 'Raphael Mansuy',
              url: 'https://github.com/raphaelmansuy'
            },
            publisher: {
              '@type': 'Organization',
              name: 'ADK Training Hub',
              logo: {
                '@type': 'ImageObject',
                url: 'https://raphaelmansuy.github.io/adk_training/img/ADK-512-color.svg'
              }
            },
            mainEntityOfPage: {
              '@type': 'WebPage',
              '@id': 'https://raphaelmansuy.github.io/adk_training/'
            },
            keywords: ['Google ADK tutorial', 'Agent Development Kit', 'build AI agents', 'multi-agent systems', 'agent orchestration', 'Google Gemini agents', 'ADK Python', 'production AI agents', 'deploy agents cloud run', 'agent architecture patterns', 'A2A protocol', 'MCP tools integration', 'agent workflow', 'AI agent framework']
          })}
        </script>

        {/* Breadcrumb Schema */}
        <script type="application/ld+json">
          {JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            itemListElement: [
              {
                '@type': 'ListItem',
                position: 1,
                name: 'Home',
                item: 'https://raphaelmansuy.github.io/adk_training/'
              }
            ]
          })}
        </script>

        {/* Course/CourseInstance Schema for the learning platform */}
        <script type="application/ld+json">
          {JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Course',
            name: 'Google ADK Training Hub',
            description: 'Complete training program for Google Agent Development Kit with 34 tutorials and production-ready examples.',
            provider: {
              '@type': 'Organization',
              name: 'ADK Training Project',
              url: 'https://raphaelmansuy.github.io/adk_training/'
            },
            courseMode: 'online',
            educationalLevel: 'beginner to advanced',
            teaches: [
              'Google Agent Development Kit',
              'AI Agent Development',
              'Google Gemini Integration',
              'Python Programming',
              'Machine Learning'
            ],
            hasCourseInstance: {
              '@type': 'CourseInstance',
              courseMode: 'online',
              instructor: {
                '@type': 'Person',
                name: 'Raphael Mansuy'
              }
            }
          })}
        </script>
      </Head>
      <HomepageHeader />
      <main>
        <QuickWins />
        <StatsSection />
        <LearningPaths />
        <FeaturesSection />
        {/* <TestimonialsSection /> - Commented out until we have real testimonials */}
        <CommunitySection />
        <GetStartedSection />
      </main>
    </Layout>
  );
}
