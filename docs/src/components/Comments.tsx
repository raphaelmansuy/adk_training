import React from 'react';
import Giscus from '@giscus/react';
import { useColorMode } from '@docusaurus/theme-common';

export default function Comments(): JSX.Element {
  const { colorMode } = useColorMode();

  return (
    <div style={{ marginTop: '3rem', marginBottom: '2rem' }}>
      <h3 style={{ marginBottom: '1rem', fontSize: '1.25rem', fontWeight: '600' }}>
        💬 Join the Discussion
      </h3>
      <p style={{ marginBottom: '1.5rem', color: 'var(--ifm-color-emphasis-700)', fontSize: '0.9rem' }}>
        Have questions or feedback? Discuss this tutorial with the community on GitHub Discussions.
      </p>
      <Giscus
        repo="raphaelmansuy/adk_training"
        repoId="R_UmVwb3NpdG9yeToxMDcyMTgzMjY4"
        category="General"
        categoryId="DIC_kwDOGh4L_oAN_V_v"
        mapping="pathname"
        strict="0"
        reactionsEnabled="1"
        emitMetadata="0"
        inputPosition="top"
        theme={colorMode}
        lang="en"
        loading="lazy"
      />
    </div>
  );
}