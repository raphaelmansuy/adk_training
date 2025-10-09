---
id: nextjs_adk_integration
title: "Tutorial 30: Next.js ADK Integration - React Chat Interfaces"
description: "Build modern chat interfaces using Next.js and CopilotKit to create seamless React-based agent interactions with real-time features."
sidebar_label: "30. Next.js ADK Integration"
sidebar_position: 30
tags: ["ui", "nextjs", "react", "copilotkit", "chat-interface"]
keywords:
  [
    "nextjs",
    "react",
    "copilotkit",
    "chat interface",
    "ui integration",
    "web interface",
  ]
status: "draft"
difficulty: "intermediate"
estimated_time: "2 hours"
prerequisites:
  [
    "Tutorial 01: Hello World Agent",
    "React/Next.js experience",
    "Node.js setup",
  ]
learning_objectives:
  - "Build Next.js chat interfaces with CopilotKit"
  - "Integrate ADK agents with React components"
  - "Create real-time agent interactions"
  - "Deploy agent-powered web applications"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial30"
---

:::danger UNDER CONSTRUCTION

**This tutorial is currently under construction and may contain errors, incomplete information, or outdated code examples.**

Please check back later for the completed version. If you encounter issues, refer to the working implementation in the [tutorial repository](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial30).

## :::

# Tutorial 30: Next.js 15 + ADK Integration (AG-UI Protocol)

**Estimated Reading Time**: 65-75 minutes  
**Difficulty Level**: Intermediate  
**Prerequisites**: Tutorial 29 (UI Integration Intro), Tutorial 1-3 (ADK Basics), Basic Next.js knowledge

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites & Setup](#prerequisites--setup)
3. [Quick Start (10 Minutes)](#quick-start-10-minutes)
4. [Understanding the Architecture](#understanding-the-architecture)
5. [Building a Customer Support Agent](#building-a-customer-support-agent)
6. [Advanced Features](#advanced-features)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Overview

### What You'll Build

In this tutorial, you'll build a **production-ready customer support chatbot** using:

- **Next.js 15** (App Router)
- **CopilotKit** (AG-UI Protocol)
- **Google ADK** (Agent backend)
- **Gemini 2.0 Flash** (LLM)

**Final Result**:

```text
┌─────────────────────────────────────────────────────────────┐
│  Customer Support Chatbot                                   │
│  ├─ Real-time chat interface                                │
│  ├─ Tool-augmented responses (knowledge base search)        │
│  ├─ Streaming responses                                     │
│  ├─ Session persistence                                     │
│  ├─ Production deployment (Vercel + Cloud Run)              │
│  └─ 99.9% uptime capability                                 │
└─────────────────────────────────────────────────────────────┘
```

### Why Next.js 15 + ADK?

| Feature                   | Benefit                                         |
| ------------------------- | ----------------------------------------------- |
| **Next.js 15 App Router** | Server Components, streaming, optimized routing |
| **CopilotKit/AG-UI**      | Pre-built chat UI, type-safe integration        |
| **Google ADK**            | Powerful agent framework with tool calling      |
| **Gemini 2.0 Flash**      | Fast, cost-effective, state-of-the-art LLM      |
| **Vercel + Cloud Run**    | Scalable, global deployment                     |

---

## Prerequisites & Setup

### System Requirements

```bash
# Node.js 18.17 or later
node --version  # Should be >= 18.17

# Python 3.9 or later
python --version  # Should be >= 3.9

# npm/pnpm/yarn
npm --version  # Any version
```

### API Keys

**1. Google AI API Key**

Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey):

```bash
export GOOGLE_API_KEY="your_gemini_api_key_here"
```

**2. (Optional) Vercel Account**

For deployment: [Sign up at Vercel](https://vercel.com)

---

## Quick Start (10 Minutes)

### Option 1: Use CopilotKit CLI (Recommended)

The fastest way to get started:

```bash
# Create new project with ADK template
npx copilotkit@latest create -f adk

# Follow prompts:
# ✓ Project name: customer-support-bot
# ✓ Include ADK agent: Yes
# ✓ Include frontend: Yes (Next.js)

cd customer-support-bot

# Install dependencies (includes Python agent deps)
npm install

# Set API key
export GOOGLE_API_KEY="your_api_key"
# Or create agent/.env:
echo "GOOGLE_API_KEY=your_api_key" > agent/.env

# Run both frontend and agent together!
npm run dev
```

**Open http://localhost:3000** - Your agent is live! 🎉

**What just happened?**

- ✅ Created Next.js 15 app with App Router
- ✅ Installed CopilotKit frontend packages
- ✅ Created Python ADK agent in `agent/` directory
- ✅ Configured bidirectional communication (AG-UI Protocol)
- ✅ Set up hot reloading for both frontend and backend

---

### Option 2: Manual Setup (Full Control)

Want to understand every piece? Build from scratch:

**Step 1: Create Next.js App**

```bash
npx create-next-app@latest customer-support-bot
# ✓ TypeScript: Yes
# ✓ ESLint: Yes
# ✓ Tailwind CSS: Yes
# ✓ App Router: Yes
# ✓ import alias: No

cd customer-support-bot
```

**Step 2: Install CopilotKit**

```bash
npm install @copilotkit/react-core @copilotkit/react-ui
```

**Step 3: Create Agent Directory**

```bash
mkdir agent
cd agent

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install ADK and dependencies
pip install google-genai fastapi uvicorn ag_ui_adk

# Create requirements.txt
cat > requirements.txt << EOF
google-genai>=1.15.0
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
ag_ui_adk>=0.1.0
python-dotenv>=1.0.0
EOF
```

**Step 4: Create Agent**

Create `agent/agent.py`:

```python
"""Customer support ADK agent with AG-UI integration."""

import os
from typing import Dict
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Google ADK imports
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

# Define knowledge base search tool
def search_knowledge_base(query: str) -> str:
    """
    Search the knowledge base for relevant information.

    Args:
        query: Search query to find relevant articles

    Returns:
        Formatted string with article title and content
    """
    # Mock knowledge base - replace with real database/vector store
    knowledge_base = {
        "refund policy": {
            "title": "Refund Policy",
            "content": "We offer full refunds within 30 days of purchase. " +
                      "Contact support@company.com to initiate a refund."
        },
        "shipping": {
            "title": "Shipping Information",
            "content": "Standard shipping takes 5-7 business days. " +
                      "Express shipping (2-3 days) available for $15 extra."
        },
        "warranty": {
            "title": "Warranty Coverage",
            "content": "All products include 1-year warranty covering " +
                      "manufacturing defects. Extended warranty available."
        },
        "account": {
            "title": "Account Management",
            "content": "Reset password at /account/reset. Update billing " +
                      "info at /account/billing. Cancel subscription anytime."
        }
    }

    # Simple keyword matching - use vector search in production
    query_lower = query.lower()
    for key, article in knowledge_base.items():
        if key in query_lower:
            return f"**{article['title']}**\n\n{article['content']}"

    # Default response
    return ("**General Support**\n\n"
            "Please contact our support team at support@company.com "
            "or call 1-800-SUPPORT for personalized assistance.")


def lookup_order_status(order_id: str) -> str:
    """
    Look up the status of a customer order.

    Args:
        order_id: The order ID to look up

    Returns:
        Order status information
    """
    # Mock order database - replace with real database
    orders = {
        "ORD-12345": "Shipped - Arriving tomorrow",
        "ORD-67890": "Processing - Ships in 2-3 days",
        "ORD-11111": "Delivered on Jan 15, 2024"
    }

    if order_id.upper() in orders:
        return f"Order {order_id}: {orders[order_id.upper()]}"
    return f"Order {order_id} not found. Please check the order ID and try again."


def create_support_ticket(issue_description: str, priority: str = "normal") -> str:
    """
    Create a support ticket for complex issues.

    Args:
        issue_description: Description of the customer's issue
        priority: Priority level (low, normal, high, urgent)

    Returns:
        Ticket confirmation with ticket ID
    """
    import uuid
    ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"

    return (f"Support ticket created successfully!\n\n"
            f"**Ticket ID:** {ticket_id}\n"
            f"**Priority:** {priority}\n"
            f"**Issue:** {issue_description}\n\n"
            f"Our support team will contact you within 24 hours.")


# Create ADK agent with tools using the new API
adk_agent = Agent(
    name="customer_support_agent",
    model="gemini-2.5-flash",  # or "gemini-2.0-flash-exp"
    instruction="""You are a helpful customer support agent for an e-commerce company.

Your responsibilities:
- Answer customer questions clearly and concisely
- Search the knowledge base when needed using search_knowledge_base()
- Look up order status using lookup_order_status() when customers ask about their orders
- Create support tickets using create_support_ticket() for complex issues
- Be empathetic and professional
- Escalate complex issues to human support when appropriate
- Never make up information - if unsure, say so

Guidelines:
- Greet customers warmly
- Use the appropriate tool for each type of query
- Offer next steps after answering
- Keep responses under 3 paragraphs unless more detail is requested
- Use a friendly but professional tone
- Format responses with markdown for better readability""",
    tools=[search_knowledge_base, lookup_order_status, create_support_ticket]
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="customer_support_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="Customer Support Agent API")

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
    return {"status": "healthy", "agent": "customer_support_agent"}

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

**Create `agent/.env`**:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Step 5: Create Frontend**

Update `app/layout.tsx`:

```typescript
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Customer Support Chat",
  description: "AI-powered customer support powered by Google ADK",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

Create `app/page.tsx`:

```typescript
"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <CopilotKit runtimeUrl="http://localhost:8000/copilotkit">
        {/* Header */}
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Customer Support
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Hi! I'm your AI support assistant. How can I help you today?
            </p>
          </div>
        </div>

        {/* Chat Interface */}
        <div className="container mx-auto px-4 pb-8">
          <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl overflow-hidden">
            <CopilotChat
              instructions="You are a customer support agent. Be helpful, empathetic, and professional."
              labels={{
                title: "Support Chat",
                initial: "Hi! I'm here to help with your questions about our products, policies, and services. What can I assist you with today?",
              }}
              className="h-[600px]"
            />
          </div>
        </div>
      </CopilotKit>
    </div>
  );
}
```

**Step 6: Run Everything**

```bash
# Terminal 1: Run agent
cd agent
source venv/bin/activate
python agent.py

# Terminal 2: Run Next.js
cd ..
npm run dev
```

**Open http://localhost:3000** - Your custom support agent is live! 🚀

---

## Understanding the Architecture

### Component Diagram

```text
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Next.js 15 App (Port 3000)                          │  │
│  │  ├─ app/page.tsx                                     │  │
│  │  │  └─ <CopilotKit> provider                        │  │
│  │  │     └─ <CopilotChat> component                   │  │
│  │  │                                                    │  │
│  │  └─ @copilotkit/react-core (TypeScript SDK)         │  │
│  │     ├─ WebSocket connection                          │  │
│  │     ├─ Message streaming                             │  │
│  │     └─ State management                              │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ AG-UI Protocol (WebSocket/SSE)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│            BACKEND SERVER (Port 8000)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  ag_ui_adk (AG-UI Middleware)                        │  │
│  │  ├─ FastAPI app                                      │  │
│  │  ├─ /api/copilotkit endpoint                         │  │
│  │  ├─ AG-UI protocol adapter                           │  │
│  │  └─ Session management                               │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │  ADKAgent (wrapper)                                  │  │
│  │  ├─ app_name: "customer_support_app"                 │  │
│  │  ├─ user_id & session management                     │  │
│  │  └─ Wraps LlmAgent                                   │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │  Google ADK LlmAgent                                 │  │
│  │  ├─ model: "gemini-2.5-flash"                        │  │
│  │  ├─ instruction: System prompt                       │  │
│  │  └─ tools: [search_knowledge_base, lookup_order,    │  │
│  │            create_support_ticket]                    │  │
│  └──────────────────────┬───────────────────────────────┘  │
└───────────────────────┬─┴───────────────────────────────────┘
                        │
                        │ Gemini API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              GEMINI 2.0 FLASH                                │
│  ├─ Text generation                                          │
│  ├─ Function calling                                         │
│  └─ Streaming responses                                      │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

**1. User sends message**: "What's your refund policy?"

**2. Frontend** (`<CopilotChat>`):

```typescript
// Message sent via WebSocket
{
  type: "textMessage",
  content: "What's your refund policy?",
  sessionId: "user-123"
}
```

**3. AG-UI Middleware** (ag_ui_adk):

```python
# ADKAgent wraps your LlmAgent
# Translates AG-UI Protocol → ADK format
# Manages sessions with timeout
# Handles tool execution
# add_adk_fastapi_endpoint() creates /api/copilotkit endpoint
```

**4. ADK Agent**:

```python
# Agent processes message
# Decides to call search_knowledge_base tool
# Executes tool with query="refund policy"
# Generates response with knowledge base result
```

**5. Gemini 2.0 Flash**:

```text
System: You are a customer support agent...
User: What's your refund policy?
Function Call: search_knowledge_base(query="refund policy")
Function Result: {"title": "Refund Policy", "content": "We offer..."}
Agent: "Our refund policy is...
```

**6. Response streams back**:

```typescript
// Frontend receives chunks
{
  type: "textMessageChunk",
  content: "Our refund policy"
}
{
  type: "textMessageChunk",
  content: " is very customer-friendly..."
}
```

**7. User sees response** progressively rendering in real-time!

---

## Building a Customer Support Agent

### Enhancing the Agent

Let's add more realistic features to our support agent.

#### Feature 1: Order Status Lookup

Update `agent/agent.py`:

```python
def lookup_order_status(order_id: str) -> Dict[str, str]:
    """
    Look up the status of an order.

    Args:
        order_id: The order ID to look up (format: ORD-XXXXX)

    Returns:
        Dict with order status details
    """
    # Mock order database - replace with real database
    orders = {
        "ORD-12345": {
            "status": "Shipped",
            "tracking": "1Z999AA10123456784",
            "estimated_delivery": "2025-10-12",
            "items": "2x Widget Pro, 1x Gadget Plus"
        },
        "ORD-67890": {
            "status": "Processing",
            "tracking": None,
            "estimated_delivery": "2025-10-15",
            "items": "1x Premium Kit"
        }
    }

    order_id_upper = order_id.upper()

    if order_id_upper in orders:
        return orders[order_id_upper]
    else:
        return {
            "status": "Not Found",
            "message": f"Order {order_id} not found. Please check the order ID and try again."
        }

# Add to agent tools - note: for testing purposes, showing function reference
# In actual implementation, tools are added to Agent constructor
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash-exp",
    name="customer_support_agent",
    instruction="""...""",  # Same as before
    tools=[lookup_order_status]  # Add function directly
)

# If using genai.Tool for testing:
# Tool(
#     function_declarations=[
#         # ... search_knowledge_base (as before)
                FunctionDeclaration(
                    name="lookup_order_status",
                    description="Look up the status and tracking information for a customer order",
                    parameters={
                        "type": "object",
                        "properties": {
                            "order_id": {
                                "type": "string",
                                "description": "The order ID in format ORD-XXXXX"
                            }
                        },
                        "required": ["order_id"]
                    }
                )
            ]
        )
    ],
    tool_config={"function_calling_config": {"mode": "AUTO"}}
)

# Update runtime tools
app = create_copilotkit_runtime(
    agent=agent,
    tools={
        "search_knowledge_base": search_knowledge_base,
        "lookup_order_status": lookup_order_status
    }
)
```

**Test it**:

User: "What's the status of my order ORD-12345?"

Agent: "Your order ORD-12345 has been shipped! Here are the details:

- Status: Shipped
- Tracking: 1Z999AA10123456784
- Estimated Delivery: October 12, 2025
- Items: 2x Widget Pro, 1x Gadget Plus

You can track your package using the tracking number above. Is there anything else I can help you with?"

---

#### Feature 2: Create Support Ticket

Add escalation capability:

```python
import uuid
from datetime import datetime

def create_support_ticket(
    issue_type: str,
    description: str,
    priority: str = "normal"
) -> Dict[str, str]:
    """
    Create a support ticket for issues that need human attention.

    Args:
        issue_type: Type of issue (billing, technical, account, other)
        description: Detailed description of the issue
        priority: Priority level (low, normal, high, urgent)

    Returns:
        Dict with ticket ID and estimated response time
    """
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"

    # Mock ticket creation - replace with real ticketing system API
    response_times = {
        "urgent": "1-2 hours",
        "high": "4-6 hours",
        "normal": "12-24 hours",
        "low": "24-48 hours"
    }

    return {
        "ticket_id": ticket_id,
        "status": "Created",
        "priority": priority,
        "estimated_response": response_times.get(priority, "24 hours"),
        "created_at": datetime.now().isoformat(),
        "message": f"Ticket {ticket_id} created successfully. Our support team will reach out within {response_times.get(priority)}."
    }

# Add to tools
FunctionDeclaration(
    name="create_support_ticket",
    description="Create a support ticket for complex issues that need human agent attention",
    parameters={
        "type": "object",
        "properties": {
            "issue_type": {
                "type": "string",
                "description": "Type of issue",
                "enum": ["billing", "technical", "account", "other"]
            },
            "description": {
                "type": "string",
                "description": "Detailed description of the issue"
            },
            "priority": {
                "type": "string",
                "description": "Priority level",
                "enum": ["low", "normal", "high", "urgent"],
                "default": "normal"
            }
        },
        "required": ["issue_type", "description"]
    }
)

# Update runtime
app = create_copilotkit_runtime(
    agent=agent,
    tools={
        "search_knowledge_base": search_knowledge_base,
        "lookup_order_status": lookup_order_status,
        "create_support_ticket": create_support_ticket
    }
)
```

**Test it**:

User: "My product stopped working after 2 months and warranty doesn't seem to cover it"

Agent: "I understand how frustrating that must be. Let me create a support ticket for our specialist team to review your warranty coverage.

_Creates ticket TKT-A1B2C3D4_

I've created ticket TKT-A1B2C3D4 for you with high priority. Our specialized support team will reach out within 4-6 hours to review your case and warranty details.

In the meantime, have you tried:

- Checking if firmware updates are available
- Performing a factory reset (if applicable)

Is there anything else I can help you with while you wait?"

---

### Adding Personality & Context

Make your agent more engaging:

```python
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash-exp",
    name="customer_support_agent",
    instruction="""You are Jamie, a friendly and knowledgeable customer support agent for TechCo, an e-commerce company selling electronics and gadgets.

Your personality:
- Warm and empathetic, but professional
- Patient and understanding with frustrated customers
- Enthusiastic about helping solve problems
- Use occasional (appropriate) emojis to be friendly 😊
- Remember context from the conversation

Your responsibilities:
1. Answer product and policy questions using the knowledge base
2. Look up order status when customers provide order IDs
3. Create support tickets for complex issues
4. Escalate urgent problems immediately
5. Never make up information - if unsure, check knowledge base or create ticket

Guidelines:
- Greet returning customers warmly
- Acknowledge frustration with empathy
- Offer proactive solutions
- End with "Is there anything else I can help with?"
- Keep responses concise but complete
- Use bullet points for clarity

Company values:
- Customer satisfaction is our top priority
- We stand behind our products
- Transparency in all communications

Remember: You represent TechCo's commitment to excellent customer service!""",
    tools=[...],  # Same tools as before
    tool_config={"function_calling_config": {"mode": "AUTO"}}
)
```

---

## Advanced Features

### Feature 1: Generative UI

Render custom React components from agent responses.

**Backend** (`agent/agent.py`):

```python
def create_product_card(product_id: str) -> Dict:
    """Generate a product card with details."""
    # Mock product data
    products = {
        "PROD-001": {
            "name": "Widget Pro",
            "price": 99.99,
            "image": "/products/widget-pro.jpg",
            "rating": 4.5,
            "inStock": True
        }
    }

    product = products.get(product_id, {})

    # Return structured data for generative UI
    return {
        "component": "ProductCard",
        "props": product
    }

# Agent can now return:
# "Here's the product you asked about: {PRODUCT_CARD:PROD-001}"
```

**Frontend** - Create `app/components/ProductCard.tsx`:

```typescript
import Image from "next/image";

interface ProductCardProps {
  name: string;
  price: number;
  image: string;
  rating: number;
  inStock: boolean;
}

export function ProductCard(props: ProductCardProps) {
  return (
    <div className="border rounded-lg p-4 bg-white shadow-sm">
      <Image
        src={props.image}
        alt={props.name}
        width={200}
        height={200}
        className="rounded-md mb-3"
      />
      <h3 className="font-semibold text-lg">{props.name}</h3>
      <div className="flex items-center gap-2 mt-2">
        <span className="text-2xl font-bold text-green-600">
          ${props.price}
        </span>
        <span className="text-yellow-500">⭐ {props.rating}</span>
      </div>
      {props.inStock ? (
        <span className="inline-block mt-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
          In Stock
        </span>
      ) : (
        <span className="inline-block mt-2 px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">
          Out of Stock
        </span>
      )}
    </div>
  );
}
```

Register component with CopilotKit:

```typescript
import { useCopilotAction, renderCopilotComponent } from "@copilotkit/react-core";
import { ProductCard } from "./components/ProductCard";

// In your component
useCopilotAction({
  name: "render_product_card",
  description: "Render a product card UI component",
  parameters: [
    {
      name: "name",
      type: "string",
      description: "Product name"
    },
    {
      name: "price",
      type: "number",
      description: "Product price"
    },
    // ... other params
  ],
  handler: async (props) => {
    return renderCopilotComponent(<ProductCard {...props} />);
  }
});
```

Now when agent mentions products, beautiful cards render inline! 🎨

---

### Feature 2: Human-in-the-Loop

Let users approve sensitive actions:

**Backend**:

```python
# Mark functions that require approval
FunctionDeclaration(
    name="process_refund",
    description="Process a refund for an order (requires user approval)",
    parameters={
        "type": "object",
        "properties": {
            "order_id": {"type": "string"},
            "amount": {"type": "number"},
            "reason": {"type": "string"}
        },
        "required": ["order_id", "amount", "reason"]
    },
    # Mark as requiring approval
    metadata={"requires_approval": True}
)
```

**Frontend**:

```typescript
import { useCopilotAction } from "@copilotkit/react-core";

useCopilotAction({
  name: "process_refund",
  description: "Process a refund",
  parameters: [...],
  handler: async ({ order_id, amount, reason }) => {
    // Show confirmation dialog
    const confirmed = window.confirm(
      `Approve refund of $${amount} for order ${order_id}?\n\nReason: ${reason}`
    );

    if (!confirmed) {
      return { status: "cancelled", message: "Refund cancelled by user" };
    }

    // Process refund
    const result = await processRefund(order_id, amount, reason);
    return result;
  },
});
```

User sees: "Approve refund of $99.99 for order ORD-12345? Yes/No"

---

### Feature 3: Shared State

Sync agent state with app state in real-time:

```typescript
"use client";

import { useCopilotReadable } from "@copilotkit/react-core";
import { useState } from "react";

export default function Home() {
  const [user Data, setUserData] = useState({
    name: "John Doe",
    email: "john@example.com",
    accountType: "Premium",
    orders: ["ORD-12345", "ORD-67890"]
  });

  // Make user data readable by agent
  useCopilotReadable({
    description: "Current user's account information",
    value: userData
  });

  return (
    <CopilotKit runtimeUrl="http://localhost:8000/copilotkit">
      {/* Agent can now access userData automatically! */}
      <CopilotChat />
    </CopilotKit>
  );
}
```

Agent automatically knows: "Hi John! I see you have 2 orders. Which one would you like to check?"

---

## Production Deployment

### Architecture Overview

```text
┌──────────────────┐         ┌──────────────────┐
│    Vercel        │         │   Cloud Run      │
│  (Frontend)      │◄───────►│   (Agent)        │
│  - Next.js app   │  HTTPS  │  - FastAPI       │
│  - Global CDN    │         │  - Auto-scaling  │
│  - Edge network  │         │  - 0-N instances │
└──────────────────┘         └──────────────────┘
        │                            │
        │                            │
        ▼                            ▼
  User browsers              Gemini 2.0 API
```

### Step 1: Deploy Agent to Cloud Run

**Create `agent/Dockerfile`**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY agent.py .
COPY .env .

# Expose port
EXPOSE 8000

# Run agent
CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy to Cloud Run**:

```bash
# Build and deploy
gcloud run deploy customer-support-agent \
  --source=./agent \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_api_key"

# Output:
# Service URL: https://customer-support-agent-abc123.run.app
```

---

### Step 2: Deploy Frontend to Vercel

**Update `app/page.tsx`** with production URL:

```typescript
const AGENT_URL = process.env.NEXT_PUBLIC_AGENT_URL || "http://localhost:8000";

export default function Home() {
  return (
    <CopilotKit runtimeUrl={`${AGENT_URL}/copilotkit`}>
      <CopilotChat />
    </CopilotKit>
  );
}
```

**Deploy**:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_AGENT_URL production
# Enter: https://customer-support-agent-abc123.run.app

# Deploy again with env
vercel --prod
```

**Your app is live!** 🚀

URL: `https://customer-support-bot.vercel.app`

---

### Step 3: Production Best Practices

**1. Environment Variables**

```bash
# Vercel (Frontend)
NEXT_PUBLIC_AGENT_URL=https://agent.run.app

# Cloud Run (Agent)
GOOGLE_API_KEY=xxx
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**2. CORS Configuration**

```python
# agent/agent.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://customer-support-bot.vercel.app",
        "https://*.vercel.app",  # Preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**3. Rate Limiting**

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/copilotkit")
@limiter.limit("100/hour")  # 100 requests per hour per IP
async def copilotkit_endpoint(...):
    ...
```

**4. Monitoring**

```python
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

# Set up Google Cloud Trace
tracer = trace.get_tracer(__name__)

@app.post("/copilotkit")
async def copilotkit_endpoint(...):
    with tracer.start_as_current_span("copilotkit_request"):
        # ... handle request
        pass
```

**5. Error Handling**

```python
from fastapi import HTTPException, status

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"}
    )
```

---

## Troubleshooting

### Common Issues

**Issue 1: WebSocket Connection Failed**

**Symptoms**:

- Chat doesn't load
- Console error: "WebSocket connection failed"

**Solution**:

```typescript
// Check runtimeUrl is correct
<CopilotKit runtimeUrl="http://localhost:8000/copilotkit">  // ✅ Correct
<CopilotKit runtimeUrl="http://localhost:8000">  // ❌ Missing /copilotkit
```

---

**Issue 2: Agent Not Responding**

**Symptoms**:

- Messages send but no response
- Loading spinner forever

**Solution**:

```bash
# Check agent is running
curl http://localhost:8000/health

# Check logs
# In agent terminal, look for errors

# Verify API key
echo $GOOGLE_API_KEY  # Should show your key
```

---

**Issue 3: CORS Errors in Production**

**Symptoms**:

- Works locally, fails in production
- Browser console: "CORS policy blocked"

**Solution**:

```python
# agent/agent.py - Add your production domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-app.vercel.app",  # Add this!
        "http://localhost:3000",  # Keep for local dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

**Issue 4: Tools Not Working**

**Symptoms**:

- Agent doesn't call functions
- Responses are generic

**Solution**:

```python
# Verify tool registration
app = create_copilotkit_runtime(
    agent=agent,
    tools={
        "search_knowledge_base": search_knowledge_base,  # ✅ Must match FunctionDeclaration name
        "searchKnowledgeBase": search_knowledge_base,    # ❌ Wrong name
    }
)

# Check function signature
def search_knowledge_base(query: str) -> Dict[str, str]:  # ✅ Return type hint
def search_knowledge_base(query):  # ❌ Missing type hint
```

---

**Issue 5: Slow Responses**

**Symptoms**:

- Agent takes 10+ seconds to respond
- Users complain about lag

**Solution**:

```python
from google.adk.agents import Agent

# Use fast model and optimize instructions
agent = Agent(
    model="gemini-2.0-flash-exp",  # ✅ Fast model
    # model="gemini-2.0-pro-exp",  # ❌ Slower, use only when needed
    name="customer_support_agent",
    instruction="Be concise. Answer in 2-3 sentences max."  # ✅ Shorter is better
)

# ❌ Avoid: Very long instructions slow down responses
# instruction="You are an extremely detailed agent..." (5 paragraphs)

# Use caching for knowledge base
from functools import lru_cache

@lru_cache(maxsize=128)
def search_knowledge_base(query: str):
    # Cached for repeated queries
    ...
```

---

## Next Steps

### You've Mastered Next.js + ADK! 🎉

You now know how to:

✅ Build production-ready Next.js 15 + ADK apps  
✅ Integrate CopilotKit/AG-UI Protocol  
✅ Create custom tools and agents  
✅ Add generative UI and HITL  
✅ Deploy to Vercel + Cloud Run  
✅ Monitor and troubleshoot

### Continue Learning

**Tutorial 31**: React Vite + ADK Integration  
Build a lightweight alternative with React Vite (same patterns, faster dev)

**Tutorial 32**: Streamlit + ADK Integration  
Build data apps with Python-only stack (no frontend code!)

**Tutorial 35**: AG-UI Deep Dive  
Master advanced features: multi-agent UI, custom protocols, enterprise patterns

### Additional Resources

- [CopilotKit Documentation](https://docs.copilotkit.ai/adk)
- [Next.js 15 Documentation](https://nextjs.org/docs)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Example: gemini-fullstack](https://github.com/google/adk-samples/tree/main/gemini-fullstack)

---

**🎉 Tutorial 30 Complete!**

**Next**: [Tutorial 31: React Vite + ADK Integration](./31_react_vite_adk_integration.md)

---

**Questions or feedback?** Open an issue on the [ADK Training Repository](https://github.com/google/adk-training).
