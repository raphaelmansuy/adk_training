# Comments System Setup Guide

## Overview

The ADK Training Hub uses Giscus for community-driven discussions
on tutorial pages. Giscus enables GitHub Discussions as a comments
system, allowing users to engage with content directly through GitHub.

## Current Status

✅ **Comments Component Created**: `src/components/Comments.tsx` is ready
✅ **Package Installed**: `@giscus/react` is in `package.json`
✅ **Component Added**: Comments added to Tutorial 01 as example
✅ **Markdown Linting**: Configured to allow React components

## Setup Instructions

### 1. Get Giscus Configuration

Visit [https://giscus.app/](https://giscus.app/) and configure for your repository:

1. **Repository**: Select `raphaelmansuy/adk_training`
2. **Page ↔ Discussions Mapping**: Choose `Discussion title contains page pathname`
3. **Discussion Category**: Create/select a category (e.g., "General")
4. **Features**: Enable reactions, set theme to match site
5. **Theme**: Choose `Preferred color scheme` to match light/dark mode

### 2. Update Comments Component

Replace the placeholder values in `src/components/Comments.tsx`:

```typescript
repoId = "R_kgDOLxxxxx"; // Replace with actual repo ID from giscus.app
categoryId = "DIC_kwDOLxxxxx"; // Replace with actual category ID from giscus.app
```

### 3. Enable Discussions on GitHub

1. Go to your repository settings
2. Navigate to "General" → "Features"
3. Enable "Discussions"

### 4. Test the Comments

1. Visit any tutorial page (e.g., Tutorial 01)
2. Scroll to the bottom to see the comments section
3. Test posting a comment (requires GitHub login)

## Adding Comments to More Pages

To add comments to other tutorial pages:

1. Add the import at the top of the MDX file:

   ```markdown
   ---
   frontmatter...
   ---

   import Comments from '@site/src/components/Comments';
   ```

2. Add the component at the end of the content:

   ```markdown
   ## Conclusion

   [Content...]

   ---

   <Comments />
   ```

## Features Included

- **GitHub Integration**: Comments are GitHub Discussions
- **Theme Support**: Automatically matches light/dark mode
- **Reactions**: Users can react to comments
- **Threaded Discussions**: Full discussion capabilities
- **No External Dependencies**: Uses GitHub's native discussion system

## Community & Social Links

The site also includes:

- **Newsletter Signup**: `https://newsletter.adk-training.com`
- **Calendly Calls**: `https://calendly.com/raphaelmansuy`
- **Twitter/X**: `https://twitter.com/raphaelmansuy`

## Troubleshooting

- **Comments not loading**: Check repo ID and category ID are correct
- **GitHub Discussions disabled**: Enable in repository settings
- **Theme issues**: Ensure theme is set to "Preferred color scheme"
- **Build errors**: Verify package is installed and component is properly imported

## Next Steps

1. Complete Giscus configuration with actual IDs
2. Add comments to all tutorial pages
3. Test comment functionality
4. Monitor community engagement
