/**
 * Remark plugin to inject og:image:width and og:image:height meta tags
 * based on image dimensions specified in frontmatter
 * 
 * Usage in docusaurus.config.js:
 * beforeDefaultRemarkPlugins: [require('./plugins/remark-og-image-dimensions.js')]
 */

module.exports = (options = {}) => {
  return async (tree, file) => {
    const { frontmatter } = file.data;

    // Only process if image_width and image_height are specified
    if (frontmatter?.image_width && frontmatter?.image_height) {
      // Store image dimensions in file metadata for the theme to use
      if (!file.data.meta) {
        file.data.meta = {};
      }
      
      file.data.meta.imageWidth = frontmatter.image_width;
      file.data.meta.imageHeight = frontmatter.image_height;

      // Also store in frontmatter for easy access in theme components
      frontmatter.og_image_width = frontmatter.image_width;
      frontmatter.og_image_height = frontmatter.image_height;
    }
  };
};
