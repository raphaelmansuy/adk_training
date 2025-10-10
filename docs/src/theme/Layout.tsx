import React from 'react';
import Layout from '@theme-original/Layout';
// import { SyntaxThemeSelector } from '../components/SyntaxThemeSelector';

export default function CustomLayout(props) {
  return (
    <Layout {...props}>
      {/* Theme selector disabled/hidden */}
      {/* <div style={{
        position: 'fixed',
        top: '16px',
        left: '20px',
        zIndex: 1000
      }}>
        <SyntaxThemeSelector />
      </div> */}
      {props.children}
    </Layout>
  );
}