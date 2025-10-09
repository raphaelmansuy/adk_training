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
            <img src="/adk_training/img/ADK-512-color.svg" alt="ADK Logo" className={styles.logo} />
          </div>
          <Heading as="h1" className={clsx("hero__title", styles.heroTitle)}>
            {siteConfig.title}
          </Heading>
          <p className={clsx("hero__subtitle", styles.heroSubtitle)}>
            Master Google Agent Development Kit from first principles to production deployment. 
            Build intelligent AI agents with 34 comprehensive tutorials and hands-on examples.
          </p>
          <div className={styles.buttons}>
            <Link
              className={styles.primaryButton}
              to="/docs/overview">
              🚀 Start Learning Now
            </Link>
            <Link
              className={styles.secondaryButton}
              to="/docs/tutorial_index">
              📚 Browse Tutorials
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

function LearningPaths() {
  return (
    <section className={styles.learningPaths}>
      <div className="container">
        <Heading as="h2" className={styles.sectionTitle}>
          Choose Your Learning Path
        </Heading>
        <p className={styles.sectionSubtitle}>
          Structured learning tracks designed to take you from beginner to expert in Google ADK development
        </p>
        <div className={styles.learningPathsGrid}>
          <div className={styles.pathCard}>
            <span className={styles.pathIcon}>🟢</span>
            <h3 className={styles.pathTitle}>Foundation Track</h3>
            <p className={styles.pathDescription}>
              Perfect for beginners. Learn the core concepts of ADK agent development with hands-on examples.
            </p>
            <ul className={styles.pathFeatures}>
              <li>Hello World Agent</li>
              <li>Function & OpenAPI Tools</li>
              <li>Sequential Workflows</li>
              <li>State Management</li>
            </ul>
            <Link className={clsx("button button--primary", styles.pathButton)} to="/docs/hello_world_agent">
              Start Foundation Track →
            </Link>
          </div>
          
          <div className={styles.pathCard}>
            <span className={styles.pathIcon}>🟡</span>
            <h3 className={styles.pathTitle}>Advanced Workflows</h3>
            <p className={styles.pathDescription}>
              Build sophisticated multi-agent systems with parallel processing and complex orchestration.
            </p>
            <ul className={styles.pathFeatures}>
              <li>Parallel Processing</li>
              <li>Multi-Agent Systems</li>
              <li>Loop Agents & Critics</li>
              <li>Event Handling</li>
            </ul>
            <Link className={clsx("button button--primary", styles.pathButton)} to="/docs/sequential_workflows">
              Explore Workflows →
            </Link>
          </div>
          
          <div className={styles.pathCard}>
            <span className={styles.pathIcon}>🔴</span>
            <h3 className={styles.pathTitle}>Production Ready</h3>
            <p className={styles.pathDescription}>
              Deploy production-grade AI agents with testing, observability, and enterprise integration.
            </p>
            <ul className={styles.pathFeatures}>
              <li>Testing & Evaluation</li>
              <li>Deployment Strategies</li>
              <li>Observability & Monitoring</li>
              <li>UI Integration</li>
            </ul>
            <Link className={clsx("button button--primary", styles.pathButton)} to="/docs/evaluation_testing">
              Go Production →
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
          Why Choose ADK Training Hub?
        </Heading>
        <div className={styles.featuresGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🧠</div>
            <h3 className={styles.featureTitle}>Mental Models</h3>
            <p className={styles.featureDescription}>
              Comprehensive mental frameworks for understanding ADK and Generative AI concepts from first principles.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🛠️</div>
            <h3 className={styles.featureTitle}>Hands-on Examples</h3>
            <p className={styles.featureDescription}>
              Every tutorial includes working code examples, complete implementations, and comprehensive test suites.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📈</div>
            <h3 className={styles.featureTitle}>Progressive Learning</h3>
            <p className={styles.featureDescription}>
              Structured curriculum that builds from basic concepts to advanced production deployment patterns.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🚀</div>
            <h3 className={styles.featureTitle}>Production Ready</h3>
            <p className={styles.featureDescription}>
              Learn deployment strategies, testing patterns, and enterprise integration for real-world applications.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🎯</div>
            <h3 className={styles.featureTitle}>Google Official</h3>
            <p className={styles.featureDescription}>
              Based on official Google ADK documentation and best practices from the core development team.
            </p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🌐</div>
            <h3 className={styles.featureTitle}>Full Stack Integration</h3>
            <p className={styles.featureDescription}>
              Integrate with React, Next.js, Streamlit, and other modern frameworks for complete AI applications.
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
      title="ADK Training Hub - Master Google Agent Development Kit"
      description="Comprehensive training for Google ADK with 34 tutorials, mental models, and production-ready examples. Learn to build intelligent AI agents from first principles to deployment.">
      <Head>
        {/* Article Schema */}
        <script type="application/ld+json">
          {JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Article',
            headline: 'ADK Training Hub - Master Google Agent Development Kit',
            description: 'Comprehensive training for Google ADK with 34 tutorials, mental models, and production-ready examples. Learn to build intelligent AI agents from first principles to deployment.',
            image: 'https://raphaelmansuy.github.io/adk_training/img/docusaurus-social-card.jpg',
            datePublished: '2025-01-01',
            dateModified: '2025-10-09',
            author: {
              '@type': 'Person',
              name: 'Raphael Mansuy',
              url: 'https://github.com/raphaelmansuy'
            },
            publisher: {
              '@type': 'Organization',
              name: 'ADK Training Project',
              logo: {
                '@type': 'ImageObject',
                url: 'https://raphaelmansuy.github.io/adk_training/img/ADK-512-color.svg'
              }
            },
            mainEntityOfPage: {
              '@type': 'WebPage',
              '@id': 'https://raphaelmansuy.github.io/adk_training/'
            },
            keywords: ['Google ADK', 'Agent Development Kit', 'AI agents', 'tutorials', 'Google Gemini', 'machine learning']
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
        <LearningPaths />
        <StatsSection />
        <FeaturesSection />
        {/* <TestimonialsSection /> - Commented out until we have real testimonials */}
        <CommunitySection />
        <GetStartedSection />
      </main>
    </Layout>
  );
}
