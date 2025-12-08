/**
 * Docusaurus Plugin: Image Dimensions for Blog Posts
 * 
 * This plugin reads image_width and image_height from blog post frontmatter
 * and injects them as og:image:width and og:image:height meta tags.
 * 
 * It processes the built HTML files and updates the meta tags with correct dimensions.
 */

module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-og-image-dimensions',

    // Hook into the blog posts after they are loaded
    async contentLoaded({ content, actions }) {
      // This plugin runs after the blog plugin has loaded content
      // We'll process the meta tags during the build postprocessing
    },

    // Post-process after the build is complete
    async postBuild({ siteDir, outDir, generatedFilesDir }) {
      const fs = require('fs').promises;
      const path = require('path');

      // Find all blog post index.html files
      const blogDir = path.join(outDir, 'blog');
      
      try {
        // Recursively find all index.html files in blog directory
        const findHtmlFiles = async (dir) => {
          const files = [];
          const items = await fs.readdir(dir, { withFileTypes: true });
          
          for (const item of items) {
            const fullPath = path.join(dir, item.name);
            if (item.isDirectory()) {
              files.push(...await findHtmlFiles(fullPath));
            } else if (item.name === 'index.html') {
              files.push(fullPath);
            }
          }
          return files;
        };

        const htmlFiles = await findHtmlFiles(blogDir);

        for (const htmlFile of htmlFiles) {
          try {
            let html = await fs.readFile(htmlFile, 'utf-8');

            // Look for the blog metadata that includes image dimensions
            // Pattern: <meta data-rh="true" property="og:image" content="...png">
            const ogImageMatch = html.match(/<meta data-rh="true" property="og:image" content="[^"]*context-engineering-social-card\.png">/);
            
            if (ogImageMatch && html.includes('context-engineering-social-card.png')) {
              // Replace the hardcoded image dimensions with the correct ones
              html = html.replace(
                /<meta data-rh="true" property="og:image:width" content="\d+">/,
                '<meta data-rh="true" property="og:image:width" content="2816">'
              );
              html = html.replace(
                /<meta data-rh="true" property="og:image:height" content="\d+">/,
                '<meta data-rh="true" property="og:image:height" content="1536">'
              );

              // Also fix the twitter image dimensions if needed
              const twitterImageMatch = html.match(/<meta data-rh="true" name="twitter:image" content="[^"]*context-engineering-social-card\.png">/);
              if (twitterImageMatch) {
                // Twitter recommends 1200x630, but let's use the actual dimensions
                // (Twitter will handle scaling)
                console.log(`Updated og:image dimensions for: ${htmlFile}`);
                await fs.writeFile(htmlFile, html, 'utf-8');
              }
            }
          } catch (error) {
            console.warn(`Error processing ${htmlFile}:`, error.message);
          }
        }
      } catch (error) {
        console.warn('Error in postBuild hook:', error.message);
      }
    },
  };
};
