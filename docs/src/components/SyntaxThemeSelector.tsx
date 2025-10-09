import React, { useState, useEffect } from 'react';
import styles from './SyntaxThemeSelector.module.css';

interface ThemeOption {
  id: string;
  name: string;
  description: string;
  preview: {
    background: string;
    text: string;
    keyword: string;
    string: string;
    punctuation: string;
  };
}

const THEMES: ThemeOption[] = [
  {
    id: 'adk-light',
    name: 'ADK Light',
    description: 'Clean and professional theme',
    preview: {
      background: '#f8f9fa',
      text: '#2d3748',
      keyword: '#3182ce',
      string: '#38a169',
      punctuation: '#4a5568',
    },
  },
  {
    id: 'adk-dark',
    name: 'ADK Dark',
    description: 'Modern and readable theme',
    preview: {
      background: '#1a202c',
      text: '#e2e8f0',
      keyword: '#63b3ed',
      string: '#68d391',
      punctuation: '#a0aec0',
    },
  },
  {
    id: 'ai-ml',
    name: 'AI/ML Theme',
    description: 'Neural network inspired',
    preview: {
      background: '#0f1419',
      text: '#e6f3ff',
      keyword: '#00d4ff',
      string: '#00ff88',
      punctuation: '#8395a7',
    },
  },
  {
    id: 'google',
    name: 'Google Theme',
    description: 'Material Design inspired',
    preview: {
      background: '#fafafa',
      text: '#202124',
      keyword: '#1967d2',
      string: '#137333',
      punctuation: '#3c4043',
    },
  },
  {
    id: 'synthwave',
    name: 'Synthwave',
    description: 'Retro futuristic theme',
    preview: {
      background: '#2a2139',
      text: '#f8f8f2',
      keyword: '#ff79c6',
      string: '#f1fa8c',
      punctuation: '#f8f8f2',
    },
  },
];

export function SyntaxThemeSelector() {
  const [currentTheme, setCurrentTheme] = useState<string>('adk-light');
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('adk-syntax-theme');
    if (savedTheme && THEMES.find(t => t.id === savedTheme)) {
      setCurrentTheme(savedTheme);
      applyTheme(savedTheme);
    } else {
      // Apply default theme
      applyTheme('adk-light');
    }
  }, []);

  const applyTheme = (themeId: string) => {
    // Remove all existing theme classes
    document.documentElement.classList.forEach(className => {
      if (className.startsWith('prism-theme-')) {
        document.documentElement.classList.remove(className);
      }
    });

    // Add new theme class
    document.documentElement.classList.add(`prism-theme-${themeId}`);

    // Store preference
    localStorage.setItem('adk-syntax-theme', themeId);
  };

  const handleThemeChange = (themeId: string) => {
    setCurrentTheme(themeId);
    applyTheme(themeId);
    setIsOpen(false);
  };

  const currentThemeData = THEMES.find(t => t.id === currentTheme);

  return (
    <div className={styles.themeSelector}>
      <button
        className={styles.themeButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Change syntax highlighting theme"
      >
        <div className={styles.themePreview}>
          <div
            className={styles.previewColors}
            style={{
              background: `linear-gradient(45deg, ${currentThemeData?.preview.keyword}, ${currentThemeData?.preview.string})`,
            }}
          />
        </div>
        <span className={styles.themeName}>
          {currentThemeData?.name}
        </span>
        <svg
          className={`${styles.arrow} ${isOpen ? styles.arrowOpen : ''}`}
          width="12"
          height="12"
          viewBox="0 0 12 12"
          fill="none"
        >
          <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {isOpen && (
        <>
          <div
            className={styles.overlay}
            onClick={() => setIsOpen(false)}
          />
          <div className={styles.themeDropdown}>
            <div className={styles.dropdownHeader}>
              <h3>Choose Syntax Theme</h3>
              <p>Select your preferred code highlighting style</p>
            </div>

            <div className={styles.themeGrid}>
              {THEMES.map((theme) => (
                <button
                  key={theme.id}
                  className={`${styles.themeOption} ${
                    currentTheme === theme.id ? styles.active : ''
                  }`}
                  onClick={() => handleThemeChange(theme.id)}
                >
                  <div className={styles.themePreview}>
                    <div
                      className={styles.previewColors}
                      style={{
                        background: `linear-gradient(45deg, ${theme.preview.keyword}, ${theme.preview.string})`,
                      }}
                    />
                  </div>

                  <div className={styles.themeInfo}>
                    <div className={styles.themeName}>
                      {theme.name}
                      {currentTheme === theme.id && (
                        <span className={styles.activeIndicator}>✓</span>
                      )}
                    </div>
                    <div className={styles.themeDescription}>
                      {theme.description}
                    </div>
                  </div>

                  <div
                    className={styles.themeSample}
                    style={{
                      background: theme.preview.background,
                      color: theme.preview.text,
                    }}
                  >
                    <span style={{ color: theme.preview.keyword }}>function</span>{' '}
                    <span style={{ color: theme.preview.text }}>hello</span>
                    <span style={{ color: theme.preview.punctuation }}>()</span>{' '}
                    <span style={{ color: theme.preview.punctuation }}>{'{'}</span>
                    <br />
                    {'  '}<span style={{ color: theme.preview.keyword }}>return</span>{' '}
                    <span style={{ color: theme.preview.string }}>"Hello, ADK!"</span>
                    <span style={{ color: theme.preview.punctuation }}>;</span>
                    <br />
                    <span style={{ color: theme.preview.punctuation }}>{'}'}</span>
                  </div>
                </button>
              ))}
            </div>

            <div className={styles.dropdownFooter}>
              <p>Theme preference is saved automatically</p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}