---
id: seo_quick_setup
title: "Quick Setup Guide - GA4 & Search Console"
description: "Step-by-step guide to configure Google Analytics 4 and Search Console for the Google ADK Training Hub. Get tracking and indexing working in 30 minutes."
sidebar_label: "⚡ Quick Setup Guide"
sidebar_position: 8
tags: ["seo", "setup", "ga4", "search-console", "quick-start"]
---

import Comments from '@site/src/components/Comments';

# Quick Setup Guide - GA4 & Search Console

**Get your site properly tracked and indexed in 30 minutes**

This guide walks you through the two most critical SEO setup tasks for the Google ADK Training Hub.

---

## Prerequisites

- GitHub account with push access to the repository
- Google account (for GA4 and Search Console)
- 30 minutes of focused time

---

## Part 1: Google Analytics 4 Setup (10 minutes)

### Step 1: Create GA4 Property

1. **Go to Google Analytics**
   - Visit: https://analytics.google.com
   - Sign in with your Google account

2. **Create New Property**
   - Click **Admin** (gear icon in bottom left)
   - Under "Account" column, select or create an account
   - Under "Property" column, click **+ Create Property**

3. **Configure Property**
   ```
   Property name: Google ADK Training Hub
   Reporting time zone: (Select your timezone)
   Currency: (Select your currency)
   ```
   - Click **Next**

4. **Business Details**
   ```
   Industry: Education / Technology
   Business size: Small (optional)
   ```
   - Click **Next**

5. **Business Objectives**
   - Select: "Examine user behavior"
   - Click **Create**

6. **Accept Terms of Service**
   - Check the boxes
   - Click **I Accept**

### Step 2: Create Data Stream

1. **Platform Selection**
   - Click **Web** (for website tracking)

2. **Set Up Web Stream**
   ```
   Website URL: https://raphaelmansuy.github.io
   Stream name: adk_training
   ```
   - Click **Create stream**

3. **Copy Your Measurement ID**
   - You'll see a screen with your Measurement ID
   - Format: `G-XXXXXXXXXX` (where X are letters/numbers)
   - **Copy this ID** - you'll need it in the next step

### Step 3: Update Configuration File

1. **Open the Repository**
   - Navigate to: `docs/docusaurus.config.ts`

2. **Find the GA4 Configuration**
   - Search for: `trackingID: 'GA_MEASUREMENT_ID'`
   - Should be around line 348

3. **Replace with Your Measurement ID**
   
   **BEFORE:**
   ```typescript
   trackingID: 'GA_MEASUREMENT_ID', // ⚠️ PLACEHOLDER - NOT TRACKING
   ```
   
   **AFTER:**
   ```typescript
   trackingID: 'G-ABC123DEF4', // ✅ Your actual GA4 Measurement ID
   ```
   
   ⚠️ **Important**: Replace `G-ABC123DEF4` with your actual Measurement ID!

4. **Save and Commit**
   ```bash
   git add docs/docusaurus.config.ts
   git commit -m "Configure Google Analytics 4 tracking"
   git push
   ```

5. **Deploy to GitHub Pages**
   - GitHub Actions will automatically rebuild and deploy your site
   - Wait 5-10 minutes for deployment to complete

### Step 4: Verify Tracking Works

1. **Wait 24 Hours** (recommended)
   - Analytics data takes time to process
   - Real-time data may appear within 30 minutes

2. **Check Real-Time Report**
   - Go back to Google Analytics
   - Click **Reports** → **Real-time**
   - Open your site in another tab: https://raphaelmansuy.github.io/adk_training/
   - You should see yourself in the real-time report!

---

## Part 2: Google Search Console Setup (15 minutes)

### Step 1: Add Property

1. **Go to Search Console**
   - Visit: https://search.google.com/search-console
   - Sign in with your Google account

2. **Add New Property**
   - Click **Add property** (top left)
   - Select **URL prefix** (not Domain)

3. **Enter Your URL**
   ```
   URL: https://raphaelmansuy.github.io/adk_training/
   ```
   - Click **Continue**

### Step 2: Verify Ownership (HTML Tag Method)

1. **Choose Verification Method**
   - Select **HTML tag** from the list of methods
   - You'll see code like:
   ```html
   <meta name="google-site-verification" content="ABC123xyz..." />
   ```

2. **Copy the Verification Code**
   - Copy ONLY the content value
   - Example: If you see `content="ABC123xyz..."`, copy `ABC123xyz...`
   - **Keep this tab open!**

3. **Update Configuration File**
   - Open: `docs/docusaurus.config.ts`
   - Search for: `google-site-verification`
   - Should be around line 408

4. **Replace with Your Code**
   
   **BEFORE:**
   ```typescript
   { name: 'google-site-verification', content: 'tuQTXHERxeAB5YzYV7ZHPEFqwMYBCEBVmsYy_m-nJEU' }, // ⚠️ PLACEHOLDER
   ```
   
   **AFTER:**
   ```typescript
   { name: 'google-site-verification', content: 'ABC123xyz...' }, // ✅ Your actual verification code
   ```
   
   ⚠️ **Important**: Replace `ABC123xyz...` with your actual code!

5. **Save, Commit and Deploy**
   ```bash
   git add docs/docusaurus.config.ts
   git commit -m "Add Google Search Console verification"
   git push
   ```

6. **Wait for Deployment**
   - Wait 5-10 minutes for GitHub Actions to rebuild and deploy

### Step 3: Complete Verification

1. **Go Back to Search Console Tab**
   - The tab where you copied the verification code

2. **Click VERIFY**
   - Google will check your site for the verification code
   - If successful: You'll see "Ownership verified" ✅
   - If failed: Wait another 5 minutes and try again

### Step 4: Submit Sitemap

1. **Go to Sitemaps Section**
   - In Search Console, click **Sitemaps** in the left sidebar

2. **Add New Sitemap**
   - In the "Add a new sitemap" field, enter:
   ```
   sitemap.xml
   ```
   - Click **Submit**

3. **Verify Submission**
   - Status should change from "Pending" to "Success" within hours
   - Google will begin crawling your pages

---

## Verification Checklist

After completing both setups, verify everything works:

### ✅ Google Analytics 4
- [ ] Measurement ID replaced in `docusaurus.config.ts`
- [ ] Changes committed and pushed to GitHub
- [ ] Site redeployed (check GitHub Actions)
- [ ] Real-time tracking works (you can see yourself visiting the site)

### ✅ Google Search Console
- [ ] Verification code replaced in `docusaurus.config.ts`
- [ ] Changes committed and pushed to GitHub
- [ ] Site redeployed (check GitHub Actions)
- [ ] Ownership verified in Search Console
- [ ] Sitemap submitted successfully

---

## Troubleshooting

### GA4 Not Tracking

**Problem**: Real-time report shows no data

**Solutions**:
1. Wait 24 hours - data processing takes time
2. Check Measurement ID is correct (starts with `G-`)
3. Verify site is deployed (check GitHub Actions)
4. Disable ad blockers and visit your site
5. Open browser console (F12) and check for errors

### Search Console Verification Failed

**Problem**: Verification button shows error

**Solutions**:
1. Wait 10 minutes after deployment
2. Check verification code is correct (no extra spaces)
3. Visit your site and view page source (Ctrl+U/Cmd+U)
4. Search for "google-site-verification" in source
5. Verify the meta tag appears in the HTML

### Sitemap Not Found

**Problem**: Sitemap submission shows 404 error

**Solutions**:
1. Visit: https://raphaelmansuy.github.io/adk_training/sitemap.xml
2. Verify it loads (should show XML)
3. If 404: Wait for next deployment
4. Check GitHub Actions for build errors

---

## What Happens Next?

After setup is complete:

### Week 1
- ✅ Google starts crawling your pages
- ✅ Analytics begins collecting visitor data
- ✅ Sitemap processing begins

### Week 2-4
- ✅ Pages begin appearing in Google search results
- ✅ You can see search performance data
- ✅ Indexing status visible in Search Console

### Month 2+
- ✅ Pages rank for branded keywords
- ✅ Organic traffic increases
- ✅ Full analytics and search data available

---

## Need Help?

- **GA4 Help**: https://support.google.com/analytics
- **Search Console Help**: https://support.google.com/webmasters
- **Implementation Guide**: [Full SEO Implementation Guide](./implementation_guide)
- **GitHub Issues**: https://github.com/raphaelmansuy/adk_training/issues

---

## Next Steps

After completing this setup:

1. **Review**: [Phase-Based Roadmap](./phase_based_roadmap) for next priorities
2. **Monitor**: [Monitoring Dashboard](./monitoring_dashboard) to track progress
3. **Report**: [Progress Tracking](./progress_tracking) for monthly updates

🎉 **Congratulations!** Your site is now properly tracked and will start appearing in Google search results within weeks.

<Comments />
