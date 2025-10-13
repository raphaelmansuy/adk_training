"use client";

import Link from "next/link";
import { ProductCard } from "@/components/ProductCard";

/**
 * Advanced Features Demo Page
 * 
 * This page demonstrates the three advanced features available in Tutorial 30:
 * 1. Generative UI - Rendering React components from agent responses
 * 2. Human-in-the-Loop - User approval for sensitive operations
 * 3. Shared State - Syncing application state with agent context
 */
export default function AdvancedFeaturesPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/"
            className="text-sm text-muted-foreground hover:text-foreground mb-4 inline-block"
          >
            ← Back to Chat
          </Link>
          <h1 className="text-4xl font-bold mb-2">Advanced Features</h1>
          <p className="text-lg text-muted-foreground">
            Explore powerful capabilities that enhance the customer support experience
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {/* Feature 1: Generative UI */}
          <div className="border rounded-lg p-6 bg-card">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
                />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold mb-2">Generative UI</h2>
            <p className="text-muted-foreground mb-4">
              Agent can render rich, interactive React components directly in the chat.
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Product cards with images</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Dynamic data visualization</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Interactive components</span>
              </div>
            </div>
          </div>

          {/* Feature 2: Human-in-the-Loop */}
          <div className="border rounded-lg p-6 bg-card">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold mb-2">Human-in-the-Loop</h2>
            <p className="text-muted-foreground mb-4">
              Critical actions require user approval before execution.
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Refund approvals</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Data modifications</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Sensitive operations</span>
              </div>
            </div>
          </div>

          {/* Feature 3: Shared State */}
          <div className="border rounded-lg p-6 bg-card">
            <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
              <svg
                className="w-6 h-6 text-primary"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
                />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold mb-2">Shared State</h2>
            <p className="text-muted-foreground mb-4">
              Agent has real-time access to application and user context.
            </p>
            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>User account data</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Order history</span>
              </div>
              <div className="flex items-start gap-2">
                <span className="text-primary">✓</span>
                <span>Session preferences</span>
              </div>
            </div>
          </div>
        </div>

        {/* Demo Section */}
        <div className="space-y-8">
          {/* Feature 1 Demo */}
          <div className="border rounded-lg p-8 bg-card">
            <h3 className="text-2xl font-semibold mb-4">1. Generative UI Example</h3>
            <p className="text-muted-foreground mb-6">
              When the agent calls <code className="px-2 py-1 bg-muted rounded">create_product_card()</code>, 
              the frontend renders a rich product card component:
            </p>
            <div className="flex justify-center">
              <ProductCard
                name="Widget Pro"
                price={99.99}
                image="https://placehold.co/400x400/6366f1/fff.png"
                rating={4.5}
                inStock={true}
              />
            </div>
            <div className="mt-6 p-4 bg-muted rounded-lg">
              <p className="text-sm font-semibold mb-2">Try asking:</p>
              <ul className="text-sm space-y-1 text-muted-foreground">
                <li>"Show me product PROD-001"</li>
                <li>"What products do you have available?"</li>
                <li>"Tell me about the Widget Pro"</li>
              </ul>
            </div>
          </div>

          {/* Feature 2 Demo */}
          <div className="border rounded-lg p-8 bg-card">
            <h3 className="text-2xl font-semibold mb-4">2. Human-in-the-Loop Example</h3>
            <p className="text-muted-foreground mb-6">
              When the agent attempts a refund, you'll see a confirmation dialog:
            </p>
            <div className="p-6 border-2 border-dashed rounded-lg bg-background">
              <div className="text-center">
                <div className="text-4xl mb-4">🔔</div>
                <h4 className="text-lg font-semibold mb-2">Refund Approval Required</h4>
                <div className="text-sm text-muted-foreground space-y-1 mb-4">
                  <p>Order ID: ORD-12345</p>
                  <p>Amount: $99.99</p>
                  <p>Reason: Product defective</p>
                </div>
                <div className="flex gap-2 justify-center">
                  <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md">
                    Approve
                  </button>
                  <button className="px-4 py-2 bg-muted text-muted-foreground rounded-md">
                    Deny
                  </button>
                </div>
              </div>
            </div>
            <div className="mt-6 p-4 bg-muted rounded-lg">
              <p className="text-sm font-semibold mb-2">Try asking:</p>
              <ul className="text-sm space-y-1 text-muted-foreground">
                <li>"I want a refund for order ORD-12345"</li>
                <li>"Process a refund of $99.99 for my order"</li>
                <li>"Can you refund my purchase?"</li>
              </ul>
            </div>
          </div>

          {/* Feature 3 Demo */}
          <div className="border rounded-lg p-8 bg-card">
            <h3 className="text-2xl font-semibold mb-4">3. Shared State Example</h3>
            <p className="text-muted-foreground mb-6">
              The agent can access your account information without asking:
            </p>
            <div className="p-6 border rounded-lg bg-background">
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="font-semibold">Name:</span>
                  <span className="text-muted-foreground">John Doe</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-semibold">Email:</span>
                  <span className="text-muted-foreground">john@example.com</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-semibold">Account Type:</span>
                  <span className="text-primary font-semibold">Premium</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-semibold">Orders:</span>
                  <span className="text-muted-foreground">ORD-12345, ORD-67890</span>
                </div>
                <div className="flex justify-between">
                  <span className="font-semibold">Member Since:</span>
                  <span className="text-muted-foreground">January 15, 2023</span>
                </div>
              </div>
            </div>
            <div className="mt-6 p-4 bg-muted rounded-lg">
              <p className="text-sm font-semibold mb-2">Try asking:</p>
              <ul className="text-sm space-y-1 text-muted-foreground">
                <li>"What's my account status?"</li>
                <li>"Show me my recent orders"</li>
                <li>"When did I join?"</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Implementation Guide */}
        <div className="mt-12 border rounded-lg p-8 bg-card">
          <h3 className="text-2xl font-semibold mb-4">Implementation Details</h3>
          <div className="space-y-6">
            <div>
              <h4 className="font-semibold mb-2">Backend (agent/agent.py)</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• <code>create_product_card()</code> - Returns structured product data</li>
                <li>• <code>process_refund()</code> - Handles refund logic</li>
                <li>• Agent instruction includes guidance for all features</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Frontend (app/page.tsx)</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• <code>useCopilotAction()</code> - Register actions for Generative UI and HITL</li>
                <li>• <code>useCopilotReadable()</code> - Share state with agent</li>
                <li>• <code>ProductCard</code> component - Rich UI rendering</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Components (components/)</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• <code>ProductCard.tsx</code> - Reusable product display component</li>
                <li>• <code>ThemeToggle.tsx</code> - Dark/light mode switcher</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Back to Chat Button */}
        <div className="mt-8 text-center">
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
              />
            </svg>
            Try Advanced Features in Chat
          </Link>
        </div>
      </div>
    </div>
  );
}
