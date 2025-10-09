import React from 'react';
import styles from './Callout.module.css';

export interface CalloutProps {
  type?: 'info' | 'warning' | 'success' | 'error' | 'note';
  title?: string;
  children: React.ReactNode;
}

export function Callout({ type = 'info', title, children }: CalloutProps) {
  const getIcon = () => {
    switch (type) {
      case 'warning':
        return '⚠️';
      case 'success':
        return '✅';
      case 'error':
        return '❌';
      case 'note':
        return '📝';
      default:
        return 'ℹ️';
    }
  };

  return (
    <div className={`${styles.callout} ${styles[type]}`}>
      <div className={styles.header}>
        <span className={styles.icon}>{getIcon()}</span>
        {title && <span className={styles.title}>{title}</span>}
      </div>
      <div className={styles.content}>
        {children}
      </div>
    </div>
  );
}