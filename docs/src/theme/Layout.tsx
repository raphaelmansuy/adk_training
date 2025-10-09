import React from 'react';
import Layout from '@theme-original/Layout';
import { SyntaxThemeSelector } from '../components/SyntaxThemeSelector';

export default function CustomLayout(props) {
  return (
    <Layout {...props}>
      <div style={{
        position: 'fixed',
        top: '50%',
        right: '20px',
        transform: 'translateY(-50%)',
        zIndex: 1000
      }}>
        <SyntaxThemeSelector />
      </div>
      {props.children}
    </Layout>
  );
}