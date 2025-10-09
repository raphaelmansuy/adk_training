import React from 'react';
import { useLocation } from '@docusaurus/router';
import { useTitleFormatter } from '@docusaurus/theme-common';

interface SocialShareProps {
  title?: string;
  description?: string;
}

export default function SocialShare({ title, description }: SocialShareProps): JSX.Element {
  const location = useLocation();
  const currentUrl = typeof window !== 'undefined' ? window.location.origin + location.pathname : '';
  const pageTitle = title || document?.title || 'ADK Training Hub';
  const pageDescription = description || 'Master Google Agent Development Kit from First Principles';

  const shareUrls = {
    twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(pageTitle)}&url=${encodeURIComponent(currentUrl)}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(currentUrl)}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(currentUrl)}`,
    reddit: `https://reddit.com/submit?url=${encodeURIComponent(currentUrl)}&title=${encodeURIComponent(pageTitle)}`,
    email: `mailto:?subject=${encodeURIComponent(pageTitle)}&body=${encodeURIComponent(`${pageDescription}\n\n${currentUrl}`)}`,
  };

  const handleShare = (platform: keyof typeof shareUrls) => {
    window.open(shareUrls[platform], '_blank', 'noopener,noreferrer');
  };

  return (
    <div style={{
      display: 'flex',
      gap: '0.5rem',
      alignItems: 'center',
      margin: '1rem 0',
      flexWrap: 'wrap'
    }}>
      <span style={{ fontSize: '0.9rem', color: 'var(--ifm-color-emphasis-700)' }}>
        Share this page:
      </span>
      <button
        onClick={() => handleShare('twitter')}
        style={{
          padding: '0.25rem 0.5rem',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: '4px',
          background: 'transparent',
          color: 'var(--ifm-color-emphasis-700)',
          cursor: 'pointer',
          fontSize: '0.8rem',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = '#1da1f2';
          e.currentTarget.style.color = 'white';
          e.currentTarget.style.borderColor = '#1da1f2';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.color = 'var(--ifm-color-emphasis-700)';
          e.currentTarget.style.borderColor = 'var(--ifm-color-emphasis-300)';
        }}
      >
        Twitter
      </button>
      <button
        onClick={() => handleShare('linkedin')}
        style={{
          padding: '0.25rem 0.5rem',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: '4px',
          background: 'transparent',
          color: 'var(--ifm-color-emphasis-700)',
          cursor: 'pointer',
          fontSize: '0.8rem',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = '#0077b5';
          e.currentTarget.style.color = 'white';
          e.currentTarget.style.borderColor = '#0077b5';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.color = 'var(--ifm-color-emphasis-700)';
          e.currentTarget.style.borderColor = 'var(--ifm-color-emphasis-300)';
        }}
      >
        LinkedIn
      </button>
      <button
        onClick={() => handleShare('facebook')}
        style={{
          padding: '0.25rem 0.5rem',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: '4px',
          background: 'transparent',
          color: 'var(--ifm-color-emphasis-700)',
          cursor: 'pointer',
          fontSize: '0.8rem',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = '#1877f2';
          e.currentTarget.style.color = 'white';
          e.currentTarget.style.borderColor = '#1877f2';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.color = 'var(--ifm-color-emphasis-700)';
          e.currentTarget.style.borderColor = 'var(--ifm-color-emphasis-300)';
        }}
      >
        Facebook
      </button>
      <button
        onClick={() => handleShare('reddit')}
        style={{
          padding: '0.25rem 0.5rem',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: '4px',
          background: 'transparent',
          color: 'var(--ifm-color-emphasis-700)',
          cursor: 'pointer',
          fontSize: '0.8rem',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = '#ff4500';
          e.currentTarget.style.color = 'white';
          e.currentTarget.style.borderColor = '#ff4500';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.color = 'var(--ifm-color-emphasis-700)';
          e.currentTarget.style.borderColor = 'var(--ifm-color-emphasis-300)';
        }}
      >
        Reddit
      </button>
      <button
        onClick={() => handleShare('email')}
        style={{
          padding: '0.25rem 0.5rem',
          border: '1px solid var(--ifm-color-emphasis-300)',
          borderRadius: '4px',
          background: 'transparent',
          color: 'var(--ifm-color-emphasis-700)',
          cursor: 'pointer',
          fontSize: '0.8rem',
          transition: 'all 0.2s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.background = 'var(--ifm-color-emphasis-300)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'transparent';
        }}
      >
        Email
      </button>
    </div>
  );
}