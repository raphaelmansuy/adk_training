# Commerce Agent - Visual Problem Analysis

## Problem Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                      REAL USER SESSION TEST                          │
│                    (15+ conversation turns)                          │
└─────────────────────────────────────────────────────────────────────┘

USER WANTS: Running shoes + minimal shorts
   ↓
AGENT RESPONSE: Asks 15 questions about preferences ⚠️ TOO MANY QUESTIONS
   ├─ Activity type
   ├─ Weather
   ├─ Shoe lightness
   ├─ Terrain type
   ├─ Shorts length
   ├─ Liner preference
   ├─ Pocket preference
   ├─ Budget
   ├─ Materials
   └─ ... more
   ↓
AGENT SEARCHES: "running shoes site:decathlon.fr"
   ↓
GOOGLE RETURNS: Adidas, New Balance, Road Runner Sports, Sports Direct ❌
   (NOT from Decathlon!)
   ↓
AGENT PROVIDES: Generic descriptions
   - "Kalenji Run 100 is great for casual jogs"
   - "Kiprun KD900X has carbon plate technology"
   - etc.
   (NO LINKS, NO REAL DATA) ❌
   ↓
USER ASKS: "Do you have the link to the products?"
   ↓
AGENT RESPONDS: "I cannot generate URLs. Search manually on Decathlon.fr"
   ❌ FAILED - User has to search anyway!
```

---

## Issue #1: Search Strategy Not Working

```
CURRENT APPROACH (FAILING):
┌─────────────────────────────────────────────────────┐
│  Prompt: "Use site:decathlon.fr in searches"       │
│                    ↓                                 │
│  LLM Constructs: "site:decathlon.fr running shoes" │
│                    ↓                                 │
│  Google Search Tool Receives: (unclear)            │
│                    ↓                                 │
│  Google API Returns: Generic results               │
│  (Adidas, Amazon, eBay, Sports Direct)             │
│                    ↓                                 │
│  RESULT: ❌ Wrong products!                         │
└─────────────────────────────────────────────────────┘

WHAT WENT WRONG:
  - site: operator may not work with Gemini API
  - Only works with Vertex AI backend
  - Google Search API might filter it out
  - No fallback when it fails
  - Can't debug or detect failure
```

---

## Issue #2: No Product Links

```
AGENT WORKFLOW (CURRENT):
┌─────────────────────────────────────────┐
│  Search for products                    │
│           ↓                             │
│  Create engaging narratives             │
│           ↓                             │
│  Tell user about products ✓             │
│           ↓                             │
│  Provide product links? ❌              │
│           ↓                             │
│  User must search manually on Decathlon │
└─────────────────────────────────────────┘

WHAT USER GETS:
  Product: "Kalenji Run 100"
  Description: "Great for casual jogs, €29.99"
  Link: ❌ NONE - User says "where do I buy it?"

WHAT USER NEEDS:
  Product: "Kalenji Run 100"
  Description: "Great for casual jogs, €29.99"
  Link: ✓ https://www.decathlon.fr/p/KALENJI_RUN_100
```

---

## Issue #3: No Product Database

```
AGENT'S PRODUCT KNOWLEDGE:

┌──────────────────────────────────────┐
│  Brand Name Awareness                │
├──────────────────────────────────────┤
│  ✓ Knows Kalenji = running           │
│  ✓ Knows Kiprun = trail running      │
│  ✓ Knows Quechua = hiking            │
│  ✓ Knows Rockrider = mountain bikes  │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  Actual Product Data                 │
├──────────────────────────────────────┤
│  ✗ No product IDs                    │
│  ✗ No prices                         │
│  ✗ No product links                  │
│  ✗ No availability/inventory          │
│  ✗ No real product specs             │
│  ✗ No images                         │
│  ✗ No customer reviews               │
└──────────────────────────────────────┘

WHAT'S NEEDED: Product Database
┌──────────────────────────────────────┐
│ {                                    │
│   "id": "KALENJI_RUN_100",           │
│   "name": "Kalenji Run 100",         │
│   "price": 29.99,                   │
│   "url": "decathlon.fr/p/...",       │
│   "category": "running_shoes",       │
│   "features": ["lightweight",        │
│                "breathable"],        │
│   "rating": 4.5,                    │
│   "in_stock": true                  │
│ }                                    │
└──────────────────────────────────────┘
```

---

## Issue #4: Excessive Preference Gathering

```
CURRENT CONVERSATION FLOW (15+ TURNS):

Turn 1: User: "I want running shoes"
        Agent: "What activity type?"
        
Turn 2: User: "Casual jogs"
        Agent: "What weather?"
        
Turn 3: User: "Hot weather"
        Agent: "How light should they be?"
        
Turn 4: User: "Extreme lightness"
        Agent: "What terrain?"
        
Turn 5: User: "Mix of roads and trails"
        Agent: "What's your budget?"
        
Turn 6: User: "Less than €300"
        Agent: "Here are products!"
        
PROBLEM: Too many back-and-forth turns!

═════════════════════════════════════════

BETTER FLOW (3-5 TURNS):

Turn 1: User: "I want running shoes"
        Agent: "Quick questions:
        A) What type? Casual/long-distance/racing/trails
        B) Budget? Under €50 / €50-100 / €100-150 / No limit
        C) Terrain? Roads/trails/mix"
        
Turn 2: User: "Casual, <€100, mix"
        Agent: "Here are top 3 recommendations:
        1️⃣ Kalenji Run 100 - €29.99 [LINK]
        2️⃣ Jogflow 100.1 - €49.99 [LINK]
        3️⃣ Run Active - €69.99 [LINK]
        
        Want details on any?"
        
BENEFIT: 2 turns instead of 6+ ✓
         Faster recommendations ✓
         Better user experience ✓
```

---

## Issue #5: Poor Error Handling

```
WHEN SEARCH FAILS (CURRENT):

Search: "running shoes site:decathlon.fr"
Result: Adidas, Amazon, eBay, Sports Direct
        ↓
Agent: "Here are some great Decathlon products:
        - Kalenji Run 100
        - Kiprun KD900X
        - ..."
        ↑ MASKS FAILURE - User thinks search worked!

PROBLEM: User trusts recommendations that might be generic


WHEN SEARCH FAILS (BETTER):

Search: "running shoes site:decathlon.fr"
Result: Adidas, Amazon, eBay, Sports Direct
        ↓
Agent: "I couldn't find that specific product on Decathlon.

        Here's what I can suggest:
        ✓ Similar products: [links]
        ✓ Browse categories: [links]
        ✓ See all running shoes: [link]
        
        Would you like alternatives?"
        
BENEFIT: Transparent, builds trust ✓
         User knows there's a fallback ✓
         Better UX ✓
```

---

## Issue #6: Agent Inefficiency

```
CURRENT PREFERENCE GATHERING:

Turn 1: PreferenceManager (Agent Tool)
        → LLM call: "understand user preferences"
        → Store in database
        → Token usage: ~500
        → API calls: 1
        
Turn 2: PreferenceManager again
        → LLM call: "answer a similar question"
        → Token usage: ~500
        → API calls: 1
        
... repeat for 15 turns ...

TOTAL: ~7,500 tokens, 15 API calls


BETTER APPROACH:

Turn 1: Direct preference function (Python)
        → Parse "casual jogs, hot weather"
        → Store instantly
        → Token usage: 0
        → API calls: 0
        
Turn 2: Another direct function
        → Parse "extreme lightness"
        → Store instantly
        → Token usage: 0
        → API calls: 0
        
BENEFIT: 
  ✓ Same result with 90% fewer tokens
  ✓ Instant responses (no LLM latency)
  ✓ No API calls wasted
  ✓ Lower cost
```

---

## Issue #7: Search Tool Integration

```
PROBLEM: Can't Debug Search

┌──────────────────────────────────────────┐
│  Current Flow:                           │
├──────────────────────────────────────────┤
│  1. Agent constructs query               │
│  2. Sends to google_search tool          │
│  3. Gets results back                    │
│  4. NO VISIBILITY into:                  │
│     ✗ What query was actually sent?      │
│     ✗ Did site: get respected?           │
│     ✗ Why are results wrong?             │
│     ✗ Can we detect failure?             │
└──────────────────────────────────────────┘

WHAT'S NEEDED:

┌──────────────────────────────────────────┐
│  Add Logging & Inspection:               │
├──────────────────────────────────────────┤
│  ✓ Log actual query sent                 │
│  ✓ Inspect results for domain            │
│  ✓ Detect when results aren't from       │
│    Decathlon.fr                          │
│  ✓ Trigger fallback mechanism            │
│  ✓ Alert on failures                     │
└──────────────────────────────────────────┘
```

---

## Summary: Impact of Issues

```
┌─────────────────────────────────────────────────────────────┐
│              USER EXPERIENCE FLOW                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. User asks for products                                 │
│     ✓ SUCCESS                                              │
│                                                             │
│  2. Agent gathers preferences                              │
│     ⚠️ SLOW (15+ questions)                                │
│                                                             │
│  3. Agent searches for products                            │
│     ❌ FAIL (wrong retailers)                              │
│                                                             │
│  4. Agent provides recommendations                         │
│     ⚠️ GENERIC (no links, no real data)                    │
│                                                             │
│  5. User gets product links                                │
│     ❌ FAIL (agent can't provide them)                     │
│                                                             │
│  6. User purchases from Decathlon                          │
│     ❌ FAIL (user abandoned, searching manually)           │
│                                                             │
│  CONVERSION RATE: ~0% ❌                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Solution: Priority Fixes

```
WEEK 1: QUICK WINS (4-5 hours total)
┌───────────────────────────────────────┐
│ 1. Build Product Database             │
│    ├─ Curate 200+ Decathlon products  │
│    ├─ Add: ID, name, price, URL       │
│    ├─ Time: 2-3 hours                 │
│    └─ Impact: CRITICAL ✓✓✓            │
│                                       │
│ 2. Add Direct Links                   │
│    ├─ Modify recommendations          │
│    ├─ Include product URLs            │
│    ├─ Time: 30 minutes                │
│    └─ Impact: CRITICAL ✓✓✓            │
│                                       │
│ 3. Simplify Preferences               │
│    ├─ 15 questions → 3 questions      │
│    ├─ Add quick buttons               │
│    ├─ Time: 1 hour                    │
│    └─ Impact: HIGH ✓✓                 │
└───────────────────────────────────────┘

WEEK 2-3: FOUNDATION FIXES (8-10 hours)
┌───────────────────────────────────────┐
│ 4. Fix Search Strategy                │
│    ├─ Option 2: Custom tool wrapper   │
│    ├─ Search database first           │
│    ├─ Google as fallback              │
│    └─ Impact: CRITICAL ✓✓✓            │
│                                       │
│ 5. Improve Error Handling             │
│    ├─ Clear failure messages          │
│    ├─ Suggest alternatives            │
│    └─ Impact: HIGH ✓✓                 │
│                                       │
│ 6. Optimize Agent Coordination        │
│    ├─ Direct tools vs sub-agents      │
│    ├─ Reduce API calls                │
│    └─ Impact: MEDIUM ✓                │
└───────────────────────────────────────┘

RESULT AFTER FIXES:
┌─────────────────────────────────────────┐
│  Conversion Rate: ~0% → 15-25% ✓✓✓     │
│  Time to Recommendations: 15 → 3 turns  │
│  Product Links: 0% → 100%               │
│  Search Accuracy: Wrong → Correct       │
│  User Satisfaction: Low → High          │
└─────────────────────────────────────────┘
```

---

## Next Steps

1. **Validate Issues**
   - Add logging to search queries
   - Run test with site: operator
   - Confirm root causes

2. **Implement Quick Wins**
   - Start with product database
   - Add links
   - Simplify preferences

3. **Plan Migration**
   - Decide between Option 2 or Option 3
   - Get stakeholder buy-in
   - Schedule implementation

4. **Test & Measure**
   - Run new agent with real users
   - Track conversion rates
   - Collect feedback

---

**Analysis:** 2025-01-24  
**Next Review:** After implementing Week 1 fixes
