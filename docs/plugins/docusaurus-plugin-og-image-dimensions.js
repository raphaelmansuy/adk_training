/**
 * Docusaurus Plugin: Image Dimensions for Blog Posts
 * 
 * This plugin reads image_width and image_height from blog post frontmatter
 * and injects them as og:image:width and og:image:height meta tags.
 * 
 * It processes the built HTML files and updates the meta tags with correct dimensions.
 * 
 * Enhanced for LinkedIn compatibility with proper meta tag ordering.
 */

module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-og-image-dimensions',

    // Post-process after the build is complete
    async postBuild({ siteDir, outDir, generatedFilesDir }) {
      const fs = require('fs').promises;
      const path = require('path');
      const matter = require('gray-matter');

      // Find all blog post markdown files to extract frontmatter
      const blogSourceDir = path.join(siteDir, 'blog');
      const blogDir = path.join(outDir, 'blog');
      
      try {
        // Read all markdown files from blog directory
        const markdownFiles = await fs.readdir(blogSourceDir);
        const blogPostDimensions = new Map();

        // Extract image dimensions from frontmatter
        for (const file of markdownFiles) {
          if (file.endsWith('.md') || file.endsWith('.mdx')) {
            try {
              const mdPath = path.join(blogSourceDir, file);
              const mdContent = await fs.readFile(mdPath, 'utf-8');
              const { data: frontmatter } = matter(mdContent);

              if (frontmatter.image && frontmatter.image_width && frontmatter.image_height) {
                // Extract image filename for matching
                const imageName = frontmatter.image.split('/').pop();
                blogPostDimensions.set(imageName, {
                  width: frontmatter.image_width,
                  height: frontmatter.image_height,
                  imageUrl: frontmatter.image
                });
              }
            } catch (err) {
              // Skip files that can't be parsed
            }
          }
        }

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
            let modified = false;

            // Check each blog post dimension mapping
            for (const [imageName, dimensions] of blogPostDimensions) {
              if (html.includes(imageName)) {
                // Update og:image:width
                const widthRegex = /<meta data-rh="true" property="og:image:width" content="\d+">/;
                if (widthRegex.test(html)) {
                  html = html.replace(
                    widthRegex,
                    `<meta data-rh="true" property="og:image:width" content="${dimensions.width}">`
                  );
                  modified = true;
                }

                // Update og:image:height
                const heightRegex = /<meta data-rh="true" property="og:image:height" content="\d+">/;
                if (heightRegex.test(html)) {
                  html = html.replace(
                    heightRegex,
                    `<meta data-rh="true" property="og:image:height" content="${dimensions.height}">`
                  );
                  modified = true;
                }

                // CRITICAL: Add LinkedIn-specific meta tags if not present
                // LinkedIn sometimes prefers these alternate formats
                const ogImageRegex = /<meta data-rh="true" property="og:image" content="([^"]+)">/;
                const ogImageMatch = html.match(ogImageRegex);
                
                if (ogImageMatch && !html.includes('property="og:image:secure_url"')) {
                  const ogImageUrl = ogImageMatch[1];
                  // Add secure_url tag right after og:image for LinkedIn
                  html = html.replace(
                    ogImageMatch[0],
                    `${ogImageMatch[0]}<meta data-rh="true" property="og:image:secure_url" content="${ogImageUrl}">`
                  );
                  modified = true;
                }

                // Add image type for better LinkedIn compatibility
                if (!html.includes('property="og:image:type"')) {
                  const imageTypeTag = '<meta data-rh="true" property="og:image:type" content="image/png">';
                  html = html.replace(
                    /<meta data-rh="true" property="og:image:height" content="\d+">/,
                    `$&${imageTypeTag}`
                  );
                  modified = true;
                }

                if (modified) {
                  console.log(`✅ Updated og:image dimensions for: ${htmlFile}`);
                  console.log(`   Image: ${imageName} (${dimensions.width}x${dimensions.height})`);
                }
                break;
              }
            }

            if (modified) {
              await fs.writeFile(htmlFile, html, 'utf-8');
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
