"use client";

import { useState } from "react";
import { CopilotKit, useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { ThemeToggle } from "@/components/ThemeToggle";
import { ProductCard } from "@/components/ProductCard";
import { FeatureShowcase } from "@/components/FeatureShowcase";
import { Markdown } from "@copilotkit/react-ui";

/**
 * ChatInterface component with advanced features:
 * 1. Generative UI - Product cards rendered from agent responses
 * 2. Human-in-the-Loop - User approval for refunds
 * 3. Shared State - User context accessible to agent
 */
function ChatInterface() {
  // Feature 3: Shared State - User context that agent can read
  const [userData] = useState({
    name: "John Doe",
    email: "john@example.com",
    accountType: "Premium",
    orders: ["ORD-12345", "ORD-67890"],
    memberSince: "2023-01-15",
  });

  // Feature 1: Generative UI - State to hold product data for rendering
  const [currentProduct, setCurrentProduct] = useState<{
    name: string;
    price: number;
    image: string;
    rating: number;
    inStock: boolean;
  } | null>(null);

  // Make user data readable by agent
  useCopilotReadable({
    description: "Current user's account information and order history",
    value: userData,
  });

  // Feature 1: Generative UI - Frontend action that agent can call to render product cards
  // Using available: "remote" means this action is ONLY callable by the backend agent
  useCopilotAction({
    name: "render_product_card",
    available: "remote",
    description: "Render a product card in the chat interface with product details",
    parameters: [
      { name: "name", type: "string", description: "Product name", required: true },
      { name: "price", type: "number", description: "Product price in USD", required: true },
      { name: "image", type: "string", description: "Product image URL", required: true },
      { name: "rating", type: "number", description: "Product rating (0-5)", required: true },
      { name: "inStock", type: "boolean", description: "Product availability", required: true },
    ],
    handler: async ({ name, price, image, rating, inStock }) => {
      // Update state to show the product card
      setCurrentProduct({ name, price, image, rating, inStock });
      
      // Return success message to agent
      return `Product card displayed successfully for ${name}`;
    },
    render: ({ args, status }) => {
      // Show loading while processing
      if (status !== "complete") {
        return (
          <div className="p-4 border rounded-lg animate-pulse bg-card">
            <div className="h-48 bg-muted rounded mb-4"></div>
            <div className="h-4 bg-muted rounded w-3/4 mb-2"></div>
            <div className="h-4 bg-muted rounded w-1/2"></div>
          </div>
        );
      }

      // Render the actual ProductCard component when complete
      return (
        <div className="my-4">
          <ProductCard
            name={args.name}
            price={args.price}
            image={args.image}
            rating={args.rating}
            inStock={args.inStock}
          />
        </div>
      );
    },
  });

  // Feature 2: Human-in-the-Loop - Refund approval
  // This intercepts process_refund calls and requires user approval
  // Using available: "enabled" with renderAndWaitForResponse for HITL
  useCopilotAction({
    name: "process_refund",
    available: "enabled",
    description: "Process a refund with user approval",
    parameters: [
      { name: "order_id", type: "string", description: "Order ID to refund", required: true },
      { name: "amount", type: "number", description: "Refund amount", required: true },
      { name: "reason", type: "string", description: "Refund reason", required: true },
    ],
    renderAndWaitForResponse: ({ args, respond, status }) => {
      if (status !== "executing") return <div />;

      return (
        <div className="p-4 border rounded-lg bg-card space-y-4">
          <h4 className="font-semibold text-lg">🔔 Refund Approval Required</h4>
          <div className="space-y-2 text-sm">
            <p>
              <strong>Order ID:</strong> {args.order_id}
            </p>
            <p>
              <strong>Amount:</strong> ${Number(args.amount || 0).toFixed(2)}
            </p>
            <p>
              <strong>Reason:</strong> {args.reason}
            </p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => respond?.({ approved: false })}
              className="px-4 py-2 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-lg text-sm hover:bg-red-200 dark:hover:bg-red-800"
            >
              ❌ Cancel
            </button>
            <button
              onClick={() => respond?.({ approved: true })}
              className="px-4 py-2 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-lg text-sm hover:bg-green-200 dark:hover:bg-green-800"
            >
              ✅ Approve Refund
            </button>
          </div>
        </div>
      );
    },
  });

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 bg-primary rounded-md">
                <svg
                  className="w-5 h-5 text-primary-foreground"
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
              </div>
              <div>
                <h1 className="text-lg font-semibold">Support Assistant</h1>
                <p className="text-xs text-muted-foreground">
                  AI-Powered Help • Logged in as {userData.name}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <a
                href="/advanced"
                className="text-sm text-muted-foreground hover:text-foreground transition-colors flex items-center gap-1"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
                Advanced Features
              </a>
              <ThemeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Chat */}
      <main className="flex-1">
        <div className="container mx-auto px-4 py-6 h-[600px]">
          <div className="h-full border rounded-lg bg-card">
            <CopilotChat
              instructions="You are a friendly and professional customer support agent. Be helpful, empathetic, and provide clear, actionable solutions. You have access to the user's account information."
              labels={{
                title: "Support Chat",
                initial:
                  "👋 Hi! I'm your AI support assistant.\n\n" +
                  "**Try these example prompts:**\n\n" +
                  "🎨 **Generative UI**\n" +
                  "• \"Show me product PROD-001\"\n" +
                  "• \"Display product PROD-002\"\n\n" +
                  "🔐 **Human-in-the-Loop**\n" +
                  "• \"I want a refund for order ORD-12345\"\n" +
                  "• \"Process a refund for my purchase\"\n\n" +
                  "👤 **Shared State**\n" +
                  "• \"What's my account status?\"\n" +
                  "• \"Show me my recent orders\"\n\n" +
                  "📦 **General Support**\n" +
                  "• \"What is your refund policy?\"\n" +
                  "• \"Track my order ORD-67890\"\n" +
                  "• \"I need help with a billing issue\"\n\n" +
                  "💡 *Scroll down to see interactive demos of all features!*",
              }}
              className="h-full"
            />
          </div>
        </div>
      </main>

      {/* Feature Showcase */}
      <FeatureShowcase userData={userData} />
    </div>
  );
}

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <CopilotKit runtimeUrl="/api/copilotkit" agent="customer_support_agent">
        <ChatInterface />
      </CopilotKit>
    </div>
  );
}
