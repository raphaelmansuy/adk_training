# Tutorial 35: AG-UI Deep Dive - Building Custom Components

**Estimated Reading Time**: 80-90 minutes  
**Difficulty Level**: Advanced  
**Prerequisites**: Tutorial 29-30 (UI Integration, Next.js + ADK), React experience, TypeScript knowledge

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites & Setup](#prerequisites--setup)
3. [Quick Start (15 Minutes)](#quick-start-15-minutes)
4. [AG-UI Protocol Deep Dive](#ag-ui-protocol-deep-dive)
5. [Building Advanced Components](#building-advanced-components)
6. [Multi-Phase Workflows](#multi-phase-workflows)
7. [Enterprise Patterns](#enterprise-patterns)
8. [Performance Optimization](#performance-optimization)
9. [Next Steps](#next-steps)

---

## Overview

### What You'll Build

In this tutorial, you'll build an **advanced research agent** with:

- **Custom Generative UI** (React components)
- **Multi-phase workflows** (Planning → Research → Analysis → Report)
- **Human-in-the-Loop** (Approval gates, feedback loops)
- **Shared State Management** (Agent ↔ App state sync)
- **Custom Event Types** (Progress tracking, cancellation)
- **Enterprise Patterns** (Error recovery, audit logs, permissions)

**Final Result**:

```text
┌─────────────────────────────────────────────────────────────┐
│  Advanced Research Agent                                     │
│  ├─ Multi-step research workflow (4 phases)                 │
│  ├─ Custom UI components (Progress, Results, Citations)     │
│  ├─ Human approval at each phase                            │
│  ├─ Real-time progress updates                              │
│  ├─ Shared context (user preferences, history)              │
│  ├─ Cancellation and error recovery                         │
│  └─ Audit trail and analytics                               │
└─────────────────────────────────────────────────────────────┘
```

### Why AG-UI Deep Dive?

| Feature | Benefit |
|---------|---------|
| **Custom Components** | Brand-aligned, polished UX |
| **Multi-Phase** | Complex workflows, not just chat |
| **HITL** | Critical decisions require human input |
| **State Sync** | Agent and app stay in sync |
| **Enterprise-Ready** | Audit, security, compliance |
| **Type-Safe** | TypeScript end-to-end |

**When to use these patterns:**

✅ Enterprise applications with complex workflows  
✅ Research and analysis tools  
✅ Multi-step approval processes  
✅ Custom branded experiences  
✅ Production apps requiring audit trails  

❌ Simple chatbots → Use Tutorial 30  
❌ Quick prototypes → Use Tutorial 32 (Streamlit)  

---

## Prerequisites & Setup

### System Requirements

```bash
# Node.js 18.17+
node --version

# Python 3.9+
python --version

# pnpm (recommended) or npm
pnpm --version
```

### API Keys

```bash
# Google AI API Key
export GOOGLE_API_KEY="your_gemini_api_key_here"
```

---

## Quick Start (15 Minutes)

### Step 1: Create Project

```bash
# Create Next.js app
npx create-next-app@latest research-agent --typescript --tailwind --app

cd research-agent

# Install CopilotKit
pnpm add @copilotkit/react-core @copilotkit/react-ui

# Install ADK dependencies (for agent)
mkdir agent
cd agent
python -m venv venv
source venv/bin/activate
pip install google-genai fastapi uvicorn ag_ui_adk python-dotenv
cd ..
```

---

### Step 2: Create Research Agent

Create `agent/agent.py`:

```python
"""
Advanced Research Agent
Multi-phase workflow: Planning → Research → Analysis → Report
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Google ADK imports
from google.adk.agents import Agent

load_dotenv()

# Research tools
def search_academic(query: str, max_results: int = 5) -> Dict:
    """
    Search academic sources.
    
    Args:
        query: Search query
        max_results: Maximum number of results
        
    Returns:
        Dict with search results
    """
    # Mock implementation - replace with real academic search API
    results = [
        {
            "title": "Deep Learning for NLP: A Survey",
            "authors": ["Smith, J.", "Doe, A."],
            "year": 2024,
            "url": "https://arxiv.org/abs/example",
            "abstract": "Comprehensive survey of deep learning methods in NLP...",
            "citations": 342
        },
        {
            "title": "Transformer Models: Past, Present, Future",
            "authors": ["Johnson, M.", "Lee, K."],
            "year": 2023,
            "url": "https://arxiv.org/abs/example2",
            "abstract": "Analysis of transformer architecture evolution...",
            "citations": 567
        }
    ]
    
    return {
        "query": query,
        "results": results[:max_results],
        "total_found": len(results)
    }

def extract_key_insights(text: str) -> Dict:
    """
    Extract key insights from research text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dict with insights
    """
    # Mock implementation - use Gemini in production
    return {
        "main_themes": [
            "Deep learning architectures",
            "Natural language processing",
            "Transfer learning"
        ],
        "key_findings": [
            "Transformers outperform RNNs for most NLP tasks",
            "Pre-training improves performance significantly"
        ],
        "research_gaps": [
            "Limited work on low-resource languages",
            "Interpretability challenges remain"
        ]
    }

def generate_citation(source: Dict) -> str:
    """
    Generate formatted citation.
    
    Args:
        source: Source information
        
    Returns:
        Formatted citation string
    """
    authors = ", ".join(source.get("authors", []))
    title = source.get("title", "Untitled")
    year = source.get("year", "n.d.")
    url = source.get("url", "")
    
    return f"{authors} ({year}). {title}. {url}"

# Create research agent using the new API
adk_agent = Agent(
    name="research_agent",
    model="gemini-2.5-flash",  # or "gemini-2.0-flash-exp"
    instruction="""You are an expert research assistant conducting academic research.

Your workflow has 4 phases:

1. PLANNING Phase:
   - Understand the research question thoroughly
   - Break down into specific sub-questions
   - Identify key topics and keywords to investigate
   - Create structured research plan
   - Emit phase state updates for UI

2. RESEARCH Phase:
   - Use search_academic() to find relevant papers
   - Collect diverse sources (aim for 5-10 papers)
   - Prioritize high-citation papers (>100 citations)
   - Note gaps in literature
   - Emit research results for UI rendering

3. ANALYSIS Phase:
   - Use extract_key_insights() on collected sources
   - Synthesize findings across all papers
   - Identify patterns, contradictions, and consensus
   - Note confidence levels for each finding
   - Emit analysis updates

4. REPORT Phase:
   - Write comprehensive research report with markdown
   - Use generate_citation() for all sources
   - Structure with clear sections: Abstract, Findings, Discussion, Conclusion
   - Include limitations and future research directions
   - Emit final report

Guidelines:
- Use **bold** for key findings
- Format reports with markdown (##, -, *, etc.)
- Request human approval before each phase transition
- Be thorough but concise (aim for clarity)
- Cite all sources properly using APA format
- Always note confidence levels ("High confidence", "Preliminary finding")
- Suggest concrete next steps""",
    tools=[search_academic, extract_key_insights, generate_citation]
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="research_agent_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="Research Agent API")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "research_agent",
        "version": "1.0.0"
    }

# Run with: uvicorn agent:app --reload --port 8000
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "agent:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
```

---

### Step 3: Create Custom UI Components

Create `app/components/ResearchProgress.tsx`:

```typescript
/**
 * Research Progress Component
 * Shows current phase and progress
 */

import React from 'react';

interface Phase {
  id: string;
  name: string;
  status: 'pending' | 'active' | 'completed' | 'error';
}

interface ResearchProgressProps {
  phases: Phase[];
  currentPhase: string;
}

export function ResearchProgress({ phases, currentPhase }: ResearchProgressProps) {
  return (
    <div className="w-full py-6">
      <div className="flex items-center justify-between">
        {phases.map((phase, index) => (
          <React.Fragment key={phase.id}>
            {/* Phase Step */}
            <div className="flex flex-col items-center">
              <div
                className={`
                  w-12 h-12 rounded-full flex items-center justify-center font-semibold text-sm
                  ${phase.status === 'completed' && 'bg-green-500 text-white'}
                  ${phase.status === 'active' && 'bg-blue-500 text-white animate-pulse'}
                  ${phase.status === 'pending' && 'bg-gray-200 text-gray-500'}
                  ${phase.status === 'error' && 'bg-red-500 text-white'}
                `}
              >
                {phase.status === 'completed' && '✓'}
                {phase.status === 'active' && index + 1}
                {phase.status === 'pending' && index + 1}
                {phase.status === 'error' && '!'}
              </div>
              <span className="mt-2 text-sm font-medium text-gray-700">
                {phase.name}
              </span>
            </div>

            {/* Connector Line */}
            {index < phases.length - 1 && (
              <div
                className={`
                  flex-1 h-1 mx-4
                  ${phases[index + 1].status !== 'pending' ? 'bg-green-500' : 'bg-gray-200'}
                `}
              />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
```

Create `app/components/ResearchResult.tsx`:

```typescript
/**
 * Research Result Component
 * Displays research findings with citations
 */

interface Source {
  title: string;
  authors: string[];
  year: number;
  url: string;
  abstract: string;
  citations: number;
}

interface ResearchResultProps {
  title: string;
  summary: string;
  sources: Source[];
}

export function ResearchResult({ title, summary, sources }: ResearchResultProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 my-4">
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
      
      <div className="prose prose-sm max-w-none mb-6">
        <p className="text-gray-700">{summary}</p>
      </div>

      {sources && sources.length > 0 && (
        <div className="border-t pt-4">
          <h4 className="font-semibold text-gray-900 mb-3">Sources:</h4>
          <div className="space-y-3">
            {sources.map((source, index) => (
              <div key={index} className="bg-gray-50 rounded p-3">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                  {source.title}
                </a>
                <p className="text-sm text-gray-600 mt-1">
                  {source.authors.join(', ')} ({source.year})
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {source.citations} citations
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### Step 4: Build Main App

Update `app/page.tsx`:

```typescript
"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { useState } from "react";
import { ResearchProgress } from "./components/ResearchProgress";
import { ResearchResult } from "./components/ResearchResult";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

export default function Home() {
  // Research workflow state
  const [phases, setPhases] = useState([
    { id: 'planning', name: 'Planning', status: 'pending' as const },
    { id: 'research', name: 'Research', status: 'pending' as const },
    { id: 'analysis', name: 'Analysis', status: 'pending' as const },
    { id: 'report', name: 'Report', status: 'pending' as const },
  ]);

  const [currentPhase, setCurrentPhase] = useState('planning');
  const [results, setResults] = useState<any[]>([]);

  // Make workflow state readable by agent
  useCopilotReadable({
    description: "Current research workflow phase",
    value: {
      currentPhase,
      phases: phases.map(p => ({ id: p.id, name: p.name, status: p.status }))
    }
  });

  // Action: Update phase
  useCopilotAction({
    name: "update_phase",
    description: "Update the current research phase",
    parameters: [
      {
        name: "phase",
        type: "string",
        description: "Phase ID to activate",
        enum: ["planning", "research", "analysis", "report"]
      },
      {
        name: "status",
        type: "string",
        description: "Phase status",
        enum: ["pending", "active", "completed", "error"]
      }
    ],
    handler: async ({ phase, status }) => {
      setPhases(prev => prev.map(p =>
        p.id === phase ? { ...p, status } : p
      ));
      
      if (status === 'active') {
        setCurrentPhase(phase);
      }
      
      return { success: true, phase, status };
    }
  });

  // Action: Add research result
  useCopilotAction({
    name: "add_research_result",
    description: "Add a research finding to the results",
    parameters: [
      {
        name: "title",
        type: "string",
        description: "Result title"
      },
      {
        name: "summary",
        type: "string",
        description: "Result summary"
      },
      {
        name: "sources",
        type: "object[]",
        description: "Source citations"
      }
    ],
    handler: async ({ title, summary, sources }) => {
      const newResult = { title, summary, sources };
      setResults(prev => [...prev, newResult]);
      return { success: true };
    },
    render: ({ title, summary, sources }) => {
      return <ResearchResult title={title} summary={summary} sources={sources} />;
    }
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      <CopilotKit runtimeUrl="http://localhost:8000/copilotkit">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="max-w-6xl mx-auto mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🔬 Research Agent
            </h1>
            <p className="text-lg text-gray-600">
              Advanced multi-phase research with human-in-the-loop
            </p>
          </div>

          {/* Progress Tracker */}
          <div className="max-w-6xl mx-auto mb-8 bg-white rounded-lg shadow-lg p-6">
            <ResearchProgress phases={phases} currentPhase={currentPhase} />
          </div>

          {/* Main Layout */}
          <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chat Interface */}
            <div className="lg:col-span-2 bg-white rounded-lg shadow-xl overflow-hidden">
              <CopilotChat
                instructions={`You are conducting research in the ${currentPhase} phase. Follow the multi-phase workflow.`}
                labels={{
                  title: "Research Assistant",
                  initial: "Hi! I'm your research assistant. What would you like to research today?\n\nI'll guide you through:\n1. Planning - Define research scope\n2. Research - Find relevant sources\n3. Analysis - Synthesize findings\n4. Report - Generate final report"
                }}
                className="h-[600px]"
              />
            </div>

            {/* Results Panel */}
            <div className="bg-white rounded-lg shadow-xl p-6 overflow-y-auto max-h-[600px]">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                Research Findings
              </h2>
              
              {results.length === 0 ? (
                <p className="text-gray-500 text-sm">
                  Research results will appear here as the agent makes discoveries.
                </p>
              ) : (
                <div className="space-y-4">
                  {results.map((result, index) => (
                    <ResearchResult
                      key={index}
                      title={result.title}
                      summary={result.summary}
                      sources={result.sources}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </CopilotKit>
    </div>
  );
}
```

---

### Step 5: Run Everything

```bash
# Terminal 1: Run agent
cd agent
source venv/bin/activate
export GOOGLE_API_KEY="your_key"
python agent.py

# Terminal 2: Run Next.js
cd ..
pnpm dev
```

**Open http://localhost:3000** and try:

"Research the latest advances in large language models"

Watch the agent progress through phases with your custom UI! 🎨

---

## AG-UI Protocol Deep Dive

### Protocol Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CopilotKit React SDK                                │  │
│  │  ├─ <CopilotKit> Provider                            │  │
│  │  ├─ useCopilotAction() - Define actions             │  │
│  │  ├─ useCopilotReadable() - Share state              │  │
│  │  └─ <CopilotChat> - UI component                    │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ AG-UI Protocol (WebSocket/SSE)
                        │ Event Types:
                        │ - textMessage
                        │ - actionRequest
                        │ - stateUpdate
                        │ - progressUpdate
                        │
┌───────────────────────▼─────────────────────────────────────┐
│            BACKEND (Python)                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ag_ui_adk (AG-UI middleware)                        │  │
│  │  ├─ AG-UI Protocol adapter                           │  │
│  │  ├─ Event routing                                    │  │
│  │  ├─ Session management                               │  │
│  │  └─ Function call translation                        │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │  Google ADK Agent (LlmAgent)                         │  │
│  │  ├─ Instructions + Tools                             │  │
│  │  ├─ Session state                                    │  │
│  │  └─ Response generation                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Event Flow

**1. User Message**:

```typescript
// Frontend sends
{
  type: "textMessage",
  content: "Research AI safety",
  sessionId: "session-123"
}
```

**2. Backend Processes**:

```python
# ag_ui_adk middleware translates to ADK format
response = adk_agent.execute(
    message="Research AI safety"
)
```

**3. Agent Uses Action**:

```python
# Agent calls function
search_academic(query="AI safety")

# ag_ui_adk translates to AG-UI actionRequest
{
  type: "actionRequest",
  action: "search_academic",
  params: { query: "AI safety" }
}
```

**4. Frontend Executes**:

```typescript
useCopilotAction({
  name: "search_academic",
  handler: async ({ query }) => {
    const results = await searchAPI(query);
    return results;
  }
});
```

**5. Result Flows Back**:

```text
Frontend → Backend → Agent → Response → Frontend
```

---

### Custom Event Types

Extend the protocol with custom events:

```typescript
// Custom progress event
interface ProgressEvent {
  type: "progress";
  phase: string;
  percentage: number;
  message: string;
}

// Custom cancellation event
interface CancellationEvent {
  type: "cancel";
  reason: string;
}

// Send custom event
const sendProgressUpdate = (phase: string, percentage: number) => {
  // Custom implementation using CopilotKit's internal messaging
  window.dispatchEvent(new CustomEvent('copilot-progress', {
    detail: { phase, percentage }
  }));
};
```

---

## Building Advanced Components

### Pattern 1: Generative UI with State

Create dynamic components based on agent output:

```typescript
/**
 * Data Visualization Component
 * Rendered when agent generates chart data
 */

import { useCopilotAction } from "@copilotkit/react-core";
import { Line, Bar, Pie } from 'react-chartjs-2';

export function useDataVisualization() {
  useCopilotAction({
    name: "render_chart",
    description: "Render a data visualization chart",
    parameters: [
      {
        name: "chartType",
        type: "string",
        enum: ["line", "bar", "pie"],
        description: "Type of chart to render"
      },
      {
        name: "data",
        type: "object",
        description: "Chart data with labels and datasets"
      },
      {
        name: "title",
        type: "string",
        description: "Chart title"
      }
    ],
    handler: async ({ chartType, data, title }) => {
      // Store chart data in state
      return { success: true, chartType, data, title };
    },
    render: ({ chartType, data, title }) => {
      const ChartComponent = 
        chartType === 'line' ? Line :
        chartType === 'bar' ? Bar :
        Pie;

      return (
        <div className="bg-white rounded-lg shadow p-4 my-4">
          <h3 className="text-lg font-semibold mb-3">{title}</h3>
          <ChartComponent data={data} options={{
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              title: { display: true, text: title }
            }
          }} />
        </div>
      );
    }
  });
}
```

**Agent uses it**:

```python
# In agent tools
def create_visualization(chart_type: str, data: dict, title: str) -> dict:
    """Create a visualization chart."""
    return {
        "action": "render_chart",
        "chartType": chart_type,
        "data": data,
        "title": title
    }

# Agent can now say:
# "Let me visualize this data for you..."
# Then call create_visualization() tool
```

---

### Pattern 2: Human-in-the-Loop with Approvals

Implement approval gates:

```typescript
/**
 * Approval Component
 * Shows approval request from agent
 */

import { useCopilotAction } from "@copilotkit/react-core";
import { useState } from "react";

export function useApprovalGate() {
  const [pendingApproval, setPendingApproval] = useState<any>(null);

  useCopilotAction({
    name: "request_approval",
    description: "Request human approval before proceeding",
    parameters: [
      {
        name: "action",
        type: "string",
        description: "Action requiring approval"
      },
      {
        name: "details",
        type: "string",
        description: "Details about the action"
      },
      {
        name: "impact",
        type: "string",
        description: "Potential impact of the action"
      }
    ],
    handler: async ({ action, details, impact }) => {
      return new Promise((resolve) => {
        setPendingApproval({
          action,
          details,
          impact,
          resolve
        });
      });
    },
    render: ({ action, details, impact }) => {
      if (!pendingApproval) return null;

      const handleApprove = () => {
        pendingApproval.resolve({ approved: true });
        setPendingApproval(null);
      };

      const handleReject = () => {
        pendingApproval.resolve({ approved: false });
        setPendingApproval(null);
      };

      return (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 my-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3 flex-1">
              <h3 className="text-sm font-medium text-yellow-800">
                Approval Required: {action}
              </h3>
              <p className="mt-2 text-sm text-yellow-700">{details}</p>
              <p className="mt-2 text-xs text-yellow-600">
                <strong>Impact:</strong> {impact}
              </p>
              <div className="mt-4 flex gap-3">
                <button
                  onClick={handleApprove}
                  className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                  ✓ Approve
                </button>
                <button
                  onClick={handleReject}
                  className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  ✗ Reject
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }
  });
}
```

**Agent requests approval**:

```python
# Before critical action
def proceed_to_next_phase(phase: str) -> dict:
    """Request approval before proceeding to next phase."""
    # This triggers approval UI
    return {
        "action": "request_approval",
        "details": f"Ready to proceed to {phase} phase",
        "impact": "Will execute search queries and process results"
    }
```

---

### Pattern 3: Shared State Synchronization

Bidirectional state sync:

```typescript
/**
 * Shared State Manager
 * Keeps agent and app in sync
 */

import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { useState, useEffect } from "react";

export function useSharedResearchState() {
  const [researchContext, setResearchContext] = useState({
    topic: "",
    keywords: [],
    sources: [],
    notes: [],
    preferences: {
      depth: "comprehensive",
      maxSources: 10
    }
  });

  // Make state readable by agent
  useCopilotReadable({
    description: "Current research context and preferences",
    value: researchContext
  });

  // Allow agent to update state
  useCopilotAction({
    name: "update_research_context",
    description: "Update the research context state",
    parameters: [
      {
        name: "field",
        type: "string",
        description: "Field to update (topic, keywords, sources, notes)"
      },
      {
        name: "value",
        type: "string",
        description: "New value"
      }
    ],
    handler: async ({ field, value }) => {
      setResearchContext(prev => ({
        ...prev,
        [field]: value
      }));
      return { success: true, field, value };
    }
  });

  // Persist to backend
  useEffect(() => {
    const saveContext = async () => {
      await fetch('/api/context', {
        method: 'POST',
        body: JSON.stringify(researchContext)
      });
    };

    const debounce = setTimeout(saveContext, 1000);
    return () => clearTimeout(debounce);
  }, [researchContext]);

  return { researchContext, setResearchContext };
}
```

---

## Multi-Phase Workflows

### Workflow Orchestration

```typescript
/**
 * Workflow Manager
 * Orchestrates multi-phase research workflow
 */

import { useState, useCallback } from "react";
import { useCopilotAction, useCopilotReadable } from "@copilotkit/react-core";

interface WorkflowPhase {
  id: string;
  name: string;
  description: string;
  requiredApproval: boolean;
  status: 'pending' | 'active' | 'completed' | 'error';
  result?: any;
}

export function useWorkflowManager() {
  const [workflow, setWorkflow] = useState<WorkflowPhase[]>([
    {
      id: 'planning',
      name: 'Research Planning',
      description: 'Define research scope and methodology',
      requiredApproval: false,
      status: 'active'
    },
    {
      id: 'research',
      name: 'Source Research',
      description: 'Find and collect relevant sources',
      requiredApproval: true,
      status: 'pending'
    },
    {
      id: 'analysis',
      name: 'Analysis & Synthesis',
      description: 'Analyze findings and synthesize insights',
      requiredApproval: true,
      status: 'pending'
    },
    {
      id: 'report',
      name: 'Report Generation',
      description: 'Generate comprehensive research report',
      requiredApproval: false,
      status: 'pending'
    }
  ]);

  const [currentPhaseIndex, setCurrentPhaseIndex] = useState(0);

  // Make workflow readable by agent
  useCopilotReadable({
    description: "Current workflow state and phase information",
    value: {
      phases: workflow,
      currentPhase: workflow[currentPhaseIndex],
      currentPhaseIndex
    }
  });

  // Complete phase action
  useCopilotAction({
    name: "complete_phase",
    description: "Mark current phase as complete and move to next",
    parameters: [
      {
        name: "phaseId",
        type: "string",
        description: "ID of phase to complete"
      },
      {
        name: "result",
        type: "object",
        description: "Phase result data"
      }
    ],
    handler: async ({ phaseId, result }) => {
      setWorkflow(prev => prev.map(phase =>
        phase.id === phaseId
          ? { ...phase, status: 'completed', result }
          : phase
      ));

      // Move to next phase
      const currentIndex = workflow.findIndex(p => p.id === phaseId);
      if (currentIndex < workflow.length - 1) {
        setCurrentPhaseIndex(currentIndex + 1);
        setWorkflow(prev => prev.map((phase, idx) =>
          idx === currentIndex + 1
            ? { ...phase, status: 'active' }
            : phase
        ));
      }

      return { success: true, nextPhase: workflow[currentIndex + 1]?.id };
    }
  });

  // Error handling
  useCopilotAction({
    name: "mark_phase_error",
    description: "Mark phase as error state",
    parameters: [
      {
        name: "phaseId",
        type: "string",
        description: "Phase ID"
      },
      {
        name: "error",
        type: "string",
        description: "Error message"
      }
    ],
    handler: async ({ phaseId, error }) => {
      setWorkflow(prev => prev.map(phase =>
        phase.id === phaseId
          ? { ...phase, status: 'error', result: { error } }
          : phase
      ));
      return { success: true };
    }
  });

  return {
    workflow,
    currentPhase: workflow[currentPhaseIndex],
    currentPhaseIndex
  };
}
```

---

## Enterprise Patterns

### Pattern 1: Audit Trail

Track all agent actions:

```typescript
/**
 * Audit Logger
 * Logs all agent actions for compliance
 */

import { useEffect, useRef } from "react";
import { useCopilotAction } from "@copilotkit/react-core";

interface AuditEntry {
  timestamp: string;
  userId: string;
  action: string;
  params: any;
  result: any;
  duration: number;
}

export function useAuditLogger(userId: string) {
  const auditLog = useRef<AuditEntry[]>([]);

  // Log action execution
  const logAction = async (entry: AuditEntry) => {
    auditLog.current.push(entry);

    // Send to backend
    await fetch('/api/audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry)
    });
  };

  // Wrap all actions with logging
  useCopilotAction({
    name: "search_with_audit",
    description: "Search with audit logging",
    parameters: [
      {
        name: "query",
        type: "string",
        description: "Search query"
      }
    ],
    handler: async ({ query }) => {
      const startTime = Date.now();

      try {
        // Execute action
        const result = await performSearch(query);

        // Log success
        await logAction({
          timestamp: new Date().toISOString(),
          userId,
          action: "search",
          params: { query },
          result,
          duration: Date.now() - startTime
        });

        return result;

      } catch (error) {
        // Log error
        await logAction({
          timestamp: new Date().toISOString(),
          userId,
          action: "search",
          params: { query },
          result: { error: String(error) },
          duration: Date.now() - startTime
        });

        throw error;
      }
    }
  });

  return { auditLog: auditLog.current };
}
```

---

### Pattern 2: Permission-Based Actions

Role-based access control:

```typescript
/**
 * Permission Manager
 * Controls what actions users can perform
 */

interface UserPermissions {
  canSearch: boolean;
  canAnalyze: boolean;
  canExport: boolean;
  canApprove: boolean;
}

export function usePermissionControl(permissions: UserPermissions) {
  useCopilotAction({
    name: "search_academic",
    description: "Search academic sources (requires permission)",
    parameters: [{ name: "query", type: "string" }],
    handler: async ({ query }) => {
      // Check permission
      if (!permissions.canSearch) {
        throw new Error("Permission denied: search_academic requires canSearch permission");
      }

      // Execute action
      return await performSearch(query);
    }
  });

  useCopilotAction({
    name: "export_results",
    description: "Export research results (requires permission)",
    parameters: [{ name: "format", type: "string" }],
    handler: async ({ format }) => {
      if (!permissions.canExport) {
        throw new Error("Permission denied: export requires canExport permission");
      }

      return await exportResults(format);
    }
  });

  // Agent receives permission info
  useCopilotReadable({
    description: "User permissions and capabilities",
    value: permissions
  });
}
```

---

### Pattern 3: Rate Limiting

Prevent abuse:

```typescript
/**
 * Rate Limiter
 * Limits action execution frequency
 */

import { useRef } from "react";

interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}

export function useRateLimiter(config: RateLimitConfig) {
  const requestLog = useRef<number[]>([]);

  const checkRateLimit = (): boolean => {
    const now = Date.now();
    
    // Remove old requests outside window
    requestLog.current = requestLog.current.filter(
      time => now - time < config.windowMs
    );

    // Check if under limit
    if (requestLog.current.length >= config.maxRequests) {
      return false;
    }

    // Add current request
    requestLog.current.push(now);
    return true;
  };

  useCopilotAction({
    name: "rate_limited_search",
    description: "Search with rate limiting",
    parameters: [{ name: "query", type: "string" }],
    handler: async ({ query }) => {
      if (!checkRateLimit()) {
        throw new Error(
          `Rate limit exceeded: max ${config.maxRequests} requests per ${config.windowMs}ms`
        );
      }

      return await performSearch(query);
    }
  });
}
```

---

## Performance Optimization

### Optimization 1: Lazy Loading Components

```typescript
/**
 * Lazy load heavy components
 */

import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false
});

export function OptimizedResearch() {
  return (
    <div>
      {/* Only load when needed */}
      {showChart && <HeavyChart data={chartData} />}
    </div>
  );
}
```

---

### Optimization 2: Debounced State Updates

```typescript
/**
 * Debounce state updates to reduce re-renders
 */

import { useState, useEffect, useRef } from "react";

export function useDebouncedState<T>(initialValue: T, delay: number = 500) {
  const [value, setValue] = useState<T>(initialValue);
  const [debouncedValue, setDebouncedValue] = useState<T>(initialValue);
  const timeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set new timeout
    timeoutRef.current = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, delay]);

  return [value, setValue, debouncedValue] as const;
}

// Usage
const [query, setQuery, debouncedQuery] = useDebouncedState("", 500);

useCopilotReadable({
  description: "User search query",
  value: debouncedQuery  // Only updates every 500ms
});
```

---

### Optimization 3: Memoized Actions

```typescript
/**
 * Memoize expensive computations
 */

import { useMemo } from "react";
import { useCopilotAction } from "@copilotkit/react-core";

export function useOptimizedAnalysis() {
  // Memoize expensive processing
  const processedData = useMemo(() => {
    return expensiveDataProcessing(rawData);
  }, [rawData]);

  useCopilotAction({
    name: "analyze_data",
    description: "Analyze research data",
    parameters: [],
    handler: async () => {
      // Use memoized result
      return processedData;
    }
  });
}
```

---

## Next Steps

### You've Mastered AG-UI! 🎉

You now know:

✅ Advanced CopilotKit patterns and components  
✅ Multi-phase workflow orchestration  
✅ Human-in-the-loop with approval gates  
✅ Bidirectional state synchronization  
✅ Enterprise patterns (audit, permissions, rate limiting)  
✅ Performance optimization techniques  
✅ Custom event types and protocol extensions  

### Complete Tutorial Series

Congratulations! You've completed the entire ADK UI Integration series:

1. ✅ **Tutorial 29**: Introduction to UI Integration & AG-UI Protocol
2. ✅ **Tutorial 30**: Next.js 15 + ADK Integration (AG-UI)
3. ✅ **Tutorial 31**: React Vite + ADK Integration (AG-UI)
4. ✅ **Tutorial 32**: Streamlit + ADK Integration (Native API)
5. ✅ **Tutorial 33**: Slack Bot Integration with ADK
6. ✅ **Tutorial 34**: Google Cloud Pub/Sub + Event-Driven Agents
7. ✅ **Tutorial 35**: AG-UI Deep Dive - Building Custom Components

### Additional Resources

- [CopilotKit Documentation](https://docs.copilotkit.ai)
- [AG-UI Protocol Specification](https://docs.copilotkit.ai/adk/protocol)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Example Applications](https://github.com/CopilotKit/CopilotKit/tree/main/examples)

---

**🎉 Tutorial 35 Complete! Series Complete! 🎊**

You've built **7 comprehensive tutorials** covering every major UI integration pattern for Google ADK! 🚀

---

**Questions or feedback?** Open an issue on the [ADK Training Repository](https://github.com/google/adk-training).
