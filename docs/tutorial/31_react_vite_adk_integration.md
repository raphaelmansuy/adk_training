---
id: react_vite_adk_integration
---

# Tutorial 31: React Vite + ADK Integration (AG-UI Protocol)

**Estimated Reading Time**: 60-70 minutes  
**Difficulty Level**: Intermediate  
**Prerequisites**: Tutorial 29 (UI Integration Intro), Tutorial 30 (Next.js + ADK), Basic React knowledge

---

## Table of Contents

1. [Overview](#overview)
2. [Why Vite for ADK Integration?](#why-vite-for-adk-integration)
3. [Quick Start (5 Minutes)](#quick-start-5-minutes)
4. [Building a Data Analysis Dashboard](#building-a-data-analysis-dashboard)
5. [Advanced Features](#advanced-features)
6. [Production Deployment](#production-deployment)
7. [Vite vs Next.js Comparison](#vite-vs-nextjs-comparison)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Overview

### What You'll Build

In this tutorial, you'll build a **real-time data analysis dashboard** using:

- **React 18** (with Vite)
- **CopilotKit** (AG-UI Protocol)
- **Google ADK** (Agent backend)
- **Gemini 2.0 Flash** (LLM)
- **Chart.js** (Visualizations)

**Final Result**:

```text
┌─────────────────────────────────────────────────────────────┐
│  Data Analysis Dashboard                                     │
│  ├─ Upload CSV files                                         │
│  ├─ Ask questions about data ("What's the trend?")          │
│  ├─ Agent analyzes and generates insights                   │
│  ├─ Interactive charts render inline                        │
│  ├─ Export analysis reports                                 │
│  └─ Deploy to Netlify/Vercel in minutes                     │
└─────────────────────────────────────────────────────────────┘
```

### Tutorial Goals

✅ Understand Vite + React + ADK architecture  
✅ Build a data analysis agent with pandas tools  
✅ Implement generative UI for charts  
✅ Handle file uploads and processing  
✅ Deploy to production (Netlify or Vercel)  
✅ Compare Vite vs Next.js approaches  

---

## Why Vite for ADK Integration?

### Vite Advantages

| Feature | Benefit |
|---------|---------|
| **⚡ Instant Server Start** | Sub-second cold starts vs Next.js `3-5s` |
| **🔥 Lightning HMR** | Updates in &lt;50ms, no page refresh |
| **📦 Optimized Build** | Smaller bundle sizes (50-70% of Next.js) |
| **🎯 Simple Config** | Single vite.config.js vs Next.js complexity |
| **🚀 Fast CI/CD** | 2x-5x faster build times |

### When to Choose Vite

**Choose Vite** when you need:
- 🏃 Fast prototyping and development
- 📱 Single-page applications (SPAs)
- 🎨 Interactive dashboards and tools
- 💰 Smaller bundle sizes
- ⚙️ Simple deployment (static hosting)

**Choose Next.js** when you need:
- 🔍 SEO optimization (server-side rendering)
- 📄 Multi-page routing with App Router
- 🌐 Edge functions and middleware
- 📊 Complex server-side logic
- 🏢 Enterprise features (ISR, etc.)

### Vite + ADK Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Vite Dev Server (Port 5173)                         │  │
│  │  ├─ React 18 SPA                                     │  │
│  │  ├─ `<CopilotKit>` provider                           │  │
│  │  ├─ Hot Module Replacement (HMR)                    │  │
│  │  └─ Instant updates                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Vite Proxy → AG-UI Protocol
                        │
┌───────────────────────▼─────────────────────────────────────┐
│            BACKEND SERVER (Port 8000)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI + ag_ui_adk (AG-UI middleware)              │  │
│  │  ├─ ADKAgent → LlmAgent (gemini-2.5-flash)           │  │
│  │  ├─ pandas tools (3 functions)                       │  │
│  │  └─ In-memory file storage                           │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┴─────────────────────────────────────┘
```

**Key Difference from Next.js**:
- Vite uses **proxy configuration** instead of API routes
- Backend runs separately (same as Next.js pattern)
- Frontend is pure SPA (no server-side rendering)

---

## Quick Start (5 Minutes)

### Step 1: Create Vite Project

```bash
# Create Vite + React + TypeScript project
npm create vite@latest data-dashboard -- --template react-ts

cd data-dashboard

# Install CopilotKit
npm install @copilotkit/react-core @copilotkit/react-ui

# Install additional dependencies
npm install chart.js react-chartjs-2 papaparse
npm install -D @types/papaparse

npm install
```

### Step 2: Configure Vite Proxy

Update `vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API requests to backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

**What this does**:
- Requests to `http://localhost:5173/api/copilotkit` → `http://localhost:8000/copilotkit`
- Avoids CORS issues during development
- Clean separation of concerns

### Step 3: Create Data Analysis Agent

Create `agent/agent.py`:

```python
"""Data analysis ADK agent with pandas tools."""

import os
import io
import json
import pandas as pd
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Google ADK imports  
from google.adk.agents import Agent

load_dotenv()

# In-memory data storage (use Redis/DB in production)
uploaded_data = {}

def load_csv_data(file_name: str, csv_content: str) -> Dict[str, Any]:
    """
    Load CSV data into memory for analysis.
    
    Args:
        file_name: Name of the CSV file
        csv_content: CSV file content as string
        
    Returns:
        Dict with dataset info and preview
    """
    try:
        # Parse CSV
        df = pd.read_csv(io.StringIO(csv_content))
        
        # Store in memory
        uploaded_data[file_name] = df
        
        # Return summary
        return {
            "status": "success",
            "file_name": file_name,
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(5).to_dict(orient='records'),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def analyze_data(
    file_name: str,
    analysis_type: str,
    columns: List[str] = None
) -> Dict[str, Any]:
    """
    Perform analysis on loaded dataset.
    
    Args:
        file_name: Name of dataset to analyze
        analysis_type: Type of analysis (summary, correlation, trend)
        columns: Optional list of columns to analyze
        
    Returns:
        Dict with analysis results
    """
    if file_name not in uploaded_data:
        return {"status": "error", "error": f"Dataset {file_name} not found"}
    
    df = uploaded_data[file_name]
    
    if columns:
        df = df[columns]
    
    results = {
        "status": "success",
        "file_name": file_name,
        "analysis_type": analysis_type
    }
    
    if analysis_type == "summary":
        results["data"] = {
            "describe": df.describe().to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "unique": df.nunique().to_dict()
        }
    
    elif analysis_type == "correlation":
        # Only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        results["data"] = numeric_df.corr().to_dict()
    
    elif analysis_type == "trend":
        # Time series analysis
        if len(df) > 0:
            numeric_df = df.select_dtypes(include=['number'])
            results["data"] = {
                "mean": numeric_df.mean().to_dict(),
                "trend": "upward" if numeric_df.iloc[-1].sum() > numeric_df.iloc[0].sum() else "downward"
            }
    
    return results

def create_chart(
    file_name: str,
    chart_type: str,
    x_column: str,
    y_column: str
) -> Dict[str, Any]:
    """
    Generate chart data for visualization.
    
    Args:
        file_name: Name of dataset
        chart_type: Type of chart (line, bar, scatter)
        x_column: Column for x-axis
        y_column: Column for y-axis
        
    Returns:
        Dict with chart configuration
    """
    if file_name not in uploaded_data:
        return {"status": "error", "error": f"Dataset {file_name} not found"}
    
    df = uploaded_data[file_name]
    
    if x_column not in df.columns or y_column not in df.columns:
        return {"status": "error", "error": "Invalid columns"}
    
    # Prepare chart data
    chart_data = {
        "status": "success",
        "chart_type": chart_type,
        "data": {
            "labels": df[x_column].tolist(),
            "values": df[y_column].tolist()
        },
        "options": {
            "x_label": x_column,
            "y_label": y_column,
            "title": f"{y_column} vs {x_column}"
        }
    }
    
    return chart_data

# Create ADK agent using the new API
adk_agent = Agent(
    name="data_analyst",
    model="gemini-2.5-flash",  # or "gemini-2.0-flash-exp"
    instruction="""You are a data analysis expert assistant.

Your capabilities:
- Load and analyze CSV datasets using load_csv_data()
- Perform statistical analysis using analyze_data()
- Generate insights and trends
- Create visualizations using create_chart()

Guidelines:
- Always start by loading data if not already loaded
- Explain your analysis clearly with markdown formatting
- Suggest relevant visualizations
- Highlight key insights with **bold** text
- Use statistical terms appropriately

When analyzing data:
1. Understand the dataset structure first
2. Perform appropriate analysis (summary, correlation, or trend)
3. Generate visualizations if helpful
4. Provide actionable insights

Be concise but thorough in your explanations.""",
    tools=[load_csv_data, analyze_data, create_chart]
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="data_analysis_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="Data Analysis Agent API")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
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
        "agent": "data_analyst",
        "datasets_loaded": list(uploaded_data.keys())
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

Create `agent/requirements.txt`:

```text
google-genai>=1.15.0
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
ag_ui_adk>=0.1.0
python-dotenv>=1.0.0
pandas>=2.0.0
```

Create `agent/.env`:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Step 4: Create React Frontend

Update `src/App.tsx`:

```typescript
import { useState } from 'react'
import { CopilotKit } from "@copilotkit/react-core"
import { CopilotChat } from "@copilotkit/react-ui"
import "@copilotkit/react-ui/styles.css"
import './App.css'

function App() {
  const [uploadedFile, setUploadedFile] = useState<string | null>(null)

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = async (e) => {
      const content = e.target?.result as string
      setUploadedFile(file.name)
      
      // File content will be passed to agent via chat
      console.log(`Loaded ${file.name}: ${content.length} bytes`)
    }
    reader.readAsText(file)
  }

  return (
    <div className="app-container">
      <CopilotKit runtimeUrl="/api/copilotkit">
        <div className="dashboard">
          {/* Header */}
          <header className="header">
            <h1>📊 Data Analysis Dashboard</h1>
            <p>Upload CSV data and ask questions to get insights</p>
          </header>

          {/* File Upload */}
          <div className="upload-section">
            <label htmlFor="file-upload" className="upload-button">
              📁 Upload CSV File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".csv"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
            />
            {uploadedFile && (
              <span className="file-name">✅ {uploadedFile}</span>
            )}
          </div>

          {/* Chat Interface */}
          <div className="chat-container">
            <CopilotChat
              instructions="You are a data analysis assistant. Help users analyze their CSV data."
              labels={{
                title: "Data Analyst",
                initial: "Hi! Upload a CSV file and I'll help you analyze it. You can ask me to:\n\n• Summarize the data\n• Find correlations\n• Identify trends\n• Create visualizations",
              }}
            />
          </div>
        </div>
      </CopilotKit>
    </div>
  )
}

export default App
```

Update `src/App.css`:

```css
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.upload-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.upload-button {
  display: inline-block;
  padding: 1rem 2rem;
  background: #667eea;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.upload-button:hover {
  background: #764ba2;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.file-name {
  margin-left: 1rem;
  color: #28a745;
  font-weight: 600;
}

.chat-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  height: 600px;
}
```

### Step 5: Run Everything

```bash
# Terminal 1: Run agent
cd agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python agent.py

# Terminal 2: Run Vite frontend
cd ..
npm run dev
```

**Open http://localhost:5173** - Your data analysis dashboard is live! 🎉

**Try it**:
1. Upload a CSV file (sales data, etc.)
2. Ask: "What are the key statistics?"
3. Ask: "Show me a chart of sales over time"
4. Watch the agent analyze and visualize your data!

---

## Building a Data Analysis Dashboard

Let's enhance our dashboard with real data visualization.

### Feature 1: Interactive Charts

Install Chart.js:

```bash
npm install chart.js react-chartjs-2
```

Create `src/components/ChartRenderer.tsx`:

```typescript
import { Line, Bar, Scatter } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface ChartData {
  chart_type: string
  data: {
    labels: string[]
    values: number[]
  }
  options: {
    x_label: string
    y_label: string
    title: string
  }
}

interface ChartRendererProps {
  chartData: ChartData
}

export function ChartRenderer({ chartData }: ChartRendererProps) {
  const data = {
    labels: chartData.data.labels,
    datasets: [
      {
        label: chartData.options.y_label,
        data: chartData.data.values,
        backgroundColor: 'rgba(102, 126, 234, 0.5)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
      },
    ],
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: chartData.options.title,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: chartData.options.x_label,
        },
      },
      y: {
        title: {
          display: true,
          text: chartData.options.y_label,
        },
      },
    },
  }

  // Render appropriate chart type
  switch (chartData.chart_type) {
    case 'line':
      return <Line data={data} options={options} />
    case 'bar':
      return <Bar data={data} options={options} />
    case 'scatter':
      return <Scatter data={data} options={options} />
    default:
      return <div>Unsupported chart type: {chartData.chart_type}</div>
  }
}
```

### Feature 2: Generative UI for Charts

Register chart rendering with CopilotKit:

```typescript
import { useCopilotAction } from "@copilotkit/react-core"
import { ChartRenderer } from './components/ChartRenderer'

// In App component
useCopilotAction({
  name: "render_chart",
  description: "Render a data visualization chart",
  parameters: [
    {
      name: "chartData",
      type: "object",
      description: "Chart configuration and data"
    }
  ],
  handler: async ({ chartData }) => {
    // Render chart as generative UI
    return <ChartRenderer chartData={chartData} />
  }
})
```

Now when the agent calls `create_chart()`, beautiful charts render inline! 📊

### Feature 3: Data Table View

Create `src/components/DataTable.tsx`:

```typescript
interface DataTableProps {
  data: Array<Record<string, any>>
  columns: string[]
}

export function DataTable({ data, columns }: DataTableProps) {
  return (
    <div className="data-table-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={col}>{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

Add CSS in `src/App.css`:

```css
.data-table-container {
  max-height: 400px;
  overflow: auto;
  margin: 1rem 0;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #667eea;
  color: white;
  position: sticky;
  top: 0;
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.data-table tbody tr:hover {
  background: #f5f5f5;
}
```

### Feature 4: Export Analysis Report

Add export functionality:

```typescript
const exportAnalysis = () => {
  // Collect all analysis results
  const report = {
    timestamp: new Date().toISOString(),
    file: uploadedFile,
    analysis: "... collected from agent responses ...",
    charts: "... chart configurations ..."
  }

  // Convert to JSON
  const blob = new Blob([JSON.stringify(report, null, 2)], {
    type: 'application/json'
  })

  // Download
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `analysis_${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
}

// Add button to UI
<button onClick={exportAnalysis} className="export-button">
  📥 Export Report
</button>
```

---

## Advanced Features

### Feature 1: Real-Time Collaboration

Share dashboard state across users:

```typescript
import { useCopilotReadable } from "@copilotkit/react-core"

function App() {
  const [sharedState, setSharedState] = useState({
    uploadedFiles: [],
    currentAnalysis: null,
    collaborators: []
  })

  // Make state readable by agent
  useCopilotReadable({
    description: "Current dashboard state",
    value: sharedState
  })

  // Agent can now see what files are loaded, what analysis is active, etc.
}
```

### Feature 2: Agent Memory

Persist analysis history:

```typescript
const [analysisHistory, setAnalysisHistory] = useState<Analysis[]>([])

useCopilotAction({
  name: "save_analysis",
  description: "Save analysis to history",
  parameters: [
    {
      name: "analysis",
      type: "object",
      description: "Analysis results to save"
    }
  ],
  handler: async ({ analysis }) => {
    setAnalysisHistory(prev => [...prev, analysis])
    localStorage.setItem('analysis_history', JSON.stringify([...analysisHistory, analysis]))
    return { status: "saved" }
  }
})
```

### Feature 3: Multi-File Analysis

Compare multiple datasets:

```python
# In agent.py
def compare_datasets(
    file_names: List[str],
    metric: str
) -> Dict[str, Any]:
    """Compare metric across multiple datasets."""
    comparison = {}
    
    for name in file_names:
        if name in uploaded_data:
            df = uploaded_data[name]
            if metric in df.columns:
                comparison[name] = df[metric].mean()
    
    return {
        "status": "success",
        "comparison": comparison,
        "winner": max(comparison, key=comparison.get) if comparison else None
    }
```

---

## Production Deployment

### Option 1: Deploy to Netlify

**Step 1: Build Frontend**

```bash
# Create production build
npm run build

# Output in dist/ directory
```

**Step 2: Deploy Agent to Cloud Run**

```bash
# Deploy agent (same as Tutorial 30)
cd agent
gcloud run deploy data-analysis-agent \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_key"

# Get URL: https://data-analysis-agent-xyz.run.app
```

**Step 3: Update Frontend for Production**

Create `src/config.ts`:

```typescript
export const API_URL = import.meta.env.PROD
  ? 'https://data-analysis-agent-xyz.run.app'
  : '/api'
```

Update `src/App.tsx`:

```typescript
import { API_URL } from './config'

<CopilotKit runtimeUrl={`${API_URL}/copilotkit`}>
```

**Step 4: Deploy to Netlify**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod --dir=dist

# Or connect GitHub repo for auto-deploy
netlify init
```

**Done!** Your app is live at `https://data-dashboard-xyz.netlify.app` 🚀

---

### Option 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variable
vercel env add VITE_API_URL production
# Enter: https://data-analysis-agent-xyz.run.app

# Redeploy with env
vercel --prod
```

**Done!** Your app is live at `https://data-dashboard.vercel.app` 🎉

---

## Vite vs Next.js Comparison

### Development Experience

| Aspect | Vite | Next.js 15 |
|--------|------|------------|
| **Cold Start** | &lt;1s | 3-5s |
| **HMR Speed** | &lt;50ms | 200-500ms |
| **Build Time** | 10-30s | 30-120s |
| **Bundle Size** | 100-200KB | 200-400KB |
| **Config** | Simple | Complex |

### Feature Comparison

| Feature | Vite | Next.js 15 |
|---------|------|------------|
| **SPA Support** | ✅ Native | ✅ Via export |
| **SSR** | ⚠️ Manual (Vite SSR) | ✅ Built-in |
| **API Routes** | ❌ Proxy only | ✅ Full support |
| **File Routing** | ❌ Manual | ✅ Built-in |
| **Image Optimization** | ❌ Manual | ✅ Built-in |
| **Middleware** | ❌ None | ✅ Edge runtime |
| **Static Export** | ✅ Native | ✅ Built-in |
| **Hot Reload** | ✅ Lightning fast | ✅ Good |

### When to Use Each

**Use Vite** for:
- ⚡ Prototypes and MVPs
- 🎨 Dashboards and admin panels
- 📊 Data visualization tools
- 🔧 Internal tools
- 📱 SPAs without SEO needs
- 🚀 Fast iteration needed

**Use Next.js** for:
- 🔍 SEO-critical sites
- 📄 Multi-page websites
- 🌐 Public-facing apps
- 🏢 Enterprise applications
- 📊 Complex routing needs
- 🔐 Server-side auth

### Code Comparison

**Vite** (Simple):
```typescript
// Single file, straightforward
import { CopilotKit } from "@copilotkit/react-core"

<CopilotKit runtimeUrl="/api/copilotkit">
  <App />
</CopilotKit>
```

**Next.js** (Structured):
```typescript
// app/layout.tsx - Layout wrapper
// app/page.tsx - Main page
// app/api/copilotkit/route.ts - API route

// More structure, more power
```

---

## Troubleshooting

### Issue 1: Proxy Not Working

**Symptoms**:
- 404 errors on `/api/copilotkit`
- Agent not receiving requests

**Solution**:

```typescript
// vite.config.ts - Check proxy config
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, options) => {
          // Log proxy requests for debugging
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Proxying:', req.method, req.url, '→', proxyReq.path)
          })
        }
      }
    }
  }
})
```

---

### Issue 2: CORS in Production

**Symptoms**:
- Works locally, fails in production
- CORS errors in browser console

**Solution**:

```python
# agent/agent.py - Update CORS for production
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://data-dashboard.netlify.app",  # Your Netlify domain
        "https://data-dashboard.vercel.app",   # Your Vercel domain
        "http://localhost:5173",  # Local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Issue 3: Large File Upload Issues

**Symptoms**:
- Upload fails for files >1MB
- Timeout errors

**Solution**:

```python
# agent/agent.py - Increase limits
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# Increase body size limit
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Handle large files
    content = await file.read()
    return {"size": len(content)}

# In uvicorn startup
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    limit_concurrency=100,
    limit_max_requests=1000,
    timeout_keep_alive=30
)
```

---

### Issue 4: Chart Not Rendering

**Symptoms**:
- Chart data received but nothing displays
- Console errors about Chart.js

**Solution**:

```typescript
// Make sure Chart.js is registered
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

// MUST register before using
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)
```

---

## Next Steps

### You've Mastered Vite + ADK! 🎉

You now know how to:

✅ Build lightning-fast React + Vite + ADK apps  
✅ Create data analysis dashboards  
✅ Implement generative UI with Chart.js  
✅ Handle file uploads and processing  
✅ Deploy to Netlify or Vercel  
✅ Compare Vite vs Next.js approaches  

### Continue Learning

**Tutorial 32**: Streamlit + ADK Integration  
Build data apps with pure Python (no frontend code!)

**Tutorial 33**: Slack Bot Integration  
Create team collaboration bots for Slack

**Tutorial 35**: AG-UI Deep Dive  
Master advanced features: multi-agent UI, custom protocols

### Additional Resources

- [Vite Documentation](https://vitejs.dev/)
- [CopilotKit + Vite Guide](https://docs.copilotkit.ai/guides/vite)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Example: gemini-fullstack](https://github.com/google/adk-samples/tree/main/gemini-fullstack)

---

**🎉 Tutorial 31 Complete!**

**Next**: [Tutorial 32: Streamlit + ADK Integration](./32_streamlit_adk_integration.md)

---

**Questions or feedback?** Open an issue on the [ADK Training Repository](https://github.com/google/adk-training).
