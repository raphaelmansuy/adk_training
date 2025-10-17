#!/usr/bin/env node

/**
 * Post-build script to format sitemap.xml with proper indentation
 * This ensures Google Search Console can read the sitemap correctly
 */

const fs = require('fs');
const path = require('path');
const { parseString, Builder } = require('xml2js');

const buildDir = path.join(__dirname, '..', 'build');
const sitemapPath = path.join(buildDir, 'sitemap.xml');

try {
  // Check if sitemap.xml exists
  if (!fs.existsSync(sitemapPath)) {
    console.log('sitemap.xml not found, skipping formatting');
    process.exit(0);
  }

  // Read the minified sitemap
  const minifiedXml = fs.readFileSync(sitemapPath, 'utf8');

  // Parse the XML
  parseString(minifiedXml, (err, result) => {
    if (err) {
      throw new Error(`Failed to parse XML: ${err.message}`);
    }

    // Create a new builder with pretty formatting
    const builder = new Builder({
      renderOpts: {
        pretty: true,
        indent: '  ', // 2 spaces
        newline: '\n'
      },
      xmldec: {
        version: '1.0',
        encoding: 'UTF-8'
      }
    });

    // Build the formatted XML
    const formattedXml = builder.buildObject(result);

    // Write the formatted sitemap back
    fs.writeFileSync(sitemapPath, formattedXml, 'utf8');

    console.log('✅ sitemap.xml has been formatted with proper indentation');
  });

} catch (error) {
  console.error('❌ Error formatting sitemap.xml:', error.message);
  process.exit(1);
}