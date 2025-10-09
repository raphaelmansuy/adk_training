# 🌟 Community & Social Features

This document explains how to use the community and social features added to the ADK Training Hub.

## Features Added

### 1. Enhanced Footer Links

- **Twitter/X**: Follow for updates and announcements
- **Newsletter**: Stay updated with latest tutorials and features
- **Calendly**: Schedule 1-on-1 calls with the author

### 2. Navbar Social Links

- Quick access to Twitter from the navigation bar

### 3. Comments System (Giscus)

GitHub Discussions-based comments for community engagement.

#### Setup Instructions

1. Go to [https://giscus.app/](https://giscus.app/)
2. Select your repository: `raphaelmansuy/adk_training`
3. Choose discussion category (create one if needed)
4. Copy the `repoId` and `categoryId` values
5. Replace the placeholder values in `src/components/Comments.tsx`

#### Usage in MDX Files (Comments)

```mdx
import Comments from '@site/src/components/Comments';

# My Tutorial

Tutorial content here...

<Comments />
```

### 4. Social Sharing Component

Share buttons for Twitter, LinkedIn, Facebook, Reddit, and Email.

#### Usage in MDX Files (Sharing)

```mdx
import SocialShare from '@site/src/components/SocialShare';

# My Tutorial

Tutorial content here...

<SocialShare
  title="Custom Title"
  description="Custom description for sharing"
/>
```

### 5. Enhanced Metadata

- LinkedIn Open Graph tags for better social media sharing
- Additional social profiles in structured data

## Configuration

### Social Media URLs

Update these URLs in `docusaurus.config.ts`:

- Twitter: `https://twitter.com/raphaelmansuy`
- Newsletter: `https://newsletter.adk-training.com`
- Calendly: `https://calendly.com/raphaelmansuy`

### Giscus Configuration

Replace placeholder values in `src/components/Comments.tsx`:

```typescript
repoId="R_kgDOLxxxxx" // Your actual repo ID
categoryId="DIC_kwDOLxxxxx" // Your actual category ID
```

## Next Steps

1. Create social media accounts and update URLs
2. Configure Giscus with your actual repo and category IDs
3. Set up a newsletter service (e.g., Mailchimp, ConvertKit)
4. Add the Comments and SocialShare components to your tutorial pages
5. Test social sharing functionality
6. Monitor community engagement and iterate

## Community Engagement Tips

- **Respond promptly** to comments and questions
- **Share updates** regularly on social media
- **Encourage contributions** through GitHub issues and PRs
- **Host community events** like AMAs or live coding sessions

## Analytics & Metrics

Track community growth through:

- Social media followers
- Newsletter subscribers
- GitHub stars and forks
- Page views and engagement
- Comments and discussions

---

Last updated: October 9, 2025
