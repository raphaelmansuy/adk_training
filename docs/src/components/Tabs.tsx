import React, { useState } from 'react';
import styles from './Tabs.module.css';

export interface TabItem {
  label: string;
  content: React.ReactNode;
  id?: string;
}

export interface TabsProps {
  items: TabItem[];
  defaultActiveTab?: number;
  className?: string;
}

export function Tabs({ items, defaultActiveTab = 0, className }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultActiveTab);

  return (
    <div className={`${styles.tabs} ${className || ''}`}>
      <div className={styles.tabList} role="tablist">
        {items.map((item, index) => (
          <button
            key={item.id || index}
            className={`${styles.tabButton} ${activeTab === index ? styles.active : ''}`}
            onClick={() => setActiveTab(index)}
            role="tab"
            aria-selected={activeTab === index}
            aria-controls={`tabpanel-${item.id || index}`}
            id={`tab-${item.id || index}`}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className={styles.tabContent}>
        {items.map((item, index) => (
          <div
            key={item.id || index}
            className={`${styles.tabPanel} ${activeTab === index ? styles.active : ''}`}
            role="tabpanel"
            aria-labelledby={`tab-${item.id || index}`}
            id={`tabpanel-${item.id || index}`}
            hidden={activeTab !== index}
          >
            {item.content}
          </div>
        ))}
      </div>
    </div>
  );
}