import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/overview">
            Start Learning - 2min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

function LearningPaths() {
  return (
    <section className={styles.learningPaths}>
      <div className="container">
        <div className="row">
          <div className="col col--4">
            <div className="card">
              <div className="card__header">
                <h3>🟢 Foundation</h3>
              </div>
              <div className="card__body">
                <p>Master the basics of ADK agent development</p>
                <ul>
                  <li>Hello World Agent</li>
                  <li>Function Tools</li>
                  <li>OpenAPI Tools</li>
                </ul>
              </div>
              <div className="card__footer">
                <Link className="button button--primary" to="/docs/tutorial/01_hello_world_agent">
                  Start Foundation
                </Link>
              </div>
            </div>
          </div>
          <div className="col col--4">
            <div className="card">
              <div className="card__header">
                <h3>🟡 Workflows</h3>
              </div>
              <div className="card__body">
                <p>Build sophisticated multi-agent systems</p>
                <ul>
                  <li>Sequential Workflows</li>
                  <li>Parallel Processing</li>
                  <li>Multi-Agent Systems</li>
                  <li>Loop Agents</li>
                </ul>
              </div>
              <div className="card__footer">
                <Link className="button button--primary" to="/docs/tutorial/01_hello_world_agent">
                  Start Workflows
                </Link>
              </div>
            </div>
          </div>
          <div className="col col--4">
            <div className="card">
              <div className="card__header">
                <h3>🔴 Production</h3>
              </div>
              <div className="card__body">
                <p>Deploy production-ready AI agents</p>
                <ul>
                  <li>State & Memory</li>
                  <li>Callbacks & Guardrails</li>
                  <li>Evaluation & Testing</li>
                  <li>Built-in Tools</li>
                </ul>
              </div>
              <div className="card__footer">
                <Link className="button button--primary" to="/docs/tutorial/01_hello_world_agent">
                  Start Production
                </Link>
              </div>
            </div>
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
        <div className="row">
          <div className="col col--3">
            <div className="text--center">
              <h2>34</h2>
              <p>Tutorials</p>
            </div>
          </div>
          <div className="col col--3">
            <div className="text--center">
              <h2>12</h2>
              <p>Implemented</p>
            </div>
          </div>
          <div className="col col--3">
            <div className="text--center">
              <h2>70+</h2>
              <p>Tests</p>
            </div>
          </div>
          <div className="col col--3">
            <div className="text--center">
              <h2>100%</h2>
              <p>Open Source</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="ADK Training Hub - Master Google Agent Development Kit"
      description="Comprehensive training for Google ADK with 34 tutorials, mental models, and production-ready examples">
      <HomepageHeader />
      <main>
        <LearningPaths />
        <StatsSection />
      </main>
    </Layout>
  );
}
