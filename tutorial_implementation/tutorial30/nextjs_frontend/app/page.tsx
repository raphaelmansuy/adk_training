"use client";

import { useState, useEffect } from "react";
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
  // State to manage approval dialog
  const [refundRequest, setRefundRequest] = useState<{
    order_id: string;
    amount: number;
    reason: string;
  } | null>(null);

  // Frontend-only action that shows approval dialog using available: "remote"
  useCopilotAction({
    name: "process_refund",
    available: "remote",
    description: "Process a refund after user approval",
    parameters: [
      { name: "order_id", type: "string", description: "Order ID to refund", required: true },
      { name: "amount", type: "number", description: "Refund amount", required: true },
      { name: "reason", type: "string", description: "Refund reason", required: true },
    ],
    handler: async ({ order_id, amount, reason }) => {
      console.log("🔍 HITL handler called with:", { order_id, amount, reason });
      
      // Store the refund request to show in the dialog
      setRefundRequest({ order_id, amount, reason });
      
      // Return a promise that resolves when user approves/cancels
      return new Promise((resolve) => {
        // We'll resolve this in the dialog buttons
        (window as any).__refundPromiseResolve = resolve;
      });
    },
    render: ({ args, status }) => {
      console.log("🔍 HITL render - Status:", status, "Args:", args);
      
      if (status !== "complete") {
        // Show loading while waiting for user decision
        return (
          <div className="p-5 border-2 border-yellow-300 dark:border-yellow-700 rounded-xl bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 space-y-3 shadow-lg">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-yellow-500 rounded-full flex items-center justify-center animate-pulse">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h4 className="font-bold text-lg text-yellow-900 dark:text-yellow-100">Awaiting Your Approval</h4>
                <p className="text-sm text-yellow-700 dark:text-yellow-300">Please review the modal dialog above</p>
              </div>
            </div>
            <div className="pl-13 space-y-1">
              <div className="flex items-center gap-2 text-sm text-yellow-800 dark:text-yellow-200">
                <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                <span>Order: <strong>{args.order_id}</strong></span>
              </div>
              <div className="flex items-center gap-2 text-sm text-yellow-800 dark:text-yellow-200">
                <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse" style={{ animationDelay: "0.2s" }}></div>
                <span>Amount: <strong>${args.amount}</strong></span>
              </div>
            </div>
          </div>
        );
      }

      return (
        <div className="p-4 border-2 border-green-300 dark:border-green-700 rounded-lg bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 flex items-center gap-3 shadow-md">
          <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <p className="font-semibold text-green-900 dark:text-green-100">Decision Recorded</p>
            <p className="text-sm text-green-700 dark:text-green-300">Processing your choice...</p>
          </div>
        </div>
      );
    },
  });

  // Render approval dialog when refundRequest is set
  const handleRefundApproval = async (approved: boolean) => {
    console.log("🔍 User decision:", approved ? "APPROVED" : "CANCELLED");
    
    const resolve = (window as any).__refundPromiseResolve;
    if (resolve && refundRequest) {
      if (approved) {
        // Call backend API to actually process the refund
        try {
          const response = await fetch("http://localhost:8000/api/copilotkit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              action: "process_refund_backend",
              params: refundRequest,
            }),
          });
          const result = await response.json();
          resolve({
            approved: true,
            message: `Refund processed successfully for order ${refundRequest.order_id}`,
          });
        } catch (error) {
          resolve({
            approved: true,
            message: `Refund approved for order ${refundRequest.order_id} - $${refundRequest.amount}`,
          });
        }
      } else {
        resolve({
          approved: false,
          message: "Refund cancelled by user",
        });
      }
    }
    
    setRefundRequest(null);
    delete (window as any).__refundPromiseResolve;
  };

  // Keyboard support for modal (ESC to cancel, Enter to approve)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (refundRequest) {
        if (e.key === "Escape") {
          e.preventDefault();
          handleRefundApproval(false);
        } else if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          handleRefundApproval(true);
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [refundRequest]);  return (
    <div className="flex flex-col min-h-screen">
      {/* HITL Approval Dialog - Enhanced UX Modal */}
      {refundRequest && (
        <div 
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4 animate-in fade-in duration-200"
          onClick={(e) => {
            // Close modal if clicking backdrop
            if (e.target === e.currentTarget) {
              handleRefundApproval(false);
            }
          }}
        >
          <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl p-8 max-w-md w-full shadow-2xl animate-in zoom-in-95 duration-200">
            {/* Header with icon */}
            <div className="flex items-start gap-4 mb-6">
              <div className="flex-shrink-0 w-14 h-14 bg-yellow-400 dark:bg-yellow-500 rounded-full flex items-center justify-center shadow-lg">
                <svg className="w-8 h-8 text-gray-900 dark:text-gray-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">Refund Approval Required</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">Please review the details below carefully</p>
              </div>
            </div>

            {/* Refund details card */}
            <div className="space-y-3 bg-gray-50 dark:bg-gray-800 rounded-lg p-5 mb-6 border border-gray-200 dark:border-gray-700">
              <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Order ID</span>
                <span className="text-sm font-mono font-semibold text-gray-900 dark:text-gray-100 bg-gray-100 dark:bg-gray-700 px-3 py-1.5 rounded-md">
                  {refundRequest.order_id}
                </span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700">
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Refund Amount</span>
                <span className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  ${refundRequest.amount.toFixed(2)}
                </span>
              </div>
              <div className="pt-2">
                <span className="text-sm font-medium text-gray-600 dark:text-gray-400 block mb-2">Reason</span>
                <div className="text-sm text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900 rounded-md p-3 border border-gray-200 dark:border-gray-700">
                  {refundRequest.reason}
                </div>
              </div>
            </div>

            {/* Warning message */}
            <div className="flex items-start gap-3 mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-500 rounded-r-lg shadow-sm">
              <svg className="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-yellow-900 dark:text-yellow-100 font-medium">
                This action cannot be undone. Approving will process the refund immediately.
              </p>
            </div>

            {/* Action buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => handleRefundApproval(false)}
                className="flex-1 px-6 py-3.5 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100 rounded-xl font-bold transition-all duration-200 hover:scale-105 active:scale-95 flex items-center justify-center gap-2 shadow-md"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Cancel
              </button>
              <button
                onClick={() => handleRefundApproval(true)}
                className="flex-1 px-6 py-3.5 bg-green-600 hover:bg-green-700 dark:bg-green-600 dark:hover:bg-green-500 text-white rounded-xl font-bold transition-all duration-200 hover:scale-105 active:scale-95 flex items-center justify-center gap-2 shadow-lg"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                </svg>
                Approve Refund
              </button>
            </div>

            {/* ESC hint */}
            <p className="text-xs text-center text-gray-500 dark:text-gray-400 mt-5">
              Press <kbd className="px-2 py-1 bg-gray-100 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded text-xs font-mono text-gray-900 dark:text-gray-100 shadow-sm">ESC</kbd> to cancel
            </p>
          </div>
        </div>
      )}

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
