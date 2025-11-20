---
id: seo_monitoring_dashboard
title: "SEO Monitoring Dashboard"
description: "Setup and tracking templates for Google Search Console, Analytics, PageSpeed Insights, and monthly reporting."
sidebar_label: "Monitoring Dashboard"
sidebar_position: 6
tags: ["seo", "monitoring", "analytics", "tracking"]
---

import Comments from '@site/src/components/Comments';

# SEO Monitoring Dashboard - Setup & Tracking Templates

**This document provides templates and setup instructions for ongoing SEO monitoring**

---

## Part 1: Google Search Console Dashboard

### Access & Setup

1. **Sign Up/Login**
   - URL: https://search.google.com/search-console
   - Select property: `https://raphaelmansuy.github.io/adk_training/`

2. **Key Reports to Monitor**

### 2.1 Performance Report

**Purpose:** Track keyword rankings and CTR  
**Update Frequency:** Daily (review weekly)

**Key Metrics:**
- Total Clicks: Organic traffic clicks from Google
- Total Impressions: Times your site appears in search results
- Average CTR: Click-through rate (target: 3-5%)
- Average Position: Where you rank (target: <5)

**Tracking Template:**

```
Week of: [DATE]

Performance Overview:
├─ Clicks: [X] (last week: [X], +/-[X]%)
├─ Impressions: [X] (last week: [X], +/-[X]%)
├─ CTR: [X]% (target: 3-5%)
└─ Avg Position: [X] (target: <5)

Top 5 Keywords:
├─ "google adk tutorial" [Clicks: X, Position: X]
├─ "agent development kit python" [Clicks: X, Position: X]
├─ "build ai agents" [Clicks: X, Position: X]
├─ [Keyword] [Clicks: X, Position: X]
└─ [Keyword] [Clicks: X, Position: X]

Observations:
- [Insight 1]
- [Insight 2]
- [Insight 3]

Actions Taken:
- [ ] Optimize content for low-CTR keywords
- [ ] Improve SERP snippets
- [ ] Add internal links to underperforming pages
```

### 2.2 Coverage Report

**Purpose:** Monitor indexing status  
**Update Frequency:** Weekly

**Key Metrics:**
- Valid: Pages successfully indexed
- Errors: Pages with crawl/indexing errors
- Warnings: Pages with issues but indexed
- Excluded: Pages intentionally excluded

**Healthy State:**
```
Valid: 95%+ of total pages
Errors: 0 critical errors
Warnings: < 5% of pages
Excluded: Tag-related, search pages (expected)
```

**Tracking Template:**

```
Week of: [DATE]

Coverage Status:
├─ Valid: [X] pages (90% is baseline, 95%+ is good)
├─ Errors: [X] (track: crawl errors, submit errors)
├─ Warnings: [X] (track: blocked resources, noindex)
└─ Excluded: [X] (track: parameter exclusions)

Error Types Found:
├─ [Error Type]: [Count] → Actions: [What will be done]
├─ [Error Type]: [Count] → Actions: [What will be done]
└─ [Error Type]: [Count] → Actions: [What will be done]

Indexing Trends:
- Indexed pages trend: [↑ increasing / ↓ decreasing / → stable]
- New pages indexed: [X] this week
- Pages removed: [X] this week
- Avg indexing lag: [X days]

Actions:
- [ ] Investigate and fix any errors
- [ ] Resubmit error pages
- [ ] Monitor excluded pages
```

### 2.3 Core Web Vitals Report

**Purpose:** Monitor page experience signals  
**Update Frequency:** Weekly

**Metrics:**
- Largest Contentful Paint (LCP): < 2.5s (Good)
- First Input Delay (FID) / INP: < 100ms (Good)
- Cumulative Layout Shift (CLS): < 0.1 (Good)

**Tracking Template:**

```
Week of: [DATE]

Core Web Vitals Status:
├─ LCP: [GOOD/NEEDS IMPROVEMENT] - [X]ms
├─ FID/INP: [GOOD/NEEDS IMPROVEMENT] - [X]ms
└─ CLS: [GOOD/NEEDS IMPROVEMENT] - [X]

Device Breakdown:
Mobile:
├─ LCP: [Status] - [X]ms
├─ FID/INP: [Status] - [X]ms
└─ CLS: [Status] - [X]

Desktop:
├─ LCP: [Status] - [X]ms
├─ FID/INP: [Status] - [X]ms
└─ CLS: [Status] - [X]

Pages Needing Improvement:
├─ [Page URL] - Issues: [LCP / FID / CLS]
├─ [Page URL] - Issues: [LCP / FID / CLS]
└─ [Page URL] - Issues: [LCP / FID / CLS]

Actions:
- [ ] Optimize images (for LCP)
- [ ] Reduce JavaScript (for INP)
- [ ] Fix layout shifts (for CLS)
- [ ] Retest after optimization
```

---

## Part 2: Google Analytics Dashboard

### Access & Setup

1. **Sign Up/Login**
   - URL: https://analytics.google.com
   - Select property: Google ADK Training Hub

2. **Key Reports to Monitor**

### 2.1 Organic Traffic Overview

**Purpose:** Track organic visitor growth  
**Update Frequency:** Daily (review weekly)

**Key Metrics:**
- Users: Unique visitors from organic search
- Sessions: Visits from organic search
- Pageviews: Total pages viewed
- Bounce Rate: % of sessions with 1 page
- Session Duration: Average time spent

**Tracking Template:**

```
Week of: [DATE]

Organic Traffic Overview:
├─ Users: [X] (+X% vs last week)
├─ Sessions: [X] (+X% vs last week)
├─ Pageviews: [X] (+X% vs last week)
├─ Avg Session Duration: [X]min (+X% vs last week)
├─ Bounce Rate: [X]% (target: < 40%)
└─ Pages/Session: [X] (target: 3+)

Top Landing Pages:
├─ [Page] - [Sessions], [Bounce Rate]
├─ [Page] - [Sessions], [Bounce Rate]
├─ [Page] - [Sessions], [Bounce Rate]
└─ [Page] - [Sessions], [Bounce Rate]

Traffic Trends:
- 7-day trend: [↑ increasing / ↓ decreasing / → stable]
- YoY change: [+X% / -X%]
- Monthly projection: [X sessions]

Actions:
- [ ] Analyze top landing pages
- [ ] Improve pages with high bounce rate
- [ ] Optimize for conversion
- [ ] Test new content
```

### 2.2 Organic Keyword Performance

**Purpose:** Understand which keywords drive traffic  
**Update Frequency:** Weekly

**Tracking Template:**

```
Week of: [DATE]

Top Keywords Driving Traffic:
├─ [Keyword]: [Sessions], [Conversion Rate]
├─ [Keyword]: [Sessions], [Conversion Rate]
├─ [Keyword]: [Sessions], [Conversion Rate]
├─ [Keyword]: [Sessions], [Conversion Rate]
└─ [Keyword]: [Sessions], [Conversion Rate]

Keyword Trends:
- New keywords: [X] (typically 3-7 new each week)
- Growing keywords: [X] (+X% growth)
- Declining keywords: [X] (-X% decline)
- Zero-traffic keywords: [X]

Actions:
- [ ] Create content for trending keywords
- [ ] Optimize pages for growing keywords
- [ ] Investigate declining keywords
- [ ] Remove low-value keywords from targeting
```

### 2.3 Conversion & Goals

**Purpose:** Track business-related actions  
**Update Frequency:** Weekly

**Tracking Template:**

```
Week of: [DATE]

Conversion Tracking:
├─ Newsletter Signups: [X] (target: 2-3% of users)
├─ Download/Clicks: [X]
├─ GitHub Star: [X]
├─ External Links: [X]
└─ Time on Page: [X]min average

Conversion Rate by Channel:
- Organic: [X]%
- Direct: [X]%
- Referral: [X]%

Top Converting Pages:
├─ [Page] - [Conversions], [Rate]
├─ [Page] - [Conversions], [Rate]
└─ [Page] - [Conversions], [Rate]

Actions:
- [ ] Optimize high-converting pages further
- [ ] Test new call-to-action elements
- [ ] Improve conversion funnel
- [ ] Analyze user behavior paths
```

---

## Part 3: PageSpeed Insights Monitoring

### Monthly Speed Check

**Purpose:** Monitor Core Web Vitals and page performance  
**URL:** https://pagespeed.web.dev/  
**Update Frequency:** Monthly (or after major changes)

**Tracking Template:**

```
Month: [MONTH/YEAR]

Homepage Performance (Mobile):
├─ Performance Score: [X]/100 (target: 75+)
├─ LCP: [X]ms (target: <2500ms)
├─ FID/INP: [X]ms (target: <100ms)
├─ CLS: [X] (target: <0.1)
└─ TTFB: [X]ms

Homepage Performance (Desktop):
├─ Performance Score: [X]/100 (target: 85+)
├─ LCP: [X]ms (target: <2500ms)
├─ FID/INP: [X]ms (target: <100ms)
├─ CLS: [X] (target: <0.1)
└─ TTFB: [X]ms

Opportunities for Improvement:
├─ [Opportunity]: Est. savings [X]ms
├─ [Opportunity]: Est. savings [X]ms
└─ [Opportunity]: Est. savings [X]ms

Actions Taken:
- [ ] Implement optimization 1
- [ ] Implement optimization 2
- [ ] Retest after changes

Trends:
- Mobile performance: [↑ improving / ↓ declining / → stable]
- Desktop performance: [↑ improving / ↓ declining / → stable]
```

---

## Part 4: Rank Tracking Setup

### Tool Recommendations

1. **Free Options:**
   - Google Search Console (built-in)
   - SE Ranking (free tier)
   - Semrush (limited free)

2. **Paid Options:**
   - Ahrefs (recommended)
   - SE Ranking
   - Semrush
   - SERPstat

### Manual Tracking Template

**Purpose:** Track target keywords manually  
**Update Frequency:** Weekly or monthly

**Tracking Spreadsheet:**

```
Keyword | Difficulty | Volume | Current Pos | Target Pos | Month 1 | Month 2 | Month 3 | Notes
--------|-----------|--------|-------------|-----------|---------|---------|---------|--------
google adk tutorial | Medium | 100 | - | 3 | 25 | 12 | 5 | [tracking notes]
agent development kit | Medium-High | 80 | - | 2 | 35 | 20 | 8 | [tracking notes]
build ai agents | High | 500 | - | 10 | 50 | 35 | 20 | [tracking notes]
adk python | Low | 30 | - | 1 | 5 | 2 | 1 | [tracking notes]
```

**How to Track Manually:**
1. Google the keyword
2. Search for your domain in results
3. Note the position (1-10 = page 1, 11-20 = page 2, etc.)
4. Record in spreadsheet
5. Update monthly to track progress

---

## Part 5: Backlink Monitoring

### Monthly Backlink Check

**Purpose:** Track domain authority growth  
**Tool:** Ahrefs, SE Ranking, or Moz (free tier)  
**Update Frequency:** Monthly

**Tracking Template:**

```
Month: [MONTH/YEAR]

Backlink Summary:
├─ Total backlinks: [X] (+[X] new)
├─ Referring domains: [X] (+[X] new)
├─ Domain rating: [X] (+[X] change)
└─ Organic traffic: [X] sessions (+[X]%)

New Backlinks:
├─ [Source]: Authority [X], Type: [Type]
├─ [Source]: Authority [X], Type: [Type]
└─ [Source]: Authority [X], Type: [Type]

Top Referring Domains:
├─ [Domain]: [Count] links, Authority [X]
├─ [Domain]: [Count] links, Authority [X]
└─ [Domain]: [Count] links, Authority [X]

Toxic Links:
├─ [Spam Domain]: [Count] links → Action: [disavow/monitor]
├─ [Spam Domain]: [Count] links → Action: [disavow/monitor]
└─ None detected: ✅

Backlink Building Actions:
- [ ] Guest post outreach: [X] contacts sent
- [ ] Resource page outreach: [X] contacts sent
- [ ] Broken link building: [X] opportunities
- [ ] Content promotion: [X] shares

Goals:
- Target backlinks: [X] (by end of month)
- Target domains: [X] (by end of month)
- Target domain authority: [X] (by end of quarter)
```

---

## Part 6: Weekly Monitoring Checklist

### Every Monday Morning (15 minutes)

```
☐ Check Search Console:
  ☐ Any new errors? [Yes/No]
  ☐ Pages indexed change? [+/- X]
  ☐ Top 3 keywords performance? [Record metrics]
  ☐ Any alerts? [Document]

☐ Check Analytics:
  ☐ Organic traffic last 7 days? [X sessions]
  ☐ New top pages? [List top 3]
  ☐ Traffic trend? [↑/↓/→]
  ☐ Bounce rate status? [X%]

☐ Core Web Vitals:
  ☐ All green? [Yes/No]
  ☐ Any pages in warning? [List]
  ☐ Performance score trend? [↑/↓/→]

☐ Content Updates:
  ☐ New content published? [Yes/No - If yes: what]
  ☐ Content optimized? [Yes/No - If yes: which pages]
  ☐ Broken links fixed? [Yes/No]

☐ Issues Found:
  ☐ [Issue]: Impact [Low/Medium/High], Fix by [Date]
  ☐ [Issue]: Impact [Low/Medium/High], Fix by [Date]
```

---

## Part 7: Monthly SEO Report Template

### Full Monthly Report

**File:** `seo_report_[MONTH]_[YEAR].md`

```markdown
# SEO Report - [Month Year]

## Executive Summary
[1-2 paragraph overview of month's performance]

## Key Metrics

| Metric | This Month | Last Month | Change | Target |
|--------|-----------|-----------|--------|--------|
| Organic Sessions | X | X | +X% | X |
| Organic Users | X | X | +X% | X |
| Organic Pageviews | X | X | +X% | X |
| Avg Session Duration | Xmin | Xmin | +X% | 3min+ |
| Bounce Rate | X% | X% | -X% | <40% |
| Keywords (Top 10) | X | X | +X | X |
| Backlinks | X | X | +X | X |
| Domain Authority | X | X | +X | X |

## Search Console Analytics

### Performance
- Impressions: X (+X%)
- Clicks: X (+X%)
- CTR: X% (+X%)
- Average Position: X (-X)

### Top 10 Keywords
1. [Keyword] - X clicks, position X
2. [Keyword] - X clicks, position X
...

### Coverage
- Indexed: X pages (X%)
- Errors: X
- Warnings: X
- Excluded: X

## Core Web Vitals
- LCP: [GOOD/NEEDS IMPROVEMENT]
- INP: [GOOD/NEEDS IMPROVEMENT]
- CLS: [GOOD/NEEDS IMPROVEMENT]

## Content Performance

### Top 5 Pages (by organic traffic)
1. [Page] - X sessions, X pageviews
2. [Page] - X sessions, X pageviews
...

### Pages Needing Improvement
1. [Page] - High bounce rate (X%), low time on page
2. [Page] - Good traffic but low conversion

## Actions Taken This Month
1. [Action] → [Result]
2. [Action] → [Result]
3. [Action] → [Result]

## Opportunities for Next Month
1. [Opportunity] - Est. impact: [X sessions/month]
2. [Opportunity] - Est. impact: [X sessions/month]
3. [Opportunity] - Est. impact: [X sessions/month]

## Goals for Next Month
- [ ] [Goal 1]
- [ ] [Goal 2]
- [ ] [Goal 3]

## Notable Events
- [Algorithm update? Traffic anomaly? etc.]

## Overall Assessment
[Comments on progress toward 6-month goals]
```

---

## Part 8: KPI Dashboard Summary

### Quick Reference: Target Metrics

```
╔════════════════════════════════════════════════════════════════╗
║              SEO PERFORMANCE DASHBOARD - TARGETS               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  MONTH 1 (Week 4-8):                                          ║
║    Organic Sessions: 50-200                                   ║
║    Indexed Pages: 90-95%                                      ║
║    Search Console Verified: ✅                                 ║
║                                                                ║
║  MONTH 2 (Week 9-13):                                         ║
║    Organic Sessions: 200-500                                  ║
║    Keywords Ranking: 20-30                                    ║
║    Core Web Vitals: All Green                                 ║
║    Coverage: No Errors                                        ║
║                                                                ║
║  MONTH 3 (Week 14-17):                                        ║
║    Organic Sessions: 500-1,500                                ║
║    Keywords Top 10: 5-10                                      ║
║    Backlinks: 5-10                                            ║
║    Avg Position: <20                                          ║
║                                                                ║
║  MONTH 6 (Goal):                                              ║
║    Organic Sessions: 5,000+ monthly                           ║
║    Keywords Ranking: 100+                                     ║
║    Keywords Top 3: 5+                                         ║
║    Backlinks: 30+                                             ║
║    Domain Authority: 25-35                                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## Tools Summary

| Tool | Purpose | Cost | Frequency |
|------|---------|------|-----------|
| Google Search Console | Track rankings, indexing | Free | Daily |
| Google Analytics | Track traffic, conversions | Free | Daily |
| PageSpeed Insights | Monitor Core Web Vitals | Free | Monthly |
| Ahrefs | Backlink tracking | $99-399/mo | Monthly |
| SE Ranking | Rank tracking, site audit | $55-199/mo | Weekly |
| Semrush | Comprehensive SEO | $120+/mo | Weekly |

**Recommended Minimum:** GSC + Analytics + PageSpeed (all free)  
**Recommended with Budget:** Add SE Ranking ($55/mo) for rank tracking

---

## Conclusion

Consistent monitoring is the foundation of successful SEO. Use these templates to:

1. **Track** what's working and what isn't
2. **Identify** opportunities quickly
3. **Make** data-driven decisions
4. **Measure** progress toward goals
5. **Iterate** and improve continuously

**Schedule:** 
- Weekly check: 15 minutes
- Monthly report: 1-2 hours
- Quarterly review: 2-3 hours

Start with free tools (GSC, Analytics, PageSpeed). Scale to paid tools as budget allows.



<Comments />
