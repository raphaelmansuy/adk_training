import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

export default function NotFound() {
  const {siteConfig} = useDocusaurusContext();
  const [clickCount, setClickCount] = useState(0);
  const [showEasterEgg, setShowEasterEgg] = useState(false);
  const [robotMood, setRobotMood] = useState('confused');

  const robotEmojis = {
    confused: '🤖',
    happy: '🤖😊',
    excited: '🤖🤩',
    dancing: '🤖💃',
    thinking: '🤖🤔'
  };

  const funFacts = [
    "🚀 ADK stands for Agent Development Kit",
    "🧠 Gemini 2.0 powers the most advanced agents",
    "🔧 You can build 34 different agent patterns with ADK",
    "⚡ Agents can run parallel tools automatically",
    "🎯 ADK agents can remember conversations across sessions",
    "🌐 Agents can call other agents remotely (A2A protocol)",
    "🔍 Agents can search the web and verify facts",
    "🎨 Agents can generate images and analyze them",
    "📊 Agents can process data and create visualizations",
    "🎵 Agents can even handle audio and video streams!"
  ];

  const [currentFact, setCurrentFact] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFact((prev) => (prev + 1) % funFacts.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleRobotClick = () => {
    setClickCount(prev => prev + 1);
    if (clickCount === 2) {
      setRobotMood('happy');
    } else if (clickCount === 5) {
      setRobotMood('excited');
    } else if (clickCount === 10) {
      setRobotMood('dancing');
      setShowEasterEgg(true);
    }
  };

  const resetRobot = () => {
    setClickCount(0);
    setRobotMood('confused');
    setShowEasterEgg(false);
  };

  return (
    <Layout
      title="Agent Not Found! 🤖"
      description="Oops! This page seems to have wandered off into the digital multiverse! Let's get you back to building amazing AI agents with ADK!">
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div style={{
              textAlign: 'center',
              padding: '3rem',
              background: 'linear-gradient(135deg, var(--ifm-color-primary-lightest) 0%, var(--ifm-color-primary-lighter) 100%)',
              borderRadius: '1rem',
              boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
              marginBottom: '2rem',
              position: 'relative',
              overflow: 'hidden'
            }}>

              {/* Floating particles animation */}
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                pointerEvents: 'none',
                overflow: 'hidden'
              }}>
                {[...Array(20)].map((_, i) => (
                  <div
                    key={i}
                    style={{
                      position: 'absolute',
                      width: '4px',
                      height: '4px',
                      background: 'var(--ifm-color-primary)',
                      borderRadius: '50%',
                      opacity: 0.3,
                      left: `${Math.random() * 100}%`,
                      top: `${Math.random() * 100}%`,
                      animation: `float ${2 + Math.random() * 3}s ease-in-out infinite`,
                      animationDelay: `${Math.random() * 2}s`
                    }}
                  />
                ))}
              </div>

              {/* Animated 404 */}
              <div style={{
                fontSize: '8rem',
                fontWeight: 'bold',
                background: 'linear-gradient(45deg, var(--ifm-color-primary), var(--ifm-color-primary-dark))',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                marginBottom: '1rem',
                animation: 'bounce 2s infinite',
                cursor: 'pointer',
                textShadow: '0 0 20px rgba(0, 123, 255, 0.3)'
              }}
              onClick={handleRobotClick}>
                4<span style={{color: 'var(--ifm-color-danger)'}}>0</span>4
              </div>

              {/* Interactive Robot */}
              <div
                style={{
                  fontSize: '4rem',
                  marginBottom: '1rem',
                  filter: 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))',
                  cursor: 'pointer',
                  transition: 'transform 0.2s ease',
                  animation: robotMood === 'dancing' ? 'dance 1s ease-in-out infinite' : 'none'
                }}
                onClick={handleRobotClick}
                title="Click me! I'm feeling a bit lost too..."
              >
                {robotEmojis[robotMood]}
              </div>

              <h1 className="hero__title" style={{
                fontSize: '2.5rem',
                marginBottom: '1rem',
                color: 'var(--ifm-color-primary-darkest)',
                textShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
              }}>
                Agent Not Found! {robotMood === 'dancing' ? '🕺' : '🤖'}
              </h1>

              <p style={{
                fontSize: '1.2rem',
                marginBottom: '2rem',
                color: 'var(--ifm-color-emphasis-700)',
                lineHeight: '1.6'
              }}>
                {showEasterEgg ? (
                  <span style={{fontSize: '1.4rem', fontWeight: 'bold', color: 'var(--ifm-color-success)'}}>
                    🎉 CONGRATULATIONS! You've discovered the secret agent dance party! 🕺💃<br/>
                    <small style={{fontSize: '0.9rem', color: 'var(--ifm-color-emphasis-600)'}}>
                      (Click the robot again to reset)
                    </small>
                  </span>
                ) : (
                  <>
                    Looks like this page got lost in the digital multiverse! Our AI agents are great at finding things,
                    but even they can't locate this one. Don't worry though - let's get you back to building amazing AI agents with ADK!
                  </>
                )}
              </p>

              {/* Fun Facts Carousel */}
              <div style={{
                background: 'rgba(255, 255, 255, 0.8)',
                padding: '1.5rem',
                borderRadius: '0.5rem',
                marginBottom: '2rem',
                textAlign: 'left',
                minHeight: '80px',
                display: 'flex',
                alignItems: 'center'
              }}>
                <div style={{width: '100%'}}>
                  <h3 style={{
                    color: 'var(--ifm-color-primary)',
                    marginBottom: '0.5rem',
                    fontSize: '1.1rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    💡 Fun Fact #{currentFact + 1} <span style={{fontSize: '0.8rem'}}>🔄</span>
                  </h3>
                  <p style={{
                    margin: '0',
                    fontSize: '0.95rem',
                    color: 'var(--ifm-color-emphasis-700)',
                    animation: 'fadeIn 0.5s ease-in-out'
                  }}>
                    {funFacts[currentFact]}
                  </p>
                </div>
              </div>

              {/* ASCII Art Agent */}
              <div style={{
                background: 'rgba(0, 0, 0, 0.05)',
                padding: '1rem',
                borderRadius: '0.5rem',
                marginBottom: '2rem',
                fontFamily: 'monospace',
                fontSize: '0.8rem',
                color: 'var(--ifm-color-emphasis-600)',
                whiteSpace: 'pre'
              }}>
{`     🤖 ADK Agent Status: CONFUSED 🤖
    ┌─────────────────────────────┐
    │ 🔍 Scanning for lost pages... │
    │ 📡 Signal strength: WEAK     │
    │ 🧠 Neural network: ACTIVE    │
    │ ⚡ Power level: 404%         │
    └─────────────────────────────┘`}
              </div>

              {/* Action Buttons */}
              <div style={{
                display: 'flex',
                gap: '1rem',
                justifyContent: 'center',
                flexWrap: 'wrap',
                marginBottom: '2rem'
              }}>
                <Link
                  className="button button--primary button--lg"
                  to="/docs/overview"
                  style={{
                    padding: '0.75rem 1.5rem',
                    fontSize: '1.1rem',
                    fontWeight: '600',
                    textDecoration: 'none',
                    borderRadius: '0.5rem',
                    transition: 'all 0.2s ease',
                    boxShadow: '0 2px 8px rgba(0, 123, 255, 0.3)'
                  }}>
                  🏠 Go to Overview
                </Link>

                <Link
                  className="button button--secondary button--lg"
                  to="/docs/hello_world_agent"
                  style={{
                    padding: '0.75rem 1.5rem',
                    fontSize: '1.1rem',
                    fontWeight: '600',
                    textDecoration: 'none',
                    borderRadius: '0.5rem',
                    transition: 'all 0.2s ease'
                  }}>
                  🚀 Start with Hello World
                </Link>

                <Link
                  className="button button--outline button--lg"
                  to="/blog"
                  style={{
                    padding: '0.75rem 1.5rem',
                    fontSize: '1.1rem',
                    fontWeight: '600',
                    textDecoration: 'none',
                    borderRadius: '0.5rem',
                    transition: 'all 0.2s ease'
                  }}>
                  📖 Read the Blog
                </Link>

                {showEasterEgg && (
                  <button
                    className="button button--success button--lg"
                    onClick={resetRobot}
                    style={{
                      padding: '0.75rem 1.5rem',
                      fontSize: '1.1rem',
                      fontWeight: '600',
                      borderRadius: '0.5rem',
                      transition: 'all 0.2s ease',
                      animation: 'pulse 1s ease-in-out infinite'
                    }}>
                    🔄 Reset Robot
                  </button>
                )}
              </div>

              {/* Search Suggestion */}
              <div style={{
                background: 'rgba(255, 255, 255, 0.9)',
                padding: '1rem',
                borderRadius: '0.5rem',
                border: '1px solid var(--ifm-color-primary-light)'
              }}>
                <p style={{
                  margin: '0',
                  fontSize: '1rem',
                  color: 'var(--ifm-color-emphasis-600)'
                }}>
                  <strong>💡 Pro Tip:</strong> Try searching for what you're looking for using the search bar above,
                  or check out our <Link to="/docs/overview" style={{color: 'var(--ifm-color-primary)'}}>comprehensive tutorial index</Link>.
                </p>
              </div>
            </div>

            {/* Footer Message */}
            <div style={{
              textAlign: 'center',
              padding: '1rem',
              background: 'var(--ifm-color-emphasis-100)',
              borderRadius: '0.5rem',
              border: '1px solid var(--ifm-color-emphasis-200)'
            }}>
              <p style={{
                margin: '0',
                fontSize: '0.9rem',
                color: 'var(--ifm-color-emphasis-700)'
              }}>
                If you believe this page should exist, please
                <a href="https://github.com/raphaelmansuy/adk_training/issues" target="_blank" rel="noopener noreferrer" style={{
                  color: 'var(--ifm-color-primary)',
                  textDecoration: 'underline',
                  marginLeft: '0.25rem'
                }}>
                  report it as an issue
                </a>.
                Meanwhile, enjoy exploring the world of AI agents! 🤖✨
              </p>
            </div>
          </div>
        </div>
      </main>

      <style>{`
        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-10px);
          }
          60% {
            transform: translateY(-5px);
          }
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(0px) rotate(0deg);
            opacity: 0.3;
          }
          50% {
            transform: translateY(-20px) rotate(180deg);
            opacity: 0.7;
          }
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes dance {
          0%, 100% { transform: rotate(0deg) scale(1); }
          25% { transform: rotate(-5deg) scale(1.05); }
          50% { transform: rotate(5deg) scale(1.1); }
          75% { transform: rotate(-3deg) scale(1.05); }
        }

        @keyframes pulse {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }

        .button:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        @media (max-width: 768px) {
          .col {
            padding: 0 1rem;
          }

          .hero__title {
            font-size: 2rem !important;
          }
        }
      `}</style>
    </Layout>
  );
}